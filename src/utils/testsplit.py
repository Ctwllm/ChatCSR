import glob
import re
import os
from openai import OpenAI
from src.llm.config import API_KEY
api_key = API_KEY
api_base = "https://hk.xty.app/v1"
client = OpenAI(api_key=api_key, base_url=api_base)


def get_test_methods(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    method_declarations = re.findall(r'(@Test\s*(?:\(.*?\))?\s*public void (\w+)\(\))', content)

    test_methods = []
    print("find method count", len(method_declarations))
    for method_declaration in method_declarations:
        method_body = method_declaration[0]
        print("find method:", method_body)
        origin_index = content.index(method_body)
        start_index = origin_index + len(method_body)
        # 继续向前查找，直到找到第一个 {
        while content[start_index] != '{':
            start_index += 1
        brace_count = 1  # got one brace
        for i in range(start_index + 1, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            if brace_count == 0:
                # find the end of the method body
                method_body = content[origin_index:i + 1]
                test_methods.append((method_body, method_declaration[1]))
                break

    # remove methods without assertions
    filtered_test_methods = [(method_name, method_body) for method_body, method_name in test_methods if
                             re.search(r'\b(?:assert\w*|assertTrue|assertFalse)\s*\(', method_body)]
    for (name, body) in filtered_test_methods:
        print("find:", name, body)
    return filtered_test_methods


def split_assertions(test_methods):
    new_test_methods = []
    for method_name, method_body in test_methods:
        # decompose the method body with OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user",
                     "content": f"""
                     You are an AI assistant for splitting code. Your task is to split a JUnit code method into several 
                     independent and runnable JUnit test unit methods. Requirements:
                     1. A test unit can only have one assertion.
                     2. If the original code has only one assertion, it does not need to be split.
                     3. Your input is a complete method.
                     4. Output several methods after the method is split.
                     5. Output without other prompts.
                     the method body is:
                     \n\n{method_body}\n\n"""}
                ],
                # response_format={ "type": "json_object" }
            )
            new_body = response.choices[0].message.content
            new_test_methods.append((method_name, new_body))
            print(f"Method '{method_name}' was successfully split into separate test units.")
        except Exception as e:
            print(f"Failed to split method '{method_name}'. Error: {str(e)}")
    return new_test_methods


def write_new_file(file_path, origin_test_methods, new_test_methods):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # create a dictionary mapping method names to bodies
    new_methods_dict = {name: body for name, body in new_test_methods}

    # replace method body with new bodies
    for method_name, old_body in origin_test_methods:
        if method_name in new_methods_dict:
            print("be replace", method_name)
            new_body = new_methods_dict[method_name]
            print("old-------------", old_body)
            print("new-------------", new_body)
            content = content.replace(old_body, new_body)

    # write the modified content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def process_directory(directory):
    test_files = glob.glob(os.path.join(directory, r'src\test\java\*\*\*.java'), recursive=True)
    print(test_files)
    for file_path in test_files:
        test_methods = get_test_methods(file_path)
        if test_methods:
            new_test_methods = split_assertions(test_methods)
            write_new_file(file_path, test_methods, new_test_methods)


# the directory to scan
directory_to_scan = r'C:\Users\dell\Desktop\BPlusTree\BPlusTree1\BPlusTree_1509180700625'
process_directory(directory_to_scan)

# if __name__ == '__main__':
#     directory = r'C:\Users\dell\Desktop\BPlusTree\BPlusTree1\BPlusTree_1509180700625'
#     print(os.path.join(directory, r'src\test\java\net\mooctest\*.java'))
#     test_files = glob.glob(os.path.join(directory, r'src\test\java\*\*\*.java'), recursive=True)
#     print(test_files)
