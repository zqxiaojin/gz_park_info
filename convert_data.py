# coding:utf-8   #字符集编码设置成UTF-8



import os
from datetime import datetime
import csv


lastNum = 0

#如果返回false，那么就是下一个obj
def parseObj(obj, text):
    global lastNum
    if '车位数一样，不播报' in text:
        num = lastNum
        obj['num'] = num
        print("分析到一个数量：{0}\n".format(num))

        return False

    # 日期判断, example 2022年03月24日 08:30:00
    dateStrKeywords = ['年','月','日']
    hasDate = False
    containNumStr = ''
    for key in dateStrKeywords:
        if key not in text:
            break
        else :
            hasDate = True
    if hasDate:
        # 先尝试转成日期 
        if '\\n' in text: ## 看看是不是右边这种格式: # 2022年03月11日 08:50:00 \n剩余停车位数： 78
            strList = text.split('\\n')
            dateStr = strList[0]
            containNumStr = strList[1]
        else :
            dateStr = text
        if '}' in text:
            strList = text.split('}')
            dateStr = strList[1]


        tmp = datetime.strptime(dateStr, '%Y年%m月%d日 %H:%M:%S\n')
        if 'date' in obj:
            if tmp != obj['date']: # 日期不一样可能是异常
                print(text)
                print("已经有了日期，又有日期？")
        else: 
            obj['date'] = tmp
            print("分析到一个日期：{0}".format(tmp))
    else:
        containNumStr = text
    if len(containNumStr) > 0 and '{' not in containNumStr :
        colonKey = [':' , '：']
        colon = ''
        for key in colonKey:
            if key in containNumStr:
                colon = key
                break
        if len(colon) > 0:
            numStr = containNumStr.split(colon)[1]
            num = int(numStr)
            obj['num'] = num
            lastNum = num
            print("分析到一个数量：{0}\n".format(num))

            return False



    return True

def parseFile(filePath):
    objList = []
    with open(filePath, 'rt') as f:
        obj = {}
        while True:
            text = f.readline()
            if not text:
                break
            res = parseObj(obj, text)
            if not res :
                objList.append(obj)
                obj = {}
    return objList

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
    # 格式化
    obj = parseFile(filePath)
    fileObjList.extend(obj)
    
print(fileObjList)
# 写入

with open('./history.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write('\ufeff')

    cvswriter = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
    # spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    cvswriter.writerow(['时间', '车位数'])
    for obj in fileObjList:
        cvswriter.writerow([obj['date'], obj['num']])


