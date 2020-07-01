import requests
import datetime
from tkinter import messagebox
import os
from tkinter import *
import execjs
class Daka:
    def __init__(self):
        # self.username=username
        # self.password=password
        self.sess = requests.session()
        self.init()
        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        self.host = "yun.ujs.edu.cn"
        self.header={"User-Agent":self.UA,"Host":self.host,
                   }
        self.url = 'http://yun.ujs.edu.cn/xxhgl/yqsb/index?ticket='
        # print(self.cookie)
        self.nexturl = "http://"+self.host+self.getNextUrl()

    def getNextUrl(self):
        # print(self.url)
        # print(self.cookie)
        txt = self.sess.get(self.url,headers=self.header).text
        # print(txt)
        return re.findall("<a href=\"(.*?)\" class=\"weui_btn  weui_btn_primary\" >每日健康打卡",txt)[0]
    def init(self):
        if(os.path.exists('lastDate.cfg') == True):
            with open('lastDate.cfg','r') as f:
                date = f.readline()
            if date == str(datetime.datetime.now().day):
                exit(0)
        root = Tk()
        root.withdraw()
        self.choice=0
        if(os.path.exists('jkdk.cfg') == False or os.path.getsize('jkdk.cfg') == 0):
            messagebox.showinfo("警告","该软件仅供学习讨论，请勿用于偷懒打卡，否则后果自负")
            self.fillInfo()
            with open('jkdk.cfg','w') as f:
                f.write(self.username+"\n")
                f.write(self.password+"\n")
        else:
            with open('jkdk.cfg', 'r') as f:
                self.username = f.readline()
                self.password = f.readline().replace('\n','')
        if(os.path.exists('choice.cfg')==True):
            with open('choice.cfg','r') as g:
                self.choice = int(g.readline())
        L = Login(self.username,self.password,self.sess)
        L.go()


    def toDo(self,data=None):
        txt =  self.sess.get(self.nexturl,headers=self.header).text
        ykt = re.findall("\"请输入一卡通号\" value=\"(.*?)\" readonly",txt)[0]
        dwmc = re.findall('name="dwmc"   value="(.*?)" readonly',txt)[0]
        zy = re.findall('placeholder="请输入专业" value="(.*?)" readonly',txt)[0]
        bj = re.findall('placeholder="请输入班级" value="(.*?)" readonly',txt)[0]
        xm = re.findall('placeholder="请输入姓名" required value="(.*?)" readonly',txt)[0]
        zjh = re.findall('placeholder="请输入证件号" required value="(.*?)" readonly',txt)[0]
        nl =  re.findall('placeholder="请输入年龄" .*?required value="(.*?)"',txt)[0]
        sjh = re.findall('placeholder="请输入手机号" required value="(.*?)"',txt)[0]
        sfhbj = re.findall('name="sfhbj".*?checked="checked" value="(.*?)"',txt)[0]
        sfyxszd = re.findall('name="sfyxszd".*?value="(.*?)"',txt)[0]
        sfid,csid,xqid = re.findall('option value="(.*?)" selected="true"',txt)
        xxdz = re.findall('placeholder="请输入详细地址" required value="(.*?)"', txt)[0]
        sffx = re.findall('name="sffx" type="radio".*?checked="checked" value="(.*?)"',txt)[0]
        # print(txt)
        infos = re.findall('option selected="true" value="(.*?)"',txt)
        if len(infos)==11:
            rylb, ryjtlb, jqdt, dzsj_m, dzsj_d, _, czjtgj, yxzt, mqzdyqdyjcs, zdyq, xsfxbj = infos
        elif len(infos)==10:
            rylb, ryjtlb, jqdt, dzsj_m, dzsj_d, czjtgj, yxzt, mqzdyqdyjcs, zdyq, xsfxbj = infos
        else:
            messagebox.showinfo("error","未知错误")
            exit(0)
        xwwd = re.findall('name="xwwd".*? required value="(.*?)"',txt)[0]
        swwd = re.findall('name="swwd".*? required value="(.*?)"',txt)[0]
        jtbjbc = re.findall('placeholder="请输入班次"  value="(.*?)"',txt)[0]
        sfgtjzryfrks = re.findall('name="sfgtjzryfrks" type="radio" checked="checked" value="(.*?)"',txt)[0]
        qtyc = ""
        bz = ""
        latitude =""
        longitude = ""
        btn =""
        data = {
            'ykt':ykt,
            'dwmc':dwmc,
            'zy':zy,
            'bj':bj,
            'xm':xm,
            'zjh':zjh,
            'nl':nl,
            'sjh':sjh,
            'sfhbj':sfhbj,
            'sfyxszd':sfyxszd,
            'sfid':sfid,
            'csid':csid,
            'xqid':xqid,
            'xxdz':xxdz,
            'jqdt':jqdt,
            'sffx':sffx,
            'dzsj_m':dzsj_m,
            'dzsj_d':dzsj_d,
            'czjtgj':czjtgj,
            'jtgjbc':jtbjbc,
            'yxzt':yxzt,
            'mqzdyqdyjcs':mqzdyqdyjcs,
            'zdyq':zdyq,
            'sfgtjzryfrks':sfgtjzryfrks,
            'xsfxbj':xsfxbj,
            'xwwd':xwwd,
            'swwd':swwd,
            'qtyc':qtyc,
            'bz':bz,
            'latitude':latitude,
            'longitude':longitude,
            'btn':btn
        }
        # print(data)
        if(self.choice==0 or self.choice==1):
            for item in data.items():
                print(item)
            self.choice = input("请判断以上信息是否正确，并输入数字命令（0 不正确且不打卡 （1 正确并打卡但以后要显示此信息 （2 正确并打卡且以后不再提示此信息:")
            with open('choice.cfg','w') as g:
                g.write(self.choice)
            self.choice = int(self.choice)
        if self.choice != 0:
            result = self.sess.post(self.nexturl,data=data,headers=self.header).text
            res1,res2 = re.findall('<h2 style="text-align:center">(.*?)</h2>',result)
            messagebox.showinfo("Success",res1.replace("&nbsp;","")+"\n"+res2)
            with open('lastdate.cfg','w') as f:
                f.write(str(datetime.datetime.now().day))
        else:
            messagebox.showinfo("失败","你已取消打卡。")
    def fillInfo(self):
        self.username = input("请输入学号:")
        self.password = input("请输入密码：")
