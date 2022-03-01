# coding:utf-8   #字符集编码设置成UTF-8
import time

import urllib.request
import urllib.parse

import json  # 导入依赖库


def printOnce():

    park_url = "https://www.tcc.jtj.gz.gov.cn/api/services/app/ParkingDataAccess/ParkingDataAccessType2Public/GetListDataRecordLatest?dataProviderId=2021-06-11T05_34_59.4360096Z_C9E578F0"

    r = urllib.request.urlopen(park_url)

    info = json.loads(r.read().decode('utf-8'))

    park_space = info["result"][0]['norps']

    text = "剩余停车位数：{}".format(park_space)

    nowtime = time.localtime()
    time_str = time.strftime("%Y{}%m{}%d{} %H:%M:%S",
                             nowtime).format("年", "月", "日")  # 占位符别忘了
    output_str = time_str + " " + text
    print(output_str)

    headers = {'Content-Type': 'application/json'}  # 定义数据类型
    # 定义webhook，从钉钉群机器人设置页面复制获得
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token='
    # 定义要发送的数据
    data = {
        "msgtype": "text",
        "text": {"content": output_str},
    }
    
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')

    req = urllib.request.Request(url=webhook, data=jsondataasbytes, headers=headers)

    urllib.request.urlopen(req)
    return


printOnce()
