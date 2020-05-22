#coding:utf-8
#import Base,tools,sys,re
import re,time,datetime,urllib.request,json
from xml.dom.minidom import Document


def gettime(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y%m%d%H%M%S",time_local)
    return dt

TIME_ZONE=" +0800"

TVs= {'1':'cctv1','2':'cctv2','3':'cctv3','4':'cctv4','5':'cctv5','6':'cctv5plus','7':'cctv6','8':'cctv7','9':'cctv8','10':'cctvjilu','11':'cctv10','12':'cctv11','13':'cctv12','14':'cctv13','15':'cctvchild','16':'cctv15','17':'cctv17','27':'hunan','28':'zhejiang','29':'jiangsu','30':'btv1','31':'dongfang','32':'anhui','33':'guangdong','34':'shenzhen','36':'liaoning','37':'travel','38':'shandong','39':'tianjin','40':'chongqing','41':'dongnan','44':'guizhou','45':'hebei','46':'heilongjiang','47':'henan','48':'hubei','50':'jiangxi','51':'jilin','56':'sichuan','106':'cctv4k'}

TVname={'cctv1':'CCTV1','cctv2':'CCTV2','cctv3':'CCTV3','cctv4':'CCTV4','cctv5':'CCTV5','cctv5plus':'CCTV5+','cctv6':'CCTV6','cctv7':'CCTV7','cctv8':'CCTV8','cctvjilu':'CCTV9','cctv10':'CCTV10','cctv11':'CCTV11','cctv12':'CCTV12','cctv13':'CCTV13','cctvchild':'CCTV14','cctv15':'CCTV15','cctv17':'CCTV17','cctv4k':'CCTV4K','hunan':'湖南卫视','zhejiang':'浙江卫视','jiangsu':'江苏卫视','btv1':'北京卫视','dongfang':'东方卫视','anhui':'安徽卫视','guangdong':'广东卫视','shenzhen':'深圳卫视','liaoning':'辽宁卫视','travel':'海南卫视','shandong':'山东卫视','tianjin':'天津卫视','chongqing':'重庆卫视','dongnan':'东南卫视','guizhou':'贵州卫视','hebei':'河北卫视','heilongjiang':'黑龙江卫视','henan':'河南卫视','hubei':'湖北卫视','jiangxi':'江西卫视','jilin':'吉林卫视','sichuan':'四川卫视'}


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



