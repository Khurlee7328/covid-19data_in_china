import requests
import json
import re
from lxml import etree
from pyecharts import options as opts
from pyecharts.charts import Map


def getHTMLText(url):
    kv = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.70 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
    try:

        res = requests.get(url, headers=kv)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return "爬取失败"


def getTime(html):
    time_in = re.findall('"mapLastUpdatedTime":"(.*?)"', html)[0]
    time_abroad = re.findall('"foreignLastUpdatedTime":"(.*?)"', html)[0]
    return time_in, time_abroad


def parseData(html):
    html = etree.HTML(html)
    result = html.xpath('//script[@type="application/json"]/text()')[0]
    result_in = json.loads(result)['component'][0]['caseList']
    result_abroad = json.loads(result)['component'][0]['globalList']
    return result_in, result_abroad


def china_map(result):
    if 'subList' in result[0][0]:
        area = []
        pro_confirmed = []
        for each in result[0]:
            area.append(each['area'])
            pro_confirmed.append(each['confirmed'])
    return area, pro_confirmed


def province_map(result):
    if 'subList' in result[0][0]:
        city = []
        ci_confirmed = []
        for each in result[0]:
            city = []
            ci_confirmed = []
            province = each['area']
            for each_city in each['subList']:
                city.append(each_city['city'])
                ci_confirmed.append(each_city['confirmed'])


class Draw_Map:
    def to_map_china(self, area, variate, update_time):
        pieces = [{"max": 999999, "min": 1001, "label": ">10000", "color": "#8A0808"},
                  {"max": 9999, "min": 1000, "label": "1000-9999", "color": "#B40404"},
                  {"max": 999, "min": 100, "label": "100-999", "color": "#DF0101"},
                  {"max": 99, "min": 10, "label": "10-99", "color": "#F78181"},
                  {"max": 9, "min": 1, "label": "1-9", "color": "#F5A9A9"},
                  {"max": 0, "min": 0, "label": "0", "color": "#FFFFFF"},
                  ]
        c = (
            Map(init_opts=opts.InitOpts(width='1000px', height='880px', )).add("累计确诊人数", [list(z) for z in zip(area,
                                                                                                               variate)]
                                                                               ,"china").set_global_opts(
                title_opts=opts.TitleOpts(title="中国疫情地图", subtitle="截止%s 中国疫情地图分布情况" % update_time, pos_left="center",
                                          pos_top='50px'),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True, pieces=pieces),
            )
                .render("中国疫情地图.html")
        )


def main():
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"
    html = getHTMLText(url)

    update_time = getTime(html)
    result = parseData(html)
    province_map(result)
    area, pro_confirmed = china_map(result)
    map1 = Draw_Map()
    map1.to_map_china(area, pro_confirmed, update_time[0])


if __name__ == '__main__':
    main()
