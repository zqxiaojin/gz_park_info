#!/bin/bash

g_lastCount="0"

echoMaxCount=80      # 大于多少个位就不播
echoHourMaxCount=90 # 整点播报， 最大值

intervalSeconds=$(expr 60 \* 5)                     #播报间隔  1分钟 * N
durationTimes=$(expr 90 \* 60 / ${intervalSeconds}) # 播报次数 ， 8点半到10点，  90分钟 / M

hourCallStr='09:00'

printOnce() {

    dateStr=$(date "+%Y年%m月%d日 %H:%M:%S")

    echo ${dateStr}

    # return

    response=$(curl "https://www.tcc.jtj.gz.gov.cn/api/services/app/ParkingDataAccess/ParkingDataAccessType2Public/GetListDataRecordLatest?dataProviderId=2021-06-11T05_34_59.4360096Z_C9E578F0")

    echo
    # echo ${response}
    echo

    rightText=${response#*norps\"*:}

    restCount=${rightText%%,*}
    if [ ${restCount} -lt 0 ]; then
        restCount=0 #小于 0 ，当作是0了
    fi

    timeStr=$(date "+%H:%M")

    shouldReport=false
    msg="默认值"

    dingMsg="剩余停车位数"

    while true; do

        re='^[0-9]+$'
        if ! [[ $restCount =~ $re ]] ; then
            shouldReport=true
            dingMsg="接口返回异常，不确定未来是否能继续播报"
            break;
        fi

        if [ ${restCount} -eq ${g_lastCount} ]; then
            msg="车位数一样，不播报"
            break
        fi

        if [[ "$timeStr" == "$hourCallStr" ]]; then # 整点播报

            if [ ${restCount} -gt ${echoHourMaxCount} ]; then
                msg="整点车位太多，不播报:"${restCount}
                break
            fi

            shouldReport=true
            echo "整点播报"
            dingMsg="整点播报车位数"
            break
        fi

        if [ ${restCount} -gt ${echoMaxCount} ]; then
            msg="车位太多，不播报:"${restCount}
            break
        fi

        shouldReport=true
        break
    done

    if [ "$shouldReport" = false ]; then
        echo $msg
        return
    fi

    g_lastCount=${restCount}

    dingdingtext=${dateStr}" \n"${dingMsg}"： "${restCount}

    echo $dingdingtext

    data='{"msgtype": "text",
            "text": {
            "content": "'${dingdingtext}'"
    }
    }'

    #echo 钉钉通知
    curl 'https://oapi.dingtalk.com/robot/send?access_token=' \
        -H 'Content-Type: application/json' \
        -d "${data}"

}

n=0

while ((${n} < ${durationTimes})); do
    printOnce
    n=$((n + 1))

    #修正一下耗时，避免误差越来越大
    cost=$(date "+%S")
    sleepInterval=$(expr ${intervalSeconds} - ${cost})
    # echo ${sleepInterval}
    sleep ${sleepInterval}

done
