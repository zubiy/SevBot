import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def add_message_reid(self, date, message):
        with self.connection:
            return self.cursor.execute("INSERT INTO `info_rade` (`date`, `message`) VALUES(?,?)", (date,message))

    def update_message_reid_is_send(self, is_send, id_post):
        with self.connection:
            return self.cursor.execute("UPDATE `info_rade` SET `is_send` = ? WHERE `id` = ?", (is_send, id_post))

    def get_reid_date(self, date):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM info_rade WHERE `date`> '{date} 00:00:00' and `date`< '{date} 23:59:59'")

    def get_vodakanal_date(self, date):
        with self.connection:
            return self.cursor.execute(
                f"SELECT * FROM info_vodakanal WHERE `date`> '{date} 00:00:00' and `date`< '{date} 23:59:59'")

    def get_message_reid(self, status = False):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `info_rade` WHERE `is_send` = ?", (status,)).fetchall()

    def delete_message_reid(self):
        sql_delete_query = """DELETE from info_rade"""
        with self.connection:
            return self.cursor.execute(sql_delete_query)

    def add_message_vodakanal(self, date, message):
        with self.connection:
            return self.cursor.execute("INSERT INTO `info_vodakanal` (`date`, `info_vod`) VALUES(?,?)", (date,message))

    def update_message_vodakanal_is_send(self, is_send, id_post):
        with self.connection:
            return self.cursor.execute("UPDATE `info_vodakanal` SET `is_send_msg` = ? WHERE `id` = ?", (is_send, id_post))

    def get_message_vodokanal(self, status = False):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `info_vodakanal` WHERE `is_send_msg` = ?", (status,)).fetchall()

    def delete_message_vodokanal(self):
        sql_delete_query = """DELETE from info_vodakanal"""
        with self.connection:
            self.cursor.execute(sql_delete_query)

    def close(self):
        self.connection.close()