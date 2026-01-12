from functions.run_python_file import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print("Output from executing calculator/main.py")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Output from executing calculator/main.py with args [3 + 5]")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Output from executing calculator/tests.py")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Output from executing calculator/calculator/main.py")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("Output from executing calculator/nonexistent.py")
    print(result)
    print("")

    result = run_python_file("calculator", "lorem.txt")
    print("Output from executing calculator/lorem.txt")
    print(result)
    print("")


if __name__ == "__main__":
    test()