"""矩阵核心模块。

提供 Matrix 类，支持基本的矩阵加法、乘法运算,
以及美观的字符串展示。
"""

from typing import List, Union

Number = Union[int, float]


class Matrix:
    """简单的二维矩阵实现。

    支持 + (逐元素相加) 和 * (矩阵乘法) 运算。

    Attributes:
        data: 二维列表表示的矩阵数据。
    """

    def __init__(self, data: List[List[Number]]) -> None:
        self._validate(data)
        self.data = [row[:] for row in data]

    @staticmethod
    def _validate(data: List[List[Number]]) -> None:
        """校验矩阵数据的合法性。"""
        if not data or not data[0]:
            raise ValueError("矩阵不能为空")
        width = len(data[0])
        for row in data:
            if len(row) != width:
                raise ValueError(
                    "矩阵必须是矩形的: 每一行的列数必须相同"
                )
            for value in row:
                if not isinstance(value, (int, float)):
                    raise TypeError(
                        f"矩阵元素必须是数字, 收到 {type(value).__name__}: {value}"
                    )

    @property
    def shape(self) -> tuple:
        """矩阵维度 (rows, cols)。"""
        return (len(self.data), len(self.data[0]))

    @property
    def rows(self) -> int:
        return self.shape[0]

    @property
    def cols(self) -> int:
        return self.shape[1]

    def __add__(self, other: "Matrix") -> "Matrix":
        if self.shape != other.shape:
            raise ValueError(
                f"矩阵加法需要相同维度, 收到 {self.shape} 与 {other.shape}"
            )
        result = [
            [a + b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(self.data, other.data)
        ]
        return Matrix(result)

    def __mul__(self, other: "Matrix") -> "Matrix":
        if self.cols != other.rows:
            raise ValueError(
                f"矩阵乘法要求左矩阵列数等于右矩阵行数, "
                f"收到 {self.shape} 与 {other.shape}"
            )
        result = []
        other_t = list(zip(*other.data))
        for row in self.data:
            result.append(
                [sum(a * b for a, b in zip(row, col)) for col in other_t]
            )
        return Matrix(result)

    def __str__(self) -> str:
        """将矩阵渲染为美观的多行字符串。"""
        rows = [[self._fmt(v) for v in row] for row in self.data]
        col_widths = [
            max(len(row[i]) for row in rows) for i in range(self.cols)
        ]
        lines = []
        for i, row in enumerate(rows):
            cells = "  ".join(
                cell.rjust(width) for cell, width in zip(row, col_widths)
            )
            brace = "┌" if i == 0 else ("└" if i == self.rows - 1 else "│")
            close = "┐" if i == 0 else ("┘" if i == self.rows - 1 else "│")
            lines.append(f"{brace} {cells} {close}")
        return "\n".join(lines)

    @staticmethod
    def _fmt(value: Number) -> str:
        """格式化单个数值: 整数原样输出, 浮点数最多 4 位小数。"""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        if isinstance(value, float):
            return f"{value:.4g}"
        return str(value)

    def __repr__(self) -> str:
        inner = ", ".join(repr(row) for row in self.data)
        return f"Matrix([{inner}])"