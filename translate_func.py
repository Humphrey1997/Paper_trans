import openai
import time
import random

# define a retry decorator
def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 5,
    errors: tuple = (openai.error,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specified errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper

@retry_with_exponential_backoff
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def translate_text(text):
    response = completions_with_backoff(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Translate English latex text about plasma physics to Chinese latex text.Do not translate person's name.Be faithful or accurate in translation. Make the translation readable or intelligible. Be elegant or natural in translation.Do not add any additional text in the translation. Ensure that all percentage signs (%) are properly escaped"},
        #添加专有名词的翻译词典
        {"role": "system", "content": "- last closed surface:最外闭合磁面 "},
        {"role": "system", "content": "- kinetic:动理学 "},

        {"role": "user", "content": f" The text to be translated is:'{text}'\n"},
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
    sx1 = r'\begin'
    sx2 = r'\end'
    
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
        if sx1 in line or sx2 in line:
            flag = not flag
            continue
        if flag and len(line)>2:
            line_ch = translate_text(line)+'\n'
            tex_file[line_idx] = line_ch

    return tex_file