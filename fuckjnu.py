# -*- coding: utf-8 -*-        
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
import pymysql
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
PATH_TO_CHROME_DRIVER = '/usr/bin/chromedriver'
class TableRobot:
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
        chrome_options = Options()
        chrome_options.add_argument('--no-sanddbox')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--headless')
        # specify the path of chrome driver.
        browser = webdriver.Chrome(PATH_TO_CHROME_DRIVER,chrome_options=chrome_options)
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
        
# if __name__=='__main__':
#     Time = {'h': 6,'m': 0}
#     robot = TableRobot()
#     while True:
#         while True:
#             now = datetime.datetime.now()
#             if now.hour == Time['h'] and now.minute == Time['m']:
#                 break
#             time.sleep(10)
#         robot.task()

robot = TableRobot()

robot.task()
