import openai

def translate_text(text,  model='gpt-3.5-turbo'):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Translate English latex text about plasma physics to Chinese latex text.Do not translate person's name.Be faithful or accurate in translation. Make the translation readable or intelligible. Be elegant or natural in translation.Do not add any additional text in the translation. Ensure that all percentage signs (%) are properly escaped"},
        #添加专有名词的翻译词典
        {"role": "system", "content": "- last closed surface:最外闭合磁面 "},
        {"role": "system", "content": "- kinetic:动理学 "},


        {"role": "user", "content": f" The text to be translated is:'{text}'\n"}
    	]
    )
    
    translation = response.choices[0].message.content.strip()
    return translation

def translate_abstract(tex_file):
    st = r'\begin{abstract}'
    print('Translate abstract')
    for line_idx, line in enumerate(tex_file):
        if st in line:
            abstract_idx = line_idx+1
            break
    abstract_en = tex_file[abstract_idx]
    abstract_ch = translate_text(abstract_en)+'\n'
    tex_file[abstract_idx] = abstract_ch

    return tex_file

def translate_body(tex_file):
    st0 = r'\maketitle'
    st1 = r'\section'
    st2 = r'{References}'
    sx1 = r'{figure}'
    sx2 = r'{equation}'
    sx3 = r'{table}'
    
    print('Translate main body')

    for line_idx, line in enumerate(tex_file):
        if st0 in line:
            start_idx = line_idx+1
        if st2 in line:
            end_idx = line_idx-1
            break
    
    flag = True
    L = end_idx-start_idx+1
    for line_idx in range(start_idx,end_idx):
        line = tex_file[line_idx]
        print(line_idx-start_idx+1,'/',L)
        if sx1 in line or sx2 in line or sx3 in line:
            flag = not flag
            continue
        if flag and len(line)>2:
            line_ch = translate_text(line)+'\n'
            tex_file[line_idx] = line_ch

    return tex_file