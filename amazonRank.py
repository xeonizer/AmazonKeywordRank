import time
import os
import json
from bs4 import BeautifulSoup
from lxml import etree
import lxml.html
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse as urlparse
from urllib.parse import parse_qs
import requests
import random
class amazon:
    def __init__(self):
        locky_sp=0
        locky_non=0
        self.locky_sp=locky_sp
        self.locky_non = locky_non

    def __enter__(self):
        return self



    def __exit__(self, exc_type, exc_value, exc_tracebac):
        # os.system("pause")
        try:
            input("press any key to exit")
        except Exception as e:
            pass

    def setPostal(self,postal):
        chrome_options = webdriver.ChromeOptions()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--ignore-certificate-error_checks')
        chrome_options.add_argument('--log-level=OFF')
        chrome_options.add_argument('--lang=en-US,en')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("window-size=1200x600")
        driver = webdriver.Chrome(executable_path=r"chromedriver.exe", chrome_options=chrome_options)
        driver.execute_script("window.key = \'blahblah\';")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'plugins', {
                get: () => [3,2,1]
            })
          """
        })
        driver.maximize_window()
        driver.get("https://www.amazon.com/")
        p=driver.find_element_by_xpath("//a[@id='nav-global-location-popover-link']")
        p.click()
        time.sleep(1)
        x=f"document.getElementById('GLUXZipUpdateInput').value='{postal}'"
        driver.execute_script(x)
        actions = ActionChains(driver)
        actions.move_by_offset(700, 328).click().perform()
        time.sleep(5)
        driver.save_screenshot("hh.png")
        actions.reset_actions()
        actions.move_by_offset(11, 60).click().perform()
        time.sleep(3)
        driver.refresh()
        driver.save_screenshot("proof.png")
        print("Postal Code Set")
        driver.get("https://www.amazon.com/")
        c=driver.get_cookies()
        with open("cookie_"+str(postal)+".cred",'w+') as w:
            w.write(json.dumps(c))
        driver.close()
        driver.quit()
        return c


    def searchReq(self,keyword,cookies):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        keyword = keyword.replace(" ", "+")
        try:
            with requests.Session() as s:
                for cookie in cookies:
                    s.cookies.set(cookie['name'], cookie['value'])
                resp = s.get("https://www.amazon.com/s?k="+keyword,headers=headers,timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            dom = etree.HTML(str(soup))
            total_pages = dom.xpath("//ul[@class='a-pagination']//li[last()-1]")
            print(f"Total Pages={total_pages[0].text},qid={int(time.time())}")
            return int(time.time()), total_pages[0].text
        except Exception as e:
            print(f"Total Pages not Found:{e}")
            return int(time.time()),6



    def for_sponsored(self,asin,page,keyword,resp):
        soup = BeautifulSoup(resp, "html.parser")
        dom = etree.HTML(str(soup))
        search = dom.xpath("//div[@data-component-type='s-search-result' and contains(@class,'AdHolder')]")
        print("sponsored =" + str(len(search)))
        for d in search:
            if d.get("data-asin") == asin:
                rank = "page" + str(int(page + 1)) + "_" + str(search.index(d) + 1)
                print(rank, d.get("data-asin"),"sponsored")
                self.locky_sp=1
                with open("output.csv",'a+') as w:
                    keyword = keyword.replace("+", " ")
                    w.writelines(keyword+","+asin+","+rank+","+"sponsored"+"\n")
                break

    def for_nonsponsored(self,asin,page,keyword,resp):
        soup = BeautifulSoup(resp, "html.parser")
        dom = etree.HTML(str(soup))
        search = dom.xpath("//div[@data-component-type='s-search-result' and not(contains(@class,'AdHolder'))]")
        print("organic =" + str(len(search)))
        for d in search:
            if d.get("data-asin") == asin:
                rank = "page" + str(int(page + 1)) + "_" + str(search.index(d) + 1)
                print(rank, d.get("data-asin"),"organic")
                self.locky_non=1
                with open("output.csv",'a+') as w:
                    keyword = keyword.replace("+", " ")
                    w.writelines(keyword+","+asin+","+rank+","+"organic"+"\n")
                break

    def postalCode(self,postal,cookies):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://www.amazon.com/',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers',
        }
        # cookie=""
        # for c in cookies:
        #     cookie=cookie+c['name']+"="+c['value']+";"
        # cookies = {
        #     'session-id': '141-6809326-0683233',
        #     'session-id-time': '2082787201l',
        #     'i18n-prefs': 'USD',
        #     'csm-hit': 'tb:K2S8JN1KWTP60JEZZYW3+s-WCD9HQ5FYN45SYPQRMEP|1628099198466&t:1628099198466&adb:adblk_no',
        #     'ubid-main': '135-6697818-9661416',
        #     'session-token': 'MwWoKz0dShvUE8c+URDMIb+RdFajBhVsEg+1DoqW3Yv4BHxRk5AfH54g2oOsf+Wu5MK8d9pCSrnAyrLuDKtkKmC/UhTGvsnofuBCkIHJciipgGsZvt82RS3IC7lKPqEwxdCCaNadVmG8CdGL7p1PHdAzoRicseKsIzm8y+YI6MYccwlW5Tdoix5o2FdPCYuK',
        #     'skin': 'noskin',
        # }
        url="https://www.amazon.com/s?k=turmeric+gummies&ref=nb_sb_noss"
        with requests.Session() as s:
            for cookie in cookies:
                s.cookies.set(cookie['name'], cookie['value'])
            r=s.get(url,headers=headers,timeout=10).text
        print(r.find(str(postal)))
        return r.find(str(postal))

    def extract(self,keyword,qu_id,pgs,asin,cookies):
        headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'},
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'},
            {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36'},
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'},
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
            {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
            {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'},
            {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}
        ]
        headers = {
            'User-Agent': random.choice(headers_list)['User-Agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        self.locky_sp=0
        self.locky_non = 0
        keyword=keyword.replace(" ","+")

        s = requests.Session()
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        page=0
        while True:
            time.sleep(1)
            url="https://www.amazon.com/s?k="+keyword+"&page="+str(int(page+1))+"&qid="+str(qu_id)+"&ref=sr_pg_"+str(int(page+1))
            print(url)
            response=s.get(url,headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            dom = etree.HTML(str(soup))
            if self.locky_sp==0:
                self.for_sponsored(asin,page,keyword,response.text)
            if self.locky_non==0:
                self.for_nonsponsored(asin,page,keyword,response.text)
            if self.locky_sp == 1 and self.locky_non==1:
                break
            page+=1
            try:
                next=dom.xpath("//a[contains(text(),'Next')]")
                if len(next) != 1:
                    break
            except exception as e:
                pass

    def isCookiePresent(self,postal):
        filename="cookie_"+str(postal)+".cred"
        return os.path.isfile(filename)

    def parsecookies(self,postal):
        if self.isCookiePresent(postal):
            filename="cookie_"+str(postal)+".cred"
            with open(filename,"r") as r:
                f=json.loads(r.read())
                if self.postalCode(postal,f) > -1:
                    return f
        else:
            return self.setPostal(postal)

if __name__ == "__main__":
    input_data=[]
    with open("input.csv", 'r') as rg:
        for x in rg:
            input_data.append(x.replace("\n","").split(","))
    # with open("output.csv", 'a+') as w:
    #     w.writelines("\n")
    with amazon() as am:
        postal=int(input("Enter Postal Code:"))
        # cookies=am.setPostal(postal)
        cookies=am.parsecookies(postal)
        if am.postalCode(postal,cookies) > -1:
            for x in input_data:
                print(x)
                time.sleep(1)
                am.extract(x[1],int(time.time()),7,x[0],cookies)
        else:
            print("Postal Code not Set, need to change cookies")





