import easygui
from clc99 import *
import sys
import pdfplumber
import re
import pyperclip

def process_complete_vocabulary(text_list):
    vocabulary = []
    
    # 匹配模式：允许字母、空格、中文、特殊符号等
    pattern = r'(\d+)\.\s+([^\.\d].*?)(?=\s+\d+\.|$)'
    
    for line in text_list:
        matches = re.findall(pattern, line)
        for num, content in matches:
            content = content.strip()
            vocabulary.append((int(num), content))
    
    # 排序并重新编号
    vocabulary.sort(key=lambda x: x[0])
    return vocabulary

def clear_invaild_chars(wordlist: list):
    cleaned_list = []
    for word in wordlist:
        cleaned_word = re.sub(r'[^a-zA-Z\s\.,;\'\"-]', '', word)
        cleaned_list.append(cleaned_word.strip())
    return cleaned_list

print_admin("欢迎使用99关于曲老师课外词单的英语单词百词斩词单生成工具！")

p = easygui.fileopenbox(msg="选择一个PDF文件", title="99英语单词百词斩词单生成", default="*.pdf", filetypes=["*.pdf"])

if p == None:
    print_warning("没有选择文件，退出程序！")
    sys.exit()
with pdfplumber.open(p) as pdf:
    english_page = pdf.pages[1]
    data = english_page.extract_text(
        x_tolerance=1,
    )
    
    data = data.split("\n")
    data = process_complete_vocabulary(data)
    data = clear_invaild_chars([item[1] for item in data])

    print_good("找到了{}个单词和短语！".format(len(data)))
    print_status("正在生成百词斩格式的单词列表，请稍候...")

    data = ",".join(data)

    pyperclip.copy(data)

    print_good("已写入剪贴板！")