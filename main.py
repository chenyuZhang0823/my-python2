from src.matrix import Matrix


def input_matrix(name: str) -> Matrix:
    """从标准输入读取一个矩阵。"""
    while True:
        try:
            rows = int(input(f"请输入矩阵 {name} 的行数: "))
            cols = int(input(f"请输入矩阵 {name} 的列数: "))
            if rows <= 0 or cols <= 0:
                print("行数和列数必须是正整数，请重新输入。")
                continue
            break
        except ValueError:
            print("请输入有效的整数。")

    print(f"请逐行输入矩阵 {name} 的元素（每行 {cols} 个数，用空格分隔）：")
    data = []
    for i in range(rows):
        while True:
            line = input(f"第 {i + 1} 行: ").strip()
            parts = line.split()
            if len(parts) != cols:
                print(f"本行需要 {cols} 个数，请重新输入。")
                continue
            try:
                row = [float(x) if "." in x or "e" in x.lower() else int(x) for x in parts]
            except ValueError:
                print("输入包含非数字，请重新输入。")
                continue
            data.append(row)
            break

    return Matrix(data)


def main() -> None:
    print("=== 矩阵加法与乘法 ===")
    a = input_matrix("A")
    b = input_matrix("B")

    print("\nA + B:")
    try:
        print(a + b, end="\n\n")
    except Exception as e:
        print(f"无法相加: {e}\n")

    print("A × B:")
    try:
        print(a * b)
    except Exception as e:
        print(f"无法相乘: {e}")


if __name__ == "__main__":
    main()