class Login:
    def __init__(self,username,password,sess):
        self.user=username
        self.pwd = password
        self.sess=sess
        self.url = 'https://pass.ujs.edu.cn/cas/login?service=http%3A%2F%2Fyun.ujs.edu.cn%2Fsite%2Flogin'
        self.header={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'host':'pass.ujs.edu.cn'
        }
        self.loginurl = 'https://pass.ujs.edu.cn/cas/login?service=http%3A%2F%2Fyun.ujs.edu.cn%2Fsite%2Flogin'
    def go(self):
        req = self.sess.get(self.url, headers=self.header)
        cookies = requests.utils.dict_from_cookiejar(req.cookies)  # 转成字典格式
        cookie = "; ".join([str(x) + "=" + str(y) for x, y in cookies.items()])
        txt = req.text

        self.lt = re.findall('name="lt" value="(.*?)"/>',txt)[0]

        self.dllt = re.findall('name="dllt" value="(.*?)"/>',txt)[0]
        self.execution = re.findall('name="execution" value="(.*?)"/>',txt)[0]
        self._eventId = re.findall('name="_eventId" value="(.*?)"/>', txt)[0]
        self.rmShown = 1
        # self._eventId = "submit"
        self.pwdDefaultEncryptSalt = re.findall('id="pwdDefaultEncryptSalt" value="(.*?)"/>', txt)[0]
        # print(self.pwdDefaultEncryptSalt)
        # print(self._eventId)
        # tmp = requests.get('https://pass.ujs.edu.cn/cas/needCaptcha.html?username='+str(self.user)+'&pwdEncrypt2=pwdEncryptSalt&_=1593532123403',headers=self.header).text
        # print(tmp)
        with open('encrypt.js') as f:
            jsdata = f.read()
        ctx = execjs.compile(jsdata)
        self.pwd = ctx.call('_ep',self.pwd , self.pwdDefaultEncryptSalt)
        # print(self.pwd)
        self.header2={
            'Content-Type':'application/x-www-form-urlencoded',
            'Origin':'https://pass.ujs.edu.cn',
            'Referer':'https://pass.ujs.edu.cn/cas/login?service=http%3A%2F%2Fyun.ujs.edu.cn%2Fsite%2Flogin',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Cookie':cookie
        }
        data = {
            'username':self.user,
            'password':self.pwd,
            'lt':self.lt,
            'dllt':self.dllt,
            'execution':self.execution,
            '_eventId':self._eventId,
            'rmShown':self.rmShown
        }
        # print(data)
        req2 = self.sess.post(self.loginurl, data,headers=self.header2)
        cookies = requests.utils.dict_from_cookiejar(req2.cookies)  # 转成字典格式
        cookie = "; ".join([str(x) + "=" + str(y) for x, y in cookies.items()])
        self.cookie = cookie
        # print(req2.text)
        if req2.text.find("密码有误") != -1:
            print("密码错误")
            return False
        else:
            print("登录成功")
            return True
if __name__=="__main__":
    # l.go()
    d = Daka()
    d.toDo()