import translate_func as tf
import openai

try:
    # 打开文件并读取内容
    with open('filename.txt', 'r') as file:
        content = file.readline()
        
    # 检查内容是否为空
    if not content:
        raise ValueError("no filename")

    # 打印读取的内容
    print('filename:',content)

except FileNotFoundError:
    print("filename.txt not exist")
    print("failed to run")
    # 终止程序
    raise SystemExit

except ValueError as e:
    print('no filename in filename.txt')
    print("failed to run")
    # 终止程序
    raise SystemExit

try:
    # 打开文件并读取内容
    with open('chatgpt-api-key.txt', 'r') as file:
        key = file.readline()
        openai.api_key = key
    # 检查内容是否为空
    if not key:
        raise ValueError("no chatgpt-api-key")

    # 打印读取的内容
    print('chatgpt-api-key:',key)

except FileNotFoundError:
    print("chatgpt-api-key.txt not exist")
    print("failed to run")
    # 终止程序
    raise SystemExit

except ValueError as e:
    print('no chatgpt-api-key in chatgpt-api-key.txt')
    print("failed to run")
    # 终止程序
    raise SystemExit

input_file_path = 'tex_file/typeset.tex'
output_file_path = 'tex_file/translate.tex'

with open(input_file_path, 'r',encoding='utf-8') as file_2:
    tex_2 = file_2.readlines()

tex_3 = tex_2.copy()
tex_3 = tf.translate_abstract(tex_3)
tex_3 = tf.translate_body(tex_3)

with open(output_file_path, 'w',encoding='utf-8') as file_3:
     file_3.write(' '.join(tex_3))