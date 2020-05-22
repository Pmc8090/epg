#coding:utf-8
#import Base,tools,sys,re
import re,time,datetime,urllib.request,json
from xml.dom.minidom import Document


def gettime(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y%m%d%H%M%S",time_local)
    return dt

TIME_ZONE=" +0800"

TVs= {'1':'cctv1'}

TVname={'cctv1':'CCTV1'}

if __name__=="__main__":
    tvdoc=Document()
    ###tv根节点
    tv=tvdoc.createElement("tv")
    tv.setAttribute("generator-info-name","epg")
    tv.setAttribute("generator-info-url","1234567@qq.com")
    tvdoc.appendChild(tv)
    ###写入节目列表
    for key,value in TVs.items():
        ###channel 标签
        channel=tvdoc.createElement("channel")
        channel.setAttribute("id",key)

        ###display-name
        display_name=tvdoc.createElement("display-name")
        display_name.setAttribute("lang","zh")
        ###display-name 标签中的值
        display_name_var=tvdoc.createTextNode(TVname.get(TVs[key]).upper())
        display_name.appendChild(display_name_var)
        ###添加到channel节点
        channel.appendChild(display_name)
        ###添加到根标签
        tv.appendChild(channel)

    for key,value in TVs.items():

        for num in range(0, 2):

            parsertime = datetime.datetime.now() + datetime.timedelta(days=num)
            parsertime = parsertime.strftime("%Y%m%d")
            parsertime_nextday=datetime.datetime.now() + datetime.timedelta(days=num+1)
            parsertime_nextday=parsertime_nextday.strftime("%Y%m%d")

            file=urllib.request.urlopen('http://api.cntv.cn/epg/getEpgInfoByChannelNew?c='+TVs[key]+'&serviceId=tvcctv&d='+parsertime+'&t=json')
            ###json 格式
            parser = json.load(file,encoding="utf-8")
            parser = parser['data'][TVs[key]]['list']
            for ele in parser:

                programme=tvdoc.createElement("programme")
                programme.setAttribute("start",str(gettime(ele['startTime']))+ TIME_ZONE)
                starttime_index=parser.index(ele)
                if starttime_index == len(parser)-1:
                    programme.setAttribute("stop", str(parsertime_nextday)+'000000'+ TIME_ZONE)
                else:
                    programme.setAttribute("stop", str(gettime(ele['endTime']))+ TIME_ZONE)

                programme.setAttribute("channel",key)

                title = tvdoc.createElement("title")
                text=tvdoc.createTextNode(ele['title'])
                title.setAttribute("lang","zh")
                title.appendChild(text)
                programme.appendChild(title)
                tv.appendChild(programme)


                with open("epg.xml","w",encoding='utf-8') as f:
                    repl = lambda x: ">%s</" % x.group(1).strip() if len(x.group(1).strip()) != 0 else x.group(0)
                    #pretty_str = re.sub(r'>\n\s*([^<]+)</', repl, tvdoc.toprettyxml(indent="\t",encoding="UTF-8"))
                    pretty_str = re.sub(r'>\n\s*([^<]+)</', repl, tvdoc.toprettyxml(indent=" "))
                    f.write(pretty_str)



