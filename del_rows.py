import time
from datetime import datetime
from sqlighter import SQLighter

db = SQLighter('db.db')


def delete_message_reid():
	while True:
		now = datetime.now().time()
		if (now.hour == 23) and (now.minute == 59):
			db.delete_message_reid()
			db.delete_message_vodokanal()
			print('удалено')
			time.sleep(120)

if __name__ == '__main__':
	delete_message_reid()