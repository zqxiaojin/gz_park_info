# coding:utf-8   #字符集编码设置成UTF-8


import os
from datetime import datetime

def parseFile(filePath):
    date = ''
    
    with open(filePath, 'rt') as f:
        text = f.readline()
        
        # 日期判断, example 2022年03月24日 08:30:00
        dateStr = ['年','月','日']
        hasDate = False
        for key in dateStr:
            if key not in text:
                break
            else :
                hasDate = True
        if hasDate:
            # 先尝试转成日期 
            tmp = datetime.strptime(text, '%Y-%m-%d')
            print(text)

# 遍历文件夹
fileList = []
rootDir = './data'
for root,dirs,files in os.walk(rootDir):
    for file in files:#遍历文件夹
        filePath =os.path.join(root, file) #拼接目录路径
        # print(filePath)
        fileList.append(filePath)
        
fileObjList = []
# 读取文件
for filePath in fileList:
    obj = parseFile(filePath)
    fileObjList.append(obj)
    

# 格式化


# 写入
