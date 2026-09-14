"""演示脚本: 直接运行 python main.py"""

from src.matrix import Matrix


def main() -> None:
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])

    print("A + B:")
    print(a + b, end="\n\n")
    print("A × B:")
    print(a * b)


if __name__ == "__main__":
    main()