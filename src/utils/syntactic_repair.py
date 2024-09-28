import javalang
import re
import subprocess
import tempfile
import os


class SyntacticRepair:
    def __init__(self, java_code):
        self.java_code = java_code

    @staticmethod
    def is_syntactic_correct(code) -> bool:
        """
        判断给定的代码是否语法正确。
        参数:
        code (str): 需要进行语法检查的代码字符串。
        返回:
        bool: 如果代码语法正确，则返回True；否则返回False。
        """
        try:
            javalang.parse.parse(code)
            return True
        except Exception as e:
            return False

    def compile_java_code(self):
        # 创建临时文件来保存 Java 代码
        with tempfile.NamedTemporaryFile(suffix='.java', delete=False) as java_file:
            java_file.write(self.java_code.encode())
            java_file_path = java_file.name

        # 使用 subprocess.run 编译 Java 代码
        compile_process = subprocess.run(
            ['javac', java_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 检查返回码来判断编译是否成功
        if compile_process.returncode == 0:
            print("编译成功")
        else:
            print("编译失败")
            print("错误信息:")
            print(compile_process.stderr.decode())

        # 删除临时文件
        os.remove(java_file_path)

    def structure_repair(self):
        if self.is_syntactic_correct(self.java_code):
            return self.java_code
        else:
            stop_point = [";", "}", "{", " "]  # 停止符
            code = ""
            for i in range(len(self.java_code) - 1, -1, -1):
                # print(code[i])
                if self.java_code[i] in stop_point:
                    code = self.java_code[:i + 1]
                    break
            # 检查大括号完整性
            left_bracket = code.count("{")
            right_bracket = code.count("}")
            for idx in range(left_bracket - right_bracket):
                code += "}\n"
            if self.is_syntactic_correct(code):
                self.java_code = code
                return code
            else:
                matches = list(re.finditer(r"(?<=\})[^\}]+(?=@)", code))
                if matches:
                    code = code[:matches[-1].start() + 1]
                    left_count = code.count("{")
                    right_count = code.count("}")
                    for _ in range(left_count - right_count):
                        code += "\n}"
                if self.is_syntactic_correct(code):
                    self.java_code = code
                    return self.java_code
                else:
                    return self.java_code

    def package_repair(self, package_info):
        """
        Repair package declaration in test.
        """
        first_line = self.java_code.split('import')[0]
        if package_info == '' or package_info in first_line:
            return self.java_code
        else:
            code_package = "package" + " " + package_info + ";" + "\n" + self.java_code
            self.java_code = code_package
            return code_package

    def repair_imports(self, imports):
        import_list = imports.split('\n')
        first_line, _code = self.java_code.split('\n', 1)
        for _import in reversed(import_list):
            if _import not in self.java_code:
                _code = _import + "\n" + _code
        return first_line + '\n' + _code

    def remove_code_block(self):
        # 正则表达式匹配 ```java 和 ```，并替换为空
        cleaned_text = re.sub(r"```java\n|```|'", "", self.java_code)
        self.java_code = cleaned_text
        return cleaned_text

    def class_name_repair(self, new_class_name):
        class_pattern = re.compile(r'public\s+class\s+(\w+)')
        match = class_pattern.search(self.java_code)
        class_name_re = match.group(1)
        tree = javalang.parse.parse(self.java_code)

        class_name_javalang = ""
        java_code_new = ""
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            class_name_javalang = node.name

        if new_class_name != class_name_javalang or new_class_name == class_name_re:
            java_code_new = re.sub(class_name_javalang, new_class_name, self.java_code)
            self.java_code = java_code_new
        else:
            java_code_new = self.java_code

        return java_code_new


if __name__ == '__main__':
    code_raw = """package net.mooctest;
import static org.junit.Assert.*;
import org.junit.Test;

public class DayTest1 {
    @Test
    public void testIncrement() {
        // Original behavior: currentPos incremented and <= month size
        Day day = new Day(1, new Month());
        assertTrue(day.increment());

        // Mutant behavior: currentPos incremented and < month size
        Day mutantDay = new Day(1, new Month());
        assertTrue(mutantDay.increment()); // This assertion should fail to kill the mutant
    }
}
"""

    syntacticRepair = SyntacticRepair(code_raw)
    is_syntactic_correct = SyntacticRepair.is_syntactic_correct(code_raw)
    print(is_syntactic_correct)
    syntacticRepair.compile_java_code()
    code_new = syntacticRepair.structure_repair()
    print(code_new)
    code_new = syntacticRepair.class_name_repair("class")
    print(code_new)
    code_new = syntacticRepair.package_repair("package")
    print(code_new)
