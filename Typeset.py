import latex_func as lf

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

input_file_path = 'tex_file/'+content+'.tex'
template_file_path = 'tex_file/template.tex'
typeset_file_path = 'tex_file/typeset.tex'

with open(input_file_path, 'r') as file_0:
    tex_0 = file_0.readlines()
with open(template_file_path, 'r',encoding='utf-8') as file_1:
    tex_1 = file_1.readlines()

format_figure = lf.get_format_figure(tex_1)
format_equation = lf.get_format_equation(tex_1)
format_table = lf.get_format_table(tex_1)

tex_2 = lf.create_new_tex(tex_1)
tex_2 = lf.modify_title(tex_0,tex_2)
tex_2 = lf.modify_abstract(tex_0,tex_2)
tex_2 = lf.modify_body(tex_0,tex_2)
tex_2 = lf.modify_references(tex_0,tex_2)

tex_2 = lf.modify_equation(tex_2,format_equation)
tex_2 = lf.modify_figure(tex_2,format_figure)
tex_2 = lf.modify_table(tex_2,format_table)
tex_2 = lf.modify_stitch(tex_2)

with open(typeset_file_path, 'w',encoding='utf-8') as file_2:
     file_2.write(' '.join(tex_2))
