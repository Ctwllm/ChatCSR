import subprocess
import sys


def run_jar(jar_path: str, projects_base: str):
    cmd = ['java', '-jar', jar_path, projects_base]
    result = subprocess.run(cmd,
                            # capture_output=True,
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,)
    print(result)


# cmd = ['java', '-jar', 'src/CodeParse-1.0-SNAPSHOT-jar-with-dependencies.jar']


if __name__ == '__main__':
    jar_path = (r'C:\YGL\Projects\pythonProject\MutationTestGEN-LLM\dependencies\CodeParse-1.0-SNAPSHOT-jar-with'
                r'-dependencies.jar')
    projects_base_dir = r'C:\Users\dell\Desktop\projects'
    run_jar(jar_path, projects_base_dir)



