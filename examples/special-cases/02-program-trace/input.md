# 样本：02-program-trace

## 学科

编程（Python）

## 题目

阅读以下 Python 代码，写出程序的输出结果，并逐行说明每一步变量的变化：

```python
total = 0
for i in range(1, 5):
    if i % 2 == 0:
        total += i * i
    else:
        total -= i
print(total)
```

## 附加要求

请说明循环边界与 continue/if-else 分支对执行次数的影响。
