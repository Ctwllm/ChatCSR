import json
import os.path
from src.utils import file_utils

"""
将JavaParser解析得到的结果进行合并
"""
def combine_ast_calls(ast_file_path: str, method_calls_file_path: str, combine_file_path: str):
    with open(ast_file_path, "r") as code_file:
        ast_datas = json.load(code_file)
    with open(method_calls_file_path, "r") as method_calls_file:
        method_calls = json.load(method_calls_file)

    for i in range(len(ast_datas)):
        if "callee" not in ast_datas[i]:
            for method_call in method_calls:
                if method_call["callerName"] == ast_datas[i]["name"] and method_call["signature"] == ast_datas[i]["signature"]:
                    ast_datas[i]["callee"]= method_call["methodCalls"]


    # with open(combine_file_path, "w", encoding='utf-8') as file:
    #     json.dump(ast_datas, file, ensure_ascii=False, indent=4)

    jsonDir = os.path.dirname(combine_file_path)
    if not os.path.exists(jsonDir):
        os.makedirs(jsonDir)
    with open(combine_file_path, 'w', encoding='utf-8') as file:
        json.dump(ast_datas, file)


    # print("combined_ast_datas: ", ast_datas)
    return ast_datas


def combine_ast_calls_for_all(project_dir: str):
    ast_datas_dir = os.path.join(project_dir, "target", "parsefiles", "ast_json")
    print("project_dir: ", project_dir)
    print("ast_datas_dir: ", ast_datas_dir)
    method_calls_dir = os.path.join(project_dir, "target", "parsefiles", "method_call")
    combine_result_dir = os.path.join(project_dir, "target", "parsefiles", "combined_result")
    if not os.path.exists(combine_result_dir):
        os.makedirs(combine_result_dir)
    for file in os.listdir(ast_datas_dir):
        file_name = os.path.basename(file)
        class_name, file_extension = os.path.splitext(file)
        method_call_file_path = file_utils.search_file_by_name(method_calls_dir, file_name)
        ast_data_file_path = os.path.join(ast_datas_dir, file_name)
        combined_result_file_path = os.path.join(combine_result_dir, file_name)
        if method_call_file_path is not None:
            combine_ast_calls(ast_data_file_path, method_call_file_path, combined_result_file_path)


if __name__ == '__main__':
    ast_path = r"C:\YGL\Projects\pythonProject\MutationTestGEN-LLM\projUT\BPlusTree_1509184036737\target\parsefiles\ast_json\Node.json"
    method_calls_path = r"C:\YGL\Projects\pythonProject\MutationTestGEN-LLM\projUT\BPlusTree_1509184036737\target\parsefiles\method_call\Node.json"
    combine_parse_path = r"C:\YGL\Projects\pythonProject\MutationTestGEN-LLM\projUT\BPlusTree_1509184036737\target\parsefiles\combined_result\Node.json"
    combine_ast_calls(ast_path, method_calls_path, combine_parse_path)
