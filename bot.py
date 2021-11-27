import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from datetime import datetime
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

db = SQLighter('db.db')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	if (not db.subscriber_exists(message.from_user.id)):
		db.add_subscriber(message.from_user.id)
	else:
		db.update_subscription(message.from_user.id, True)

	await message.answer("Вы успешно подписались на рассылку!\n")

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if (not db.subscriber_exists(message.from_user.id)):
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		db.update_subscription(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")


@dp.message_handler(commands=['reid'])
async def reid_info(message: types.Message):
	current_date = str(datetime.now().date())
	reid_msg = db.get_reid_date(current_date)
	print(reid_msg)
	if reid_msg:
		for info in reid_msg:
			await bot.send_message(message.from_user.id, info[2])
	else:
		await bot.send_message(message.from_user.id, 'Нет актуальной информации')

@dp.message_handler(commands=['vodokanal'])
async def vodakanal_info(message: types.Message):
	current_date = str(datetime.now().date())
	vodakanal_msg = db.get_vodakanal_date(current_date)
	if vodakanal_msg:
		for info in vodakanal_msg:
			await bot.send_message(message.from_user.id, info[2])
	else:
		await bot.send_message(message.from_user.id, 'Нет актуальной информации')

async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		reid_msg = db.get_message_reid()
		vodokanal_msg = db.get_message_vodokanal()
		subscriptions = db.get_subscriptions()
		for info in reid_msg:
			for s in subscriptions:
				await bot.send_message(s[1], info[2])
			db.update_message_reid_is_send(True, info[0])
		for info_vod in vodokanal_msg:
			for s in subscriptions:
				await bot.send_message(s[1], info_vod[2])
			db.update_message_vodakanal_is_send(True, info_vod[0])
if __name__ == '__main__':
	#threading.Thread(target=add_mesage)
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(1))
	#loop.create_task(delete_message_reid())
	executor.start_polling(dp, skip_updates=True)