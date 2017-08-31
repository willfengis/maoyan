import requests
from requests.exceptions import RequestException
import re
from multiprocessing  import Pool
import pymysql

class sprider():
    def __init__(self):
        pass

    def mysqlOpen(self):
        self.mysqlcnt = pymysql.connect("127.0.0.1","root","123456","text",charset="utf8")
        self.mycursor = self.mysqlcnt.cursor()
        self.myinsert = 'insert into maoyan values("{0}","{1}","{2}","{3}")'

    def mysqlClose(self):
        self.mycursor.close()
        self.mysqlcnt.close()

    def getHtml(self,url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None

    def getStr(self,myhtml):
        my_rule = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?"name"><a.*?>(.*?)</a>.*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>',re.S)
        mystr = re.findall(my_rule,myhtml)
        for item in mystr:
            yield [item[0],item[1],item[2].strip(),item[3]]

    def writeStr(self,item):
        self.mycursor.execute(self.myinsert.format(item[0],item[1],item[2],item[3]))
        self.mysqlcnt.commit()
        print(item)

    def main(self,offset):
        url = "http://maoyan.com/board/4?offset="+str(offset)
        myhtml = self.getHtml(url)
        self.mysqlOpen()
        for item in self.getStr(myhtml):
            self.writeStr(item)
        self.mysqlClose()

if __name__ == "__main__":
    maoyan = sprider()
    pool = Pool()
    pool.map(maoyan.main,[i*10 for i in range(10)])
