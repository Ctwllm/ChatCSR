import os
import json
import xml.etree.ElementTree as ET
import javalang.parse

from src.llm.llm import ask_llm
from src.utils import file_utils
from src.utils.log import logger

# test_gen_prompt = f"""
# You are a test generator.
# You are given a piece of code and a package name.
# You need to generate a test for the code.
# You need to generate a test for the code."""


def count_mutants(project_dir: str):
    """
    Count the number of mutants in the project.
    :param project_dir: The directory of the project.
    :return: The number of mutants.
    """
    count = []
    for item in os.listdir(os.path.join(project_dir, "target", "mutants")):
        item_path = os.path.join(os.path.join(project_dir, "target", "mutants"), item)
        if os.path.isdir(item_path):
            count.append(item)
    return count


def get_package_name(project_dir: str, class_name: str, method_name: str, method="javalang"):
    if method == "javalang":
        source_file_path = get_source_file_path(project_dir, class_name)
        with open(source_file_path, "r", encoding="utf-8") as file:
            source_code = file.read()
        code_tree = javalang.parse.parse(source_code)
        package_name = code_tree.package.name

        return package_name

    else:
        get_borders_objects = {}
        combined_parse_result_file_path = os.path.join(project_dir, "target", "parsefiles", "combined_result",
                                                       class_name + ".json")
        try:
            # 打开并读取JSON文件
            with open(combined_parse_result_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # 遍历数据，查找'name'为'getBorders'的JSON对象
            for obj in data:
                if obj.get('name') == method_name:
                    get_borders_objects = obj
                    break
                else:
                    continue
            # get_borders_objects = obj for obj in data if obj.get('name') == method_name
            package_name = get_borders_objects.get('packageName')
        except FileNotFoundError:
            print("File not found: " + combined_parse_result_file_path)
            logger.error("File not found: " + combined_parse_result_file_path)
            return None
        # except Exception as e:
        #     print("Error:", e)
        #     logger.error("Error:", e)
        #     return None
        return package_name


def get_class_name(project_dir: str, mutant_number: str):
    print(file_utils.search_java_files(os.path.join(project_dir, "target", "mutants", mutant_number)))
    class_java_file_path = file_utils.search_java_files(os.path.join(project_dir, "target", "mutants", mutant_number))[
        0]
    try:
        class_name = os.path.basename(class_java_file_path).split('.')[0]
    except FileNotFoundError:
        print("File not found: " + class_java_file_path)
        logger.error("File not found: " + class_java_file_path)
        return None
    # except Exception as e:
    #     print("Error:", e)
    #     logger.error("Error:", e)
    #     return None
    return class_name


def get_method_name(project_dir: str, mutant_number: str, class_name: str):
    mutant_class_file_path = os.path.join(project_dir, "target", "mutants", mutant_number, class_name + ".json")
    try:
        with open(mutant_class_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            method_name = data.get("mutant_method_name")
    except FileNotFoundError:
        print("File not found: " + mutant_class_file_path)
        logger.error("File not found: " + mutant_class_file_path)
        return None
    # except Exception as e:
    #     print("Error:", e)
    #     logger.error("Error:", e)
    #     return None
    return method_name


def get_ori_class_code(project_dir: str, class_name: str):
    ori_class_code_file_path = file_utils.search_file_by_name(os.path.join(project_dir, "target", "classes"),
                                                              class_name + ".java")
    try:
        with open(ori_class_code_file_path, 'r', encoding='utf-8') as file:
            ori_class_code = file.read()
    except FileNotFoundError:
        print("File not found: " + ori_class_code_file_path)
        logger.error("File not found: " + ori_class_code_file_path)
        return None
    # except Exception as e:
    #     print("Error:", e)
    #     logger.error("Error:", e)
    #     return None
    return ori_class_code


def get_ori_method_code(project_dir: str, mutant_number: str, class_name: str):
    mutant_class_file_path = os.path.join(project_dir, "target", "mutants", mutant_number, class_name + ".json")
    try:
        with open(mutant_class_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        ori_method_code = data.get("method_original_code")
    except FileNotFoundError:
        print("File not found: " + mutant_class_file_path)
        logger.error("File not found: " + mutant_class_file_path)
        return None
    # except Exception as e:
    #     print("Error:", e)
    #     logger.error("Error:", e)
    #     return None
    return ori_method_code


def get_mutated_method_code(project_dir: str, mutant_number: str, class_name: str):
    mutant_class_file_path = os.path.join(project_dir, "target", "mutants", mutant_number, class_name + ".json")
    try:
        with open(mutant_class_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        mutated_method_code = data.get("method_mutated_code")
    except FileNotFoundError:
        print("File not found: " + mutant_class_file_path)
        logger.error("File not found: " + mutant_class_file_path)
        return None
    # except Exception as e:
    #     print("Error:", e)
    #     logger.error("Error:", e)
    #     return None
    return mutated_method_code


def get_method_signature(project_dir: str, class_name: str, method_name: str):
    get_borders_objects = {}
    combined_parse_result_file_path = os.path.join(project_dir, "target", "parsefiles", "combined_result",
                                                   class_name + ".json")
    try:
        # 打开并读取JSON文件
        with open(combined_parse_result_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 遍历数据，查找'name'为'getBorders'的JSON对象
        for obj in data:
            if obj.get('name') == method_name:
                get_borders_objects = obj
                break
            else:
                continue
        # get_borders_objects = obj for obj in data if obj.get('name') == method_name
        signature = get_borders_objects.get('signature')
    except FileNotFoundError:
        print("File not found: " + combined_parse_result_file_path)
        logger.error("File not found: " + combined_parse_result_file_path)
        return None
    # except Exception as e:
    #     print("Error:", e)
    #     logger.error("Error:", e)
    #     return None
    return signature


def get_callee_methods_signatures(project_dir: str, class_name: str, method_name: str):
    get_borders_objects = {}
    combined_parse_result_file_path = os.path.join(project_dir, "target", "parsefiles", "combined_result",
                                                   class_name + ".json")
    signatures = []

    try:
        # 打开并读取JSON文件
        with open(combined_parse_result_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 遍历数据，查找'name'为'getBorders'的JSON对象
        for obj in data:
            if obj.get('name') == method_name:
                get_borders_objects = obj
                break
            else:
                continue
        for o in get_borders_objects.get("callee"):
            signatures.append(o.get("signature"))
    except FileNotFoundError:
        print("File not found: " + combined_parse_result_file_path)
        logger.error("File not found: " + combined_parse_result_file_path)
        return None
    # except Exception as e:
    #     print("Error:", e)
    #     logger.error("Error:", e)
    #     return None
    return signatures


def get_source_directory(maven_project_path):
    """
    解析Maven项目的pom.xml文件来查找源代码目录的位置
    :param maven_project_path:
    :return:
    """
    pom_path = os.path.join(maven_project_path, 'pom.xml')
    tree = ET.parse(pom_path)
    root = tree.getroot()
    namespace = {'m': 'http://maven.apache.org/POM/4.0.0'}
    build_element = root.find('m:build', namespace)
    source_directory = None
    if build_element is not None:
        source_directory_element = build_element.find('m:sourceDirectory', namespace)
        if source_directory_element is not None:
            source_directory = source_directory_element.text
    return source_directory if source_directory else 'src/main/java'


def get_source_file_path(maven_project_path, class_name):
    """
    get the path of the source file by class name
    :param maven_project_ path:
    :param class_name:
    :return:
    """
    source_directory = get_source_directory(maven_project_path)
    full_source_path = os.path.join(maven_project_path, source_directory)
    class_name = class_name.replace('.', '/') + '.java'
    for root, dirs, files in os.walk(full_source_path):
        if class_name in files:
            return os.path.join(root, class_name)
    return None

#
# class_name = "Triangle"
#
# method_name = "diffOfBorders"
#
# class_original_code = """
# package net.mooctest;
#
# public class Triangle {
#    protected long lborderA = 0L;
#    protected long lborderB = 0L;
#    protected long lborderC = 0L;
#    public static int t = 0;
#
#    public Triangle(long lborderA, long lborderB, long lborderC) {
#       this.lborderA = lborderA;
#       this.lborderB = lborderB;
#       this.lborderC = lborderC;
#    }
#
#    public boolean isTriangle(Triangle triangle) {
#       boolean isTriangle = false;
#       if (triangle.lborderA > 0L && triangle.lborderA <= Long.MAX_VALUE && triangle.lborderB > 0L && triangle.lborderB <= Long.MAX_VALUE && triangle.lborderC > 0L && triangle.lborderC <= Long.MAX_VALUE && this.diffOfBorders(triangle.lborderA, triangle.lborderB) < triangle.lborderC && this.diffOfBorders(triangle.lborderB, triangle.lborderC) < triangle.lborderA && this.diffOfBorders(triangle.lborderC, triangle.lborderA) < triangle.lborderB) {
#          isTriangle = true;
#          ++t;
#       }
#
#       return isTriangle;
#    }
#
#    public String getType(Triangle triangle) {
#       String strType = "Illegal";
#       if (this.isTriangle(triangle)) {
#          if (triangle.lborderA == triangle.lborderB && triangle.lborderB == triangle.lborderC) {
#             strType = "Regular";
#          } else if (triangle.lborderA != triangle.lborderB && triangle.lborderB != triangle.lborderC && triangle.lborderA != triangle.lborderC) {
#             strType = "Scalene";
#          } else {
#             strType = "Isosceles";
#          }
#       }
#
#       return strType;
#    }
#
#    public long diffOfBorders(long a, long b) {
#       return a > b ? a - b : b - a;
#    }
#
#    public long[] getBorders() {
#       long[] borders = new long[]{this.lborderA, this.lborderB, this.lborderC};
#       return borders;
#    }
# }
#
# """
#
# method_original_code = "public long diffOfBorders(long a, long b) {\r\n    return a > b ? a - b : b - a;\r\n}"
#
# method_mutated_code = """
# public long diffOfBorders(long a, long b) {
#     return a >= b ? a - b : b - a;
# }"""
# method_signature = "public long diffOfBorders(long a, long b)"
#
# callee_signature = ""
#
#
#
#
# short_message = f"""
#
# """


def gen_one_test_from_llm(
        method_name,
        method_signature,
        class_name,
        class_original_code,
        method_original_code,
        method_mutated_code,
        callee_signatures,
        mutant_number,
        project_dir
):
    long_message = f"""
    1.The name of mutated method is {method_name}, whose signature is {method_signature}, from class {class_name}.
    2.The original complete codes of the class to which this method belongs are {class_original_code}
    3.The original codes are {method_original_code}.
    4.After mutation testing, the codes of method{method_name} are mutated to {method_mutated_code}.
    5.The signatures of the methods called by {method_name} are {callee_signatures}.
    6.The returned message should not include the code block markers of Markdown format. Just return the pure code.
    7.The test code should be written in the following format:

    import static org.junit.Assert.*;
    import org.junit.Test;
    public class {class_name}Test{mutant_number}{{
        @Test
        public void test{method_name}() {{

        }}
    }}

    """

    package_name = get_package_name(project_dir, class_name, method_name)

    if os.name == "nt":
        package_dir = package_name.replace(".", "\\")
    else:
        package_dir = package_name.replace(".", "/")
    save_path = str(os.path.join(project_dir, "src", "test", "java", package_dir,
                                 class_name + str(mutant_number) + "Test" + ".java"))

    test_gen_result = ask_llm(long_message, package_name, save_path, max_try_times=5)
    return test_gen_result


def gen_tests_for_all_mutants_from_llm(project_dir):
    number_of_mutants = count_mutants(project_dir)
    gen_test_num = 0
    for mutant_number in number_of_mutants:
        print(f"-----Generating test for mutant {mutant_number}...")
        logger.info(f"-----Generating test for mutant {mutant_number}...")
        class_name = get_class_name(project_dir, mutant_number)
        method_name = get_method_name(project_dir, mutant_number, class_name)
        if method_name is None:
            print(f"No. {mutant_number} mutant missed.")
            logger.warning(f"No. {mutant_number} mutant missed. No test generated.")
            continue
        method_signature = get_method_signature(project_dir, class_name, method_name)
        class_original_code = get_ori_class_code(project_dir, class_name)
        method_original_code = get_ori_method_code(project_dir, mutant_number, class_name)
        method_mutated_code = get_mutated_method_code(project_dir, mutant_number, class_name)
        callee_signatures = get_callee_methods_signatures(project_dir, class_name, method_name)

        test_gen_result = gen_one_test_from_llm(method_name,
                                                method_signature,
                                                class_name,
                                                class_original_code,
                                                method_original_code,
                                                method_mutated_code,
                                                callee_signatures,
                                                mutant_number,
                                                project_dir)
        if test_gen_result:
            gen_test_num += 1
            logger.info(f"Test code for No. {mutant_number} mutant generated.")
        else:
            logger.warning(f"Test code for No. {mutant_number} mutant failed to generate.")
    print(f"Test generation finished. {gen_test_num} tests generated.")
    logger.info(f"Test generation finished. {gen_test_num} tests generated.")


if __name__ == '__main__':
    project = r"C:\Users\dell\Desktop\projects\BPlusTree_1509184036737"
    gen_tests_for_all_mutants_from_llm(project)
    # path = get_source_file_path(project, "Day")
    # print(path)
