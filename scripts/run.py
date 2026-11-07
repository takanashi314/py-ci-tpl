from py_ci_tpl.calculator import add


def add_user_input() -> None:
    a = float(input("数値aを入力してください： "))
    b = float(input("数値bを入力してください： "))
    result = add(a, b)
    print(f"結果： {a} + {b} = {result}")


if __name__ == "__main__":
    add_user_input()
