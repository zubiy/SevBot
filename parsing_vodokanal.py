from reid_parse import get_source
from bs4 import BeautifulSoup
import re
from datetime import date
from sqlighter import SQLighter
import time
from datetime import datetime
from dateutil import parser

today = date.today()
db = SQLighter('db.db')
def vodokanal():
    info = []
    regex_span = '<span.*?>(.+?)</span>'
    res = get_source('https://sevvodokanal.org.ru/news')
    soup = BeautifulSoup(res.content, 'html.parser')
    for div_tag in soup.findAll('div', id="news-preview"):
        for div_tag2 in div_tag.findAll('div', class_='right-preview'):
            #print(div_tag2)
            date = re.findall(regex_span, str(div_tag2))[0]
            date = parser.parse(date).date()
            if date == today:
                for a_tag in div_tag2.findAll('a'):
                    res1 = get_source('https://sevvodokanal.org.ru/' + a_tag.attrs.get('href'))
                    soup1 = BeautifulSoup(res1.content, 'html.parser')
                    for div_tag4 in soup1.findAll('div', class_='right-preview'):
                        msg = ' '.join(div_tag4.stripped_strings).strip()
                        info.append(msg)
    return info

def add_mesage():
    i =0
    print('Start')
    while True:
        if i == 0:
            info_vodokanal = vodokanal()
            if not info_vodokanal:
                time.sleep(5)
                continue

            for info in info_vodokanal:
                date = datetime.now()
                db.add_message_vodakanal(date,info)
            old_info = info_vodokanal
            i+=1
            print('First iteration')
        if i!=0:
            info_vodokanal = vodokanal()

            if info_vodokanal == old_info:
                continue
            if info_vodokanal != old_info:
                per = set(info_vodokanal) - set(old_info)
                if len(per)!=0:
                    for info in per:
                        date = datetime.now()
                        db.add_message_vodakanal(date, info)
                        old_info.append(info)
        time.sleep(5)

if __name__ == '__main__':
    add_mesage()