# examples/ — 样本库与回归基准

本目录存放该技能的**回归测试样本**：固定的题目输入（`input.md`）、人工审定的参考输出（`reference.md`）、以及可机器校验的检查清单（`checklist.md` + `checks.json`）。

## 它解决什么问题

本技能是纯声明式的——仓库中只有一份 `SKILL.md` 指令，没有任何可执行代码。因此「测试」不可能落在函数上，只能落在**模型输出的文本**上。而模型输出天然不确定，无法做字符串精确比对。

本目录提供的是**分级基线**：

| 级别 | 组成 | 用途 | 维护成本 |
|---|---|---|---|
| **Tier A** | `input.md` + `reference.md` + `checklist.md` + `checks.json` | 锚定输出风格与深度，作为 LLM-as-judge 的比对对象 | 高（每次措辞调整需重录） |
| **Tier B** | `input.md` + `checklist.md` + `checks.json` | 只校验流程结构与关键事实，不约束措辞 | 低（规则稳定时不需改动） |

**Tier B 优先、逐步补齐 Tier A** 是本目录的既定策略：结构规则（8 步流程是否齐全、关键结论是否正确）长期稳定，而完整参考输出会随每一版措辞调整而迅速失效。

## 目录结构

```text
examples/
├── README.md              # 本文件
├── RUBRIC.md              # 判定规则与 judge 提示词模板
├── check.py               # 确定性检查脚本（Python 3，零第三方依赖）
├── _template/             # 新增样本时复制此目录
│   ├── input.md
│   ├── checklist.md
│   └── checks.json
├── signal-systems/        # 主线：信号与系统
│   ├── 01-laplace-inverse/
│   ├── 02-convolution-piecewise/
│   ├── 03-fourier-series/
│   ├── 04-stability-causality/
│   ├── 05-z-transform-difference/
│   └── 06-sampling-aliasing/
├── postgrad-math/         # 副线：考研数学
│   ├── 01-parametric-integral/
│   ├── 02-matrix-rank-system/
│   ├── 03-power-series/
│   ├── 04-multivariable-derivative/
│   ├── 05-double-integral/
│   └── 06-probability-distribution/
└── special-cases/         # 特殊情形
    ├── 01-mcq-elimination/
    ├── 02-program-trace/
    ├── 03-image-ambiguity/
    └── 04-multi-part-dependent/
```

## 样本选取原则

样本的价值在于**覆盖 `SKILL.md` 中最容易退化的规则分支**，而不是学科广度。选取优先级：

1. `SKILL.md` 明文点名的易错环节——分段、绝对值、卷积、积分区间、变换域、矩阵维度、程序执行过程。
2. 验算三件套——定义域、收敛域、因果稳定条件。
3. 特殊情形规则——公式追问、概念追问、选择题、编程题、图片题、多问大题。
4. 输出可判定性——优先选最终答案唯一、可写成确定条件的样本。

**不纳入样本集**：需要图片文件才能作答的题（纯文本仓库无法承载）、答案不唯一的开放题。

## 样本状态一览

| 样本 | 学科 | 基线级别 | 锁定的主要规则 |
|---|---|---|---|
| `signal-systems/01-laplace-inverse` | 信号与系统 | Tier A | 双边拉普拉斯逆变换、收敛域与因果性的绑定关系 |
| `signal-systems/02-convolution-piecewise` | 信号与系统 | Tier A | 卷积积分区间划分、分段讨论、绝对值处理 |
| `signal-systems/03-fourier-series` | 信号与系统 | Tier A | 傅里叶级数、狄利克雷条件、端点收敛值 |
| `signal-systems/04-stability-causality` | 信号与系统 | Tier A | 系统函数分解、因果性与稳定性判据、零状态响应 |
| `signal-systems/05-z-transform-difference` | 信号与系统 | Tier A | Z 变换、差分方程、ROC 与因果/稳定性的绑定 |
| `signal-systems/06-sampling-aliasing` | 信号与系统 | Tier A | 奈奎斯特采样率、频谱混叠、混叠后频率计算 |
| `postgrad-math/01-parametric-integral` | 考研数学 | Tier A | 含参积分求导、端点收敛性、积分区间 |
| `postgrad-math/02-matrix-rank-system` | 考研数学 | Tier A | 行列式、秩、含参方程组解的讨论 |
| `postgrad-math/03-power-series` | 考研数学 | Tier B | 幂级数展开、收敛半径、端点敛散性 |
| `postgrad-math/04-multivariable-derivative` | 考研数学 | Tier B | 多元偏导、全微分、混合偏导交换 |
| `postgrad-math/05-double-integral` | 考研数学 | Tier B | 积分区域描述、换序、极坐标 |
| `postgrad-math/06-probability-distribution` | 考研数学 | Tier B | 分布函数分段、数字特征计算 |
| `special-cases/01-mcq-elimination` | 选择题 | Tier A | 标准推导先行、排除法及其适用边界 |
| `special-cases/02-program-trace` | 编程题 | Tier A | 变量逐步变化、执行顺序、循环边界 |
| `special-cases/03-image-ambiguity` | 图片题 | Tier B | 歧义符号暂停协议（**期望行为是不给答案**） |
| `special-cases/04-multi-part-dependent` | 信号与系统 | Tier B | 多问大题的子问依赖声明 |

## 如何运行检查

```bash
# 列出全部样本
python examples/check.py --list

# 检查单个样本（输出文件为该次实际生成的完整回答）
python examples/check.py --sample signal-systems/01-laplace-inverse --output /tmp/out.md

# 批量检查：每个样本对应 outputs/<sample-id>.md
python examples/check.py --all --outputs-dir ./outputs

# 打印某个样本的检查项清单
python examples/check.py --sample signal-systems/01-laplace-inverse --show
```

脚本只做**确定性检查**（章节齐全、关键词出现、禁语缺席、关键结论存在）。风格与深度维度的判定见 `RUBRIC.md`，需 LLM-as-judge 或人工完成。

## 新增样本的流程

1. 复制 `_template/` 为 `examples/<学科>/<序号>-<短名>/`。
2. 在 `input.md` 写入**可复现的完整题目**（含全部已知条件，不引用外部资料）。
3. 在 `checklist.md` 写明该样本要锁定的规则与判定条件。
4. 在 `checks.json` 填写机器可校验项（章节名、关键词、禁语、关键结论的若干可接受写法）。
5. Tier A 样本额外产出 `reference.md`，并在 `checklist.md` 中标注人工审定的关键结论。
6. 提交 PR 时在描述中说明该样本锁定了哪条规则——参见仓库根 `README.md` 的贡献建议。

## 重要说明

**本目录不参与技能运行时。** `SKILL.md` 未引用 `examples/`，宿主模型在推理时不会读取这里的任何文件。它的作用是**维护者的回归基准**，而非 few-shot 示例。

若希望参考输出影响实际生成质量，需要把其中的片段以 few-shot 形式内嵌进 `SKILL.md`——这是另一项工作，与本目录相互独立。
