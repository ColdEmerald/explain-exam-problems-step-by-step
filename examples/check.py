#!/usr/bin/env python3
"""examples/ 样本的确定性检查器。

只做字面层面的检查：章节是否齐全、关键词是否出现、禁语是否缺席、
关键结论是否存在。它不判断推导是否正确、不判断表达是否优美——
那些交给 RUBRIC.md 里的人工或 LLM-as-judge。

用法：
    python examples/check.py --list
    python examples/check.py --sample signal-systems/01-laplace-inverse --show
    python examples/check.py --sample signal-systems/01-laplace-inverse --output out.md
    python examples/check.py --all --outputs-dir ./outputs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent

DEFAULT_FORBIDDEN = ["显然", "容易得", "同理可得"]

# 标准模式（完整 8 步流程）要求出现的章节
STANDARD_SECTIONS = [
    "题型判断",
    "第一眼突破口",
    "逐步推导",
    "解题思维复盘",
    "核心套路总结",
    "易错点",
    "更快捷的方法",
    "同类型变式题",
]

# 简明模式（3 步）
BRIEF_SECTIONS = ["题型判断", "逐步推导", "最终答案"]

# 禁语只在这些章节正文中扫描。排除「易错点」——该节经常把「显然成立」
# 作为反例引用，若扫全文会产生误判。
FORBIDDEN_SCAN_SECTIONS = ["逐步推导"]



def load_samples() -> list[dict]:
    """读取所有样本的 checks.json，按目录名排序返回。"""
    samples = []
    for path in sorted(EXAMPLES_DIR.rglob("checks.json")):
        if "_template" in path.parts:
            continue
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec["_dir"] = path.parent
        spec["_rel"] = path.parent.relative_to(EXAMPLES_DIR).as_posix()
        spec.setdefault("mode", "standard")
        spec.setdefault("forbidden_keywords", DEFAULT_FORBIDDEN)
        if spec["mode"] == "brief":
            spec.setdefault("required_sections", BRIEF_SECTIONS)
        else:
            spec.setdefault("required_sections", STANDARD_SECTIONS)
        samples.append(spec)
    return samples


def find_sample(samples: list[dict], sample_id: str) -> dict | None:
    for spec in samples:
        if spec["_rel"] == sample_id or spec.get("id") == sample_id:
            return spec
    return None


def _expand_braces(text: str, start: int) -> tuple[str, int]:
    """把 text[start] 处的 {...} 内容取出，返回 (内容, 结束位置)。"""
    if start >= len(text) or text[start] != "{":
        return "", start
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
    return text[start + 1 :], len(text)


def normalize_math(text: str) -> str:
    """归一化数学表达式，使 LaTeX 与纯文本写法的同一结论可比。

    处理：去除空白与 $ 包裹、剥离 \\left \\right 等排版命令、
    \\frac{a}{b} 展开为 (a)/(b)、\\mathrm \\text 包裹的内容取裸文本。
    """
    text = text.replace("$", "")
    text = re.sub(r"\\(?:left|right|!|,|;|:|quad|qquad|displaystyle)\b", "", text)
    text = re.sub(r"\\(?:dfrac|tfrac)\b", r"\\frac", text)
    text = re.sub(r"\\mathrm\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\text\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:cdot|times)\b", "*", text)

    # \frac{a}{b} -> a/b 或 (a)/(b)：分子含运算符时加括号
    out = []
    index = 0
    while index < len(text):
        if text.startswith("\\frac", index):
            cursor = index + 5
            numerator, cursor = _expand_braces(text, cursor)
            denominator, cursor = _expand_braces(text, cursor)
            if re.fullmatch(r"[A-Za-z0-9]+", numerator):
                out.append(f"{numerator}/({denominator})")
            else:
                out.append(f"({numerator})/({denominator})")
            index = cursor
            continue
        out.append(text[index])
        index += 1
    text = "".join(out)

    return re.sub(r"\s+", "", text)


def extract_headings(text: str) -> list[str]:
    """提取 Markdown 标题的纯文本内容，忽略编号与装饰符。"""
    headings = []
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.*)$", line)
        if not match:
            continue
        title = match.group(2)
        title = re.sub(r"[*_`]", "", title)
        title = re.sub(r"^\s*\d+[.、)]\s*", "", title)
        headings.append(title.strip())
    return headings


def extract_section_body(text: str, keyword: str) -> str | None:
    """取出标题含 keyword 的那一节正文（不含标题本身）。

    章节边界为下一个同级或更高级标题。找不到返回 None。
    """
    lines = text.splitlines()
    start = None
    level = 0
    for index, line in enumerate(lines):
        match = re.match(r"^(\s{0,3})(#{1,6})\s+(.*)$", line)
        if not match:
            continue
        title = re.sub(r"[*_`]", "", match.group(3)).strip()
        title = re.sub(r"^\s*\d+[.、)]\s*", "", title)
        if keyword in title:
            start = index + 1
            level = len(match.group(2))
            break
    if start is None:
        return None

    end = len(lines)
    for index in range(start, len(lines)):
        match = re.match(r"^\s{0,3}(#{1,6})\s+", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end])



def check_sample(spec: dict, output: str) -> list[tuple[bool, str, str]]:
    """返回 [(是否通过, 检查项说明, 失败原因)]。"""
    results: list[tuple[bool, str, str]] = []
    headings = extract_headings(output)

    for keyword in spec["required_sections"]:
        hit = any(keyword in heading for heading in headings)
        results.append(
            (
                hit,
                f"章节存在：{keyword}",
                "" if hit else "未找到含该词的标题",
            )
        )

    for keyword in spec.get("absent_sections", []):
        hit = any(keyword in heading for heading in headings)
        results.append(
            (
                not hit,
                f"章节不应出现：{keyword}",
                "" if not hit else "出现了本应缺席的标题",
            )
        )

    for keyword in spec.get("required_keywords", []):
        alternatives = spec.get("keyword_alternatives", {}).get(keyword, [keyword])
        hit = any(alt in output for alt in alternatives)
        results.append(
            (
                hit,
                f"关键词出现：{keyword}",
                "" if hit else "输出中未出现该词（可接受写法：" + " / ".join(alternatives) + "）",
            )
        )

    for keyword in spec.get("forbidden_keywords", []):
        scanned = output
        scope = "全文"
        for section in FORBIDDEN_SCAN_SECTIONS:
            body = extract_section_body(output, section)
            if body is not None:
                scanned = body
                scope = f"「{section}」节"
                break
        hit = keyword in scanned
        results.append(
            (
                not hit,
                f"禁语缺席：{keyword}（扫描范围：{scope}）",
                "" if not hit else f"在{scope}中出现了禁用词",
            )
        )

    for fact in spec.get("key_facts", []):
        candidates = fact.get("any_of", [])
        hit = any(candidate in output for candidate in candidates)
        if not hit and candidates:
            normalized = normalize_math(output)
            hit = any(normalize_math(candidate) in normalized for candidate in candidates)
        results.append(
            (
                hit,
                f"关键结论：{fact['desc']}",
                "" if hit else "所有候选写法均未命中：" + " | ".join(candidates),
            )
        )

    # token 约束：要求若干片段同时出现（all_of），且另一些片段不出现（none_of）。
    # 适用于「同一份输出里有多分支答案」的场景——此时单个片段无法定位到具体分支，
    # 但 all_of / none_of 的组合仍能排除明显错误。
    for fact in spec.get("token_facts", []):
        all_of = fact.get("all_of", [])
        none_of = fact.get("none_of", [])
        missing = [token for token in all_of if token not in output]
        present = [token for token in none_of if token in output]
        ok = not missing and not present
        detail = ""
        if missing:
            detail += "缺少：" + "、".join(missing) + " "
        if present:
            detail += "不应出现：" + "、".join(present)
        results.append((ok, f"token 约束：{fact['desc']}", detail.strip()))

    for fact in spec.get("absent_facts", []):
        candidates = fact["any_of"]
        hit = any(candidate in output for candidate in candidates)
        results.append(
            (
                not hit,
                f"结论不应出现：{fact['desc']}",
                "" if not hit else "出现了本应缺席的结论",
            )
        )

    return results


def print_report(spec: dict, results: list[tuple[bool, str, str]]) -> bool:
    passed = sum(1 for ok, _, _ in results if ok)
    total = len(results)
    print(f"\n=== {spec['_rel']} ({spec.get('title', '')}) ===")
    for ok, label, reason in results:
        mark = "PASS" if ok else "FAIL"
        line = f"  [{mark}] {label}"
        if not ok and reason:
            line += f"  -> {reason}"
        print(line)
    print(f"  ---- {passed}/{total} 通过 ----")
    return passed == total


def main() -> int:
    parser = argparse.ArgumentParser(description="examples/ 样本确定性检查器")
    parser.add_argument("--list", action="store_true", help="列出全部样本")
    parser.add_argument("--sample", help="样本 id（目录相对路径，如 signal-systems/01-laplace-inverse）")
    parser.add_argument("--output", help="待检查的输出文件（单个样本时必填）")
    parser.add_argument("--all", action="store_true", help="检查全部样本")
    parser.add_argument("--outputs-dir", help="批量模式下的输出目录，按 <sample-id>.md 取文件")
    parser.add_argument("--show", action="store_true", help="打印样本的检查项与判定条件")
    args = parser.parse_args()

    samples = load_samples()
    if not samples:
        print("未找到任何 checks.json", file=sys.stderr)
        return 2

    if args.list:
        for spec in samples:
            tier = spec.get("tier", "?")
            mode = spec.get("mode", "standard")
            print(f"{spec['_rel']:<52} tier={tier} mode={mode}  {spec.get('title', '')}")
        print(f"\n共 {len(samples)} 个样本")
        return 0

    if args.show:
        if not args.sample:
            print("--show 需要配合 --sample 使用", file=sys.stderr)
            return 2
        spec = find_sample(samples, args.sample)
        if spec is None:
            print(f"未找到样本：{args.sample}", file=sys.stderr)
            return 2
        print(f"样本：{spec['_rel']}")
        print(f"标题：{spec.get('title', '')}")
        print(f"学科：{spec.get('subject', '')}")
        print(f"基线：Tier {spec.get('tier', '?')}    模式：{spec.get('mode', 'standard')}")
        print(f"输入：{spec.get('input', 'input.md')}")
        if spec.get("reference"):
            print(f"参考：{spec.get('reference')}")
        print("\n必须出现的章节：")
        for item in spec["required_sections"]:
            print(f"  - {item}")
        if spec.get("absent_sections"):
            print("\n必须缺席的章节：")
            for item in spec["absent_sections"]:
                print(f"  - {item}")
        if spec.get("required_keywords"):
            print("\n必须出现的关键词：")
            for item in spec["required_keywords"]:
                print(f"  - {item}")
        print("\n禁语（不得出现）：")
        for item in spec.get("forbidden_keywords", []):
            print(f"  - {item}")
        if spec.get("key_facts"):
            print("\n关键结论（任一写法命中即通过）：")
            for fact in spec["key_facts"]:
                print(f"  - {fact['desc']}")
                print(f"      候选：{' | '.join(fact['any_of'])}")
        if spec.get("token_facts"):
            print("\ntoken 约束（片段组合）：")
            for fact in spec["token_facts"]:
                print(f"  - {fact['desc']}")
                if fact.get("all_of"):
                    print(f"      须同时出现：{' | '.join(fact['all_of'])}")
                if fact.get("none_of"):
                    print(f"      不得出现：{' | '.join(fact['none_of'])}")
        if spec.get("absent_facts"):
            print("\n不应出现的结论：")
            for fact in spec["absent_facts"]:
                print(f"  - {fact['desc']}")
                print(f"      候选：{' | '.join(fact['any_of'])}")
        return 0

    if args.sample:
        spec = find_sample(samples, args.sample)
        if spec is None:
            print(f"未找到样本：{args.sample}", file=sys.stderr)
            return 2
        if not args.output:
            print("--sample 需要配合 --output 指定待检查文件", file=sys.stderr)
            return 2
        output = Path(args.output).read_text(encoding="utf-8")
        ok = print_report(spec, check_sample(spec, output))
        return 0 if ok else 1

    if args.all:
        if not args.outputs_dir:
            print("--all 需要配合 --outputs-dir 指定输出目录", file=sys.stderr)
            return 2
        out_dir = Path(args.outputs_dir)
        all_ok = True
        for spec in samples:
            candidate = out_dir / f"{spec['_rel']}.md"
            if not candidate.exists():
                print(f"\n=== {spec['_rel']} ===\n  [SKIP] 未找到输出文件 {candidate}")
                all_ok = False
                continue
            output = candidate.read_text(encoding="utf-8")
            if not print_report(spec, check_sample(spec, output)):
                all_ok = False
        print("\n" + ("全部样本通过" if all_ok else "存在未通过的样本"))
        return 0 if all_ok else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
