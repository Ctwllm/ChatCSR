import os.path

from utils import parse_result_process
from utils import file_utils
from utils.log import logger

from src.test_generation.test_gen import gen_tests_for_all_mutants_from_llm


def main(projects_base: str):

    #  combine ast and calls for all projects in the base folder
    print("=======================================\n"
          "Start Combining\n"
          "=======================================\n")
    logger.info("=======================================Start Combining=======================================")
    projects_dir = file_utils.search_pros_in_folder(projects_base)
    print("projects_dir: ", projects_dir)
    for project_dir in projects_dir:
        print("Combining ast and calls for project {}".format(os.path.split(project_dir)[1]))
        logger.info("Combining ast and calls for project {}".format(os.path.split(project_dir)[1]))
        parse_result_process.combine_ast_calls_for_all(project_dir)

    #  generate tests based on mutants
    print("=======================================\n"
          "Start Generating Tests\n"
          "=======================================\n")
    logger.info("=======================================Start Generating Tests=======================================")
    for project_dir in projects_dir:
        gen_tests_for_all_mutants_from_llm(project_dir)


if __name__ == '__main__':
    projects_base_dir = r"C:\Users\dell\Desktop\projects"
    main(projects_base_dir)


