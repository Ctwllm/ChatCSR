import re
import sys



"""
使用正则匹配提取java方法，缺点只能提取方法，无法深入分析
"""

class MethodParse:
    def __init__(self, codefilepath):
        try:
            with open(codefilepath, 'r') as codefile:
                self.code = codefile.read()
        except FileNotFoundError:
            print("File not found")
            sys.exit()

    def get_methods(self):
        # methods = re.findall(r"(?<=\n)(?P<method>def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([a-zA-Z0-9_]*\)\s*:)", self.code)
        method_pattern = re.compile(
            r'(?s)(public\s+\w+\s+\w+\s*\(.*?\)\s*{.*?})'  # 匹配方法签名和正文
        )
        # 查找所有匹配的方法
        methods = method_pattern.findall(self.code)

        # 打印出每个方法的代码
        for i, method in enumerate(methods, start=1):
            print(f"Method {i}:")
            print(method)
            print("\n---\n")


if __name__ == '__main__':
    codepath = r"C:\Users\dell\Desktop\Triangle\Triangle\src\main\java\net\mooctest\Triangle.java"
    m = MethodParse(codepath)
    m.get_methods()
