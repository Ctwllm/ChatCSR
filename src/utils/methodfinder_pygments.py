import javalang
from javalang.tree import MethodDeclaration

"""
Get methods with javalang
* abandoned
"""

with open("../source_proj/Test.java", "r") as f:
    java_code = f.read()
# java_code = """
# package net.mooctest;
# import com.sta.aaa;
# import com.sta.bbb;
# public class Main {
# 	private String s;
# }
# """

tree = javalang.parse.parse(java_code)
print("tree:\n", tree)
for i in range(len(tree.children)):
    print(f"tree.children[{i}]:\n", tree.children[i])

for i in range(len(tree.children[2])):
    print(f"child{i}:\n", tree.children[2][i])

for _, node in tree.filter(MethodDeclaration):
    if node.name == 'isTriangle':
        # 打印方法名称
        print(f"Method name: {node.name}")
        # 打印方法代码
        method_code = java_code[node.position[0] - 1:node.position[1]]
        print(node.position[0])
        print(node.position[1])
        print(java_code[node.position[1]])
        print("Method code:")
        print(method_code)
        break
