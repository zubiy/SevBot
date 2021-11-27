import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from fake_headers import Headers
from dateutil import parser
from datetime import date, datetime
from sqlighter import SQLighter
import time

header = Headers()
today = date.today()
db = SQLighter('db.db')
def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url, headers=header.generate())
       # time.sleep(2)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def reid():
    regex_span = '<span.*?>(.+?)</span>'
    regex_a = '<a.*?>(.+?)</a>'
    res = get_source('https://www.sevmp.ru/')
    soup = BeautifulSoup(res.content, 'html.parser')
    message = []
    for li_tag in soup.findAll('li', class_='widget widget_recent_entries'):
        for li_tag2 in li_tag.findAll('li'):
            date = re.findall(regex_span, str(li_tag2))
            date = parser.parse(date[0]).date()
            info = re.findall(regex_a, str(li_tag2))[0]
            if date == today:
                info = f"{date.day}.{date.month}.{date.year} - {info}"
                message.append(info)
    return message


def add_mesage():
	i =0
	print('Start')
	while True:
		if i == 0:
			info_rade = reid()
			if not info_rade:
				time.sleep(5)
				continue

			for info in info_rade:
				date = datetime.now()
				db.add_message_reid(date,info)
			old_info = info_rade
			i+=1
			print('First iteration')
		else:
			info_rade = reid()

			if info_rade == old_info:
				continue
			else:
				first_old_info = old_info[0]
				old_info = info_rade
				if first_old_info in info_rade:
					reversed_list = list(reversed(info_rade))
					reversed_list = reversed_list[reversed_list.index(first_old_info)+1:]
				else:
					reversed_list = info_rade

				for info in reversed_list:
					date = datetime.now()
					db.add_message_reid(date, info)
		time.sleep(5)

if __name__ == '__main__':
    add_mesage()