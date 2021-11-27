from sqlighter import SQLighter

db = SQLighter('db.db')


if __name__ == '__main__':
    subscriptions = db.get_subscriptions()
    print(f"id|user_id|status")
    for i in subscriptions:
        print(f"{i[0]}|{i[1]}|{i[2]}")