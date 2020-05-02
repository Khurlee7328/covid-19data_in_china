import requests
from lxml import etree
import json
import openpyxl

url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3"
kv = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def getHTMLText(url):
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "失败"


# 生成HTML对象
text = getHTMLText(url)
html = etree.HTML(text)
results = html.xpath('//script[@type="application/json"]/text()')

# 使用json.loads(）将字符串转化为python数据类型  dict
results = json.loads(results[0])


# 创建工作簿
wb = openpyxl.Workbook()
# 创建工作表
ws = wb.active
# 解析出更准确的数据
results_in = results['component'][0]['caseList']
results_abroad = results['component'][0]['globalList']
# print(results_abroad[0])

ws.title = "国内"
ws.append(['省份', '累计确诊', '死亡人数', '治愈人数', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量'])

for each in results_in:
    temp_list = [each['area'],
                 each['confirmed'],
                 each['died'],
                 each['crued'],
                 each['curConfirm'],
                 each['confirmedRelative'],
                 each['diedRelative'],
                 each['curedRelative'],
                 each['curConfirmRelative']]
    for i in range(len(temp_list)):
        if temp_list[i] == '':
            temp_list[i] = '0'
    ws.append(temp_list)

for each in results_abroad:
    sheet_title = each['area']
    # 创建新的工作表
    ws_abroad = wb.create_sheet(sheet_title)
    ws_abroad.append(['国家', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量'])
    for country in each['subList']:
        temp_list = [country['country'],
                     country['confirmed'],
                     country['died'],
                     country['crued'],
                     country['curConfirm'],
                     country['confirmedRelative']]
        for i in range(len(temp_list)):
            if temp_list[i] == '':
                temp_list[i] = '0'
        ws_abroad.append(temp_list)



'''
area -------  省份/直辖市/特别行政区等
city -------  城市
confirmed ------  累计确诊人数
died  ------  死亡人数
cured  ------  治愈人数
confirmRelative  ------  现有确诊增量
curedRelative  ------  治愈增量
curConfirmed  ------  现有确诊人数
curConfirmRelative  ------  现有确诊的增量
diedRelative  ------  死亡增量
'''

wb.save('./data.xlsx')
