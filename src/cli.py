"""命令行界面入口。

用法示例:
    matrix-cli add "1,2;3,4" "5,6;7,8"
    matrix-cli mul "1,2;3,4" "5,6;7,8"
    matrix-cli show "1,2,3;4,5,6"
    matrix-cli info "1,2;3,4"
"""

import re

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .matrix import Matrix

app = typer.Typer(
    name="matrix-cli",
    help="矩阵运算命令行工具 ⚡",
    no_args_is_help=True,
    add_completion=False,
)

console = Console()


def parse_matrix(text: str) -> Matrix:
    """解析 CLI 输入的矩阵字符串。

    行与行之间用分号(;)或换行分隔,
    列与列之间用逗号(,)或空格分隔。

    示例: "1,2;3,4"  => [[1, 2], [3, 4]]
    """
    text = text.strip().replace("\\n", "\n").replace(";", "\n")
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        tokens = re.split(r"[\s,]+", line.strip())
        try:
            rows.append([int(t) if t.lstrip('-').isdigit() else float(t) for t in tokens])
        except ValueError:
            raise typer.BadParameter(
                f"无法解析数字: '{line}'", param_hint="矩阵"
            )
    if not rows:
        raise typer.BadParameter("矩阵不能为空", param_hint="矩阵")
    try:
        return Matrix(rows)
    except (ValueError, TypeError) as e:
        raise typer.BadParameter(str(e), param_hint="矩阵")


def display_matrix(title: str, matrix: Matrix) -> None:
    """以美观的表格形式展示矩阵。"""
    table = Table(
        title=title,
        show_header=False,
        title_style="bold cyan",
        box=None,
        pad_edge=False,
    )
    for _ in range(matrix.cols):
        table.add_column(justify="right")
    for row in matrix.data:
        table.add_row(*[str(v) for v in row])
    console.print(table)


@app.command()
def add(
    a: str = typer.Argument(help="矩阵 A, 如: 1,2;3,4"),
    b: str = typer.Argument(help="矩阵 B, 如: 5,6;7,8"),
) -> None:
    """矩阵加法: A + B (逐元素相加)"""
    try:
        ma, mb = parse_matrix(a), parse_matrix(b)
        result = ma + mb
    except ValueError as e:
        console.print(f"[bold red]✗[/] {e}")
        raise typer.Exit(code=1)
    console.print("  [bold]A[/] ⊞ [bold]B[/]  = ")
    display_matrix("A + B", result)


@app.command()
def mul(
    a: str = typer.Argument(help="矩阵 A, 如: 1,2,3;4,5,6"),
    b: str = typer.Argument(help="矩阵 B, 如: 1,2;3,4;5,6"),
) -> None:
    """矩阵乘法: A × B"""
    try:
        ma, mb = parse_matrix(a), parse_matrix(b)
        result = ma * mb
    except ValueError as e:
        console.print(f"[bold red]✗[/] {e}")
        raise typer.Exit(code=1)
    console.print("  [bold]A[/] ⛌ [bold]B[/]  = ")
    display_matrix("A × B", result)


@app.command()
def show(
    matrix: str = typer.Argument(help="要显示的矩阵, 如: 1,2;3,4"),
) -> None:
    """显示矩阵"""
    try:
        m = parse_matrix(matrix)
    except typer.BadParameter as e:
        console.print(f"[bold red]✗[/] {e}")
        raise typer.Exit(code=1)
    display_matrix("Matrix", m)
    console.print(f"  [dim]shape: {m.shape[0]}x{m.shape[1]}[/]")


@app.command()
def info(
    matrix: str = typer.Argument(help="要分析的矩阵, 如: 1,2;3,4"),
) -> None:
    """查看矩阵维度信息"""
    try:
        m = parse_matrix(matrix)
    except typer.BadParameter as e:
        console.print(f"[bold red]✗[/] {e}")
        raise typer.Exit(code=1)
    rows, cols = m.shape
    console.print(
        Panel.fit(
            f"[bold cyan]{rows}[/] × [bold cyan]{cols}[/]",
            title="矩阵维度",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    app()