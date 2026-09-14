# matrix-cli

矩阵运算命令行工具 ⚡

## 安装

```bash
# 创建虚拟环境并安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 安装为可执行命令
pip install -e .
```

## 快速上手

```bash
# 矩阵加法
matrix-cli add "1,2;3,4" "5,6;7,8"

# 矩阵乘法
matrix-cli mul "1,2,3;4,5,6" "7,8;9,10;11,12"

# 显示矩阵
matrix-cli show "1,2;3,4"

# 查看维度
matrix-cli info "1,2,3;4,5,6"
```

## 输入格式

矩阵用一对引号包裹，规则如下：

- **逗号 `,` 或空格** 分隔同一行的元素
- **分号 `;` 或换行** 分隔不同的行

```
"1,2;3,4"        → 2×2 矩阵
"1 2 3;4 5 6"    → 2×3 矩阵
"1 2
 3 4"            → 2×2 矩阵（多行输入）
```

## 命令详解

| 命令 | 说明 | 维度要求 |
| --- | --- | --- |
| `add <A> <B>` | 逐元素相加 | 两个矩阵行列数相同 |
| `mul <A> <B>` | 矩阵乘法 | A 的列数 = B 的行数 |
| `show <M>` | 展示矩阵及其维度 | 无 |
| `info <M>` | 查看矩阵维度 | 无 |

维度不匹配时，会给出清晰的中文错误提示。

## Python 库用法

除了 CLI，代码也可作为库使用：

```python
from src.matrix import Matrix

a = Matrix([[1, 2], [3, 4]])
b = Matrix([[5, 6], [7, 8]])

print(a + b)   # 加法, 重新实现了 __str__
print(a * b)   # 乘法
print(a.shape) # (2, 2)
```

或运行演示脚本：

```bash
python main.py
```

## 开发

```bash
# 直接以模块方式运行 CLI（无需安装）
python -m src.cli add "1,2;3,4" "5,6;7,8"
```