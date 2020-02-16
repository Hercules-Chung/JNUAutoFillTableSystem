# -*- coding: utf-8 -*-        
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
import pymysql
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from selenium.webdriver.support.ui import Select
PATH_TO_CHROME_DRIVER = 'F:\迅雷下载\chromedriver.exe'
class TableRobotBase:
    def fillTable(self,user):
        pass
    def readDatabase(self):
        pass
    def sendMail(self,user):
        sender = 'jiaqinlin12138@163.com'
        receiver = user['email']
        title = "今日填表结果"
        message = "今天的填表已经完成，请查收" + user['link']

        pw = "linjiaqin12306"
        smtp = SMTP_SSL('smtp.163.com',465)
        smtp.login(sender,pw)
        msg = MIMEText(message,"plain",'utf-8')
        msg["Subject"] = Header(title,'utf-8')
        msg["From"] = sender
        msg["To"] = receiver
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    def task(self):
        userList = self.readDatabase()
        for user in userList:
            user['link'] = self.fillTable(user)
            self.sendMail(user)
class TableRobot1(TableRobotBase):
    db = pymysql.connect("aliyun.linjiaqin.xyz","root","toor","JNUSTU")
    postURLToLogin = "https://ehall.jnu.edu.cn/infoplus/form/XNYQSB/start"
    def readDatabase(self):
        # 读取数据库
        cursor = self.db.cursor()
        counts = cursor.execute("select * from LoginData")
        userAccount = cursor.fetchall()
        result = []
        for user in userAccount:
            cursorForInfo = self.db.cursor()
            if(cursorForInfo.execute("select * from UserInfo where user=\'" + user[0]+"\'") > 1):
                raise Exception("Error: no less than one user info")
            userinfo = cursorForInfo.fetchone()
            oneuser = {
                'user': user[0],
                'password': user[1],
                'email': user[2],
                'teacher': userinfo[1],
                'class': userinfo[2],
                'contactName': userinfo[3],
                'contactPhone': userinfo[4],
                'province': userinfo[5],
                'city': userinfo[6],
                'area': userinfo[7],
                'road': userinfo[8]
            }
            print(oneuser)
            result.append(oneuser)
        return result
    def fillTable(self,user):
        # 启动浏览器
        # chrome_options = Options()
        # chrome_options.add_argument('--no-sanddbox')
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--disable-extensions')
        # chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        # chrome_options.add_argument('--headless')
        # specify the path of chrome driver.
        # browser = webdriver.Chrome(PATH_TO_CHROME_DRIVER,chrome_options=chrome_options)
        browser = webdriver.Chrome(PATH_TO_CHROME_DRIVER)
        browser.get(self.postURLToLogin)
        # 填表
        # 登录
        username = browser.find_element_by_id('un')
        password = browser.find_element_by_id('pd')
        un = user['user']
        pw = user['password']
        username.send_keys(un)
        password.send_keys(pw)
        loginBtn = browser.find_element_by_id('index_login_btn')
        loginBtn.click()
        # 等待加载页面
        time.sleep(5)
        # 开始填表
        browser.find_element_by_name('fieldJBXXjjlxr').send_keys(user['contactName'])
        browser.find_element_by_name('fieldJBXXnj').send_keys(user['class'])
        browser.find_element_by_name('fieldJBXXjjlxrdh').send_keys(user['contactPhone'])
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[4]/td[4]/div/div/div/div/input").send_keys(user['teacher'])
        # 辅导员下拉框
        while len(browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[4]/td[4]/div/div/div/div/div").text) == 0:
            time.sleep(0.5)
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[4]/td[4]/div/div/div/div/div").find_elements_by_xpath("div")[1].click()
        
        browser.find_elements_by_name('fieldSTQKsfstbs')[0].click()
        browser.find_elements_by_name('fieldCXXXcxzt')[0].click()
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[2]/div/div/div/div/input").send_keys(user['province'])
        while len(browser.find_elements_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[2]/div/div/div/div/div/div"))!=2:
            time.sleep(0.5)
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[2]/div/div/div/div/div/div").click()
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[4]/div/div/div/div/input").send_keys(user['city'])
        while len(browser.find_elements_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[4]/div/div/div/div/div/div"))!=2:
            time.sleep(0.5)
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[4]/div/div/div/div/div/div").click()
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[6]/div/div/div/div/input").send_keys(user['area'])
        while len(browser.find_elements_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[6]/div/div/div/div/div/div"))!=2:
            time.sleep(0.5)
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[6]/div/div/div/div/div/div").click()
        browser.find_element_by_xpath("//td[@class='xdTableContentCell']/div/table/tbody/tr[22]/td[8]/div/input").send_keys('潮汕路')
        browser.find_elements_by_name('fieldYQJLjrsfczbl')[1].click()
        browser.find_elements_by_name('fieldYQJLsfjcqtbl')[1].click()
        browser.find_elements_by_name('fieldCXXXsftjhb')[1].click()
        browser.find_element_by_name('fieldCNS').click()
        browser.find_element_by_xpath('/html/body/div[4]/form/div/div/div[2]/ul/li[1]/a').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[7]/div/div[2]/button').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[7]/div/div[2]/button').click()
        time.sleep(5)
        result = browser.current_url
        print(browser.current_url)
        browser.close()
        return result
    
class TableRobot2(TableRobotBase):
    db = pymysql.connect("aliyun.linjiaqin.xyz","root","toor","JNUSTU")
    postURLToLogin = "https://stuhealth.jnu.edu.cn/#/login"
    postURLToFill = "https://stuhealth.jnu.edu.cn/#/index"
    def readDatabase(self):
        # 读取数据库
        cursor = self.db.cursor()
        counts = cursor.execute("select * from LoginData")
        userAccount = cursor.fetchall()
        result = []
        for user in userAccount:
            cursorForInfo = self.db.cursor()
            if(cursorForInfo.execute("select * from UserInfo where user=\'" + user[0]+"\'") > 1):
                raise Exception("Error: no less than one user info")
            userinfo = cursorForInfo.fetchone()
            oneuser = {
                'user': user[0],
                'password': user[1],
                'email': user[2],
                'teacher': userinfo[1],
                'class': userinfo[2],
                'contactName': userinfo[3],
                'contactPhone': userinfo[4],
                'TrafficNo': userinfo[5],
                'TrafficType': userinfo[6],
                'province': userinfo[7],
                'city': userinfo[8],
                'area': userinfo[9],
                'arriveDate': userinfo[10],
                'leaveDate': userinfo[11],
                'road': userinfo[13],
                'phone': userinfo[14]
            }
            print(oneuser)
            result.append(oneuser)
        return result
    def selectDate(self,browser,element,t):
        browser.find_element_by_name(element).click()
        year,month,day = t.split('-')
        browser.find_element_by_xpath("//div[@class='datepicker-days']/table/thead/tr/th[2]").click()
        browser.find_element_by_xpath("//div[@class='datepicker-months']/table/thead/tr/th[2]").click()
        not_in_Range = True
        while not_in_Range:
            yearRange = [int(y) for y in browser.find_element_by_xpath("//div[@class='datepicker-years']/table/thead/tr/th[2]").text.split('-')]
            yearRange[0]-=1
            yearRange[1]+=1
            if int(year) < yearRange[0]:
                browser.find_element_by_xpath("//div[@class='datepicker-years']/table/thead/tr/th[1]").click()
            elif int(year) > yearRange[1]:
                browser.find_element_by_xpath("//div[@class='datepicker-years']/table/thead/tr/th[2]").click()
            else:
                not_in_Range = False
                yearList = browser.find_elements_by_xpath("//div[@class='datepicker-years']//td/span")
                index = 0
                for i in range(len(yearList)):
                    if year in yearList[i].text:
                        index = i
                        break
                yearList[index].click()
                monthList = browser.find_elements_by_xpath("//div[@class='datepicker-months']//td/span")
                monthList[int(month)-1].click()
                browser.find_elements_by_xpath("//div[@class='datepicker-days']/table/thead/tbody//td[@class='day']")
                dayList = browser.find_elements_by_xpath("//div[@class='datepicker-days']/table/tbody//td")
                index = 0
                for i in range(len(dayList)):
                    attribute = dayList[i].get_attribute("class")
                    if(attribute != 'day' and attribute!='active day'):
                        continue
                    if int(day) == int(dayList[i].text):
                        index = i
                        break
                if dayList[index].get_attribute("class")=='active day':
                    dayList[index].click()
                    dayList = browser.find_elements_by_xpath("//div[@class='datepicker-days']/table/tbody//td")
                    dayList[index].click()
                else:
                    dayList[index].click()
    def fillTable(self,user):
        # 启动浏览器
        # chrome_options = Options()
        # chrome_options.add_argument('--no-sanddbox')
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--disable-extensions')
        # chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        # chrome_options.add_argument('--headless')
        # specify the path of chrome driver.
        # browser = webdriver.Chrome(PATH_TO_CHROME_DRIVER,chrome_options=chrome_options)
        browser = webdriver.Chrome(PATH_TO_CHROME_DRIVER)
        browser.get(self.postURLToLogin)
        username = browser.find_element_by_name('appId')
        password = browser.find_element_by_name('password')
        un = user['user']
        pw = user['password']
        username.send_keys(un)
        password.send_keys(pw)
        browser.find_element_by_xpath("//button[@class='btn btn-primary btn-block btn-flat']").click()
        time.sleep(1)
        # 开始填表
        browser.get("https://stuhealth.jnu.edu.cn/#/index")
        time.sleep(1)
        browser.find_element_by_name("phone").clear()
        browser.find_element_by_name("phone").send_keys(user["phone"])
        browser.find_element_by_name("class_name").clear()
        browser.find_element_by_name("class_name").send_keys(user["class"])
        # 辅导员选择
        browser.find_element_by_xpath("//body[@class='skin-blue-light']/app-root/app-index/div[@class='wrapper sidebar-collapse']/div[@class='content-wrapper']/app-home/section[@class='content']/section/div[@class='row']/div[@class='col-md-12']/div[@class='box']/div[@class='box-header with-border']/div/div[9]/div[1]/span[1]/span[1]/span[1]/span[1]").click()
        res = browser.find_elements_by_xpath("//ul[@id='select2-assistant_name-results']/li")
        teacher = user["teacher"]
        index = 0
        for i in range(len(res)):
            if teacher in res[i].text:
                index = i
                break
        res[index].click()
        browser.find_element_by_name("linkman").clear()
        browser.find_element_by_name("linkman").send_keys(user["contactName"])
        browser.find_element_by_name("linkmanPhone").clear()
        browser.find_element_by_name("linkmanPhone").send_keys(user["contactPhone"])
        browser.find_element_by_name("temperature").clear()
        browser.find_element_by_name("temperature").send_keys("36.5")
        browser.find_elements_by_name("stqk")[0].click()
        browser.find_elements_by_name("jqshdr")[1].click()
        browser.find_elements_by_name("jqlxqk")[0].click()
        self.selectDate(browser,"lxsj",str(user["leaveDate"]))
        self.selectDate(browser,"ddmddsj",str(user["arriveDate"]))
        browser.find_elements_by_name("leave_hubei")[1].click()
        if not browser.find_elements_by_name("lxjtgj")[1].is_selected():
            browser.find_elements_by_name("lxjtgj")[user["TrafficType"]].click()
        browser.find_element_by_name("way_no").clear()
        browser.find_element_by_name("way_no").send_keys(user["TrafficNo"])
        browser.find_elements_by_name("person_state")[0].click()
        browser.find_elements_by_name("sfzzgjw")[0].click()
        provinces = browser.find_element_by_xpath("//select[@name='selectProvince']")
        s1 = Select(provinces)
        s1.select_by_visible_text(user["province"])
        # browser.find_element_by_xpath("//select[@name='selectProvince']").click()
        citys = browser.find_element_by_xpath("//select[@name='selectCity']")
        s1 = Select(citys)
        s1.select_by_visible_text(user["city"])
        area = browser.find_element_by_xpath("//select[@name='selectDistrict']")
        s1 = Select(area)
        s1.select_by_visible_text(user["area"])
        browser.find_element_by_xpath("//input[@name='person_c4']").clear()
        browser.find_element_by_xpath("//input[@name='other_c4']").clear()
        browser.find_element_by_xpath("//input[@name='person_c4']").send_keys(user["road"])
        browser.find_element_by_xpath("//input[@name='other_c4']").send_keys("没有")
        browser.find_elements_by_name("is_other")[1].click()
        browser.find_elements_by_name("is_pass_c1")[1].click()
        browser.find_elements_by_name("is_family")[1].click()
        browser.find_element_by_xpath("//body[@class='skin-blue-light']/app-root/app-index/div[@class='wrapper sidebar-collapse']/div[@class='content-wrapper']/app-home/section[@class='content']/section/div[@class='row']/div[@class='col-md-12']/div[@class='box']/div[@class='box-header with-border']/div/div/input[1]").click()
        browser.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        result = "https://stuhealth.jnu.edu.cn/#/index/complete"
        print(browser.current_url)
        browser.close()
        return result
        
if __name__=='__main__':
    Time = {'h': 6,'m': 0}
    robot = TableRobot()
    while True:
        while True:
            now = datetime.datetime.now()
            if now.hour == Time['h'] and now.minute == Time['m']:
                break
            time.sleep(10)
        robot.task()

# robot = TableRobot2()

# robot.task()
