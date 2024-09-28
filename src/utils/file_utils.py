import os


def search_file_by_name(folder_path, file_name):
    for root, dirs, files in os.walk(folder_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            # print(f'找到文件: {file_path}')
            return file_path

    else:
        # print(f'未找到文件: {file_name}')
        return None


def search_pros_in_folder(directory) -> list:
    # 获取目录下的所有文件和子目录名称列表
    file_list = os.listdir(directory)

    # 筛选出子目录并获取其完整路径
    subdirectories = [os.path.join(directory, item) for item in file_list if
                      os.path.isdir(os.path.join(directory, item))]
    return subdirectories
    # # 打印子目录的完整路径
    # for subdirectory in subdirectories:
    #     print(subdirectory)


def search_java_files(folder_path):
    java_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


if __name__ == '__main__':
    print(os.listdir(r"C:\YGL\Projects\CodeParse\projUT\Nextday_1523352132921\target\mutants"))

