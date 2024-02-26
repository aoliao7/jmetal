import ast

with open("finalvariables.txt", "r") as file:
    data_str = file.read().strip()  # 读取文件内容并去除可能的空白字符

# 使用ast.literal_eval安全地将字符串形式的列表转换为Python列表
data_list = ast.literal_eval(data_str)

with open("dict.txt", "r") as file:
    # 读取文件内容
    content = file.read()

    # 使用 eval() 函数解析文件内容为字典对象
    my_dict = eval(content)
items_list = list(my_dict.items())
second_key_value_pair = items_list[1]

# 获取第二个键值对的键和值
second_key = items_list[1][0]
second_value = items_list[1][1]
print("第二个键：", second_key)
print("第二个值：", second_value)
print(my_dict["f97e0f7406e84f0e9ff95f958ec1a340"])
