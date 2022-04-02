import psycopg2 as ps
import os


def users_start():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print("-------------------------------USERS DATABASE CONNECTED-------------------------------")
    cur.execute("CREATE TABLE IF NOT EXISTS userlist(user_id INTEGER, user_state INTEGER, activity TEXT)")
    base.commit()
    return


async def take_activity(user_id):
    activity = cur.execute("SELECT activity from userlist WHERE user_id = %s", (user_id,)).fetchone()[0]
    base.commit()
    return activity


async def change_activity_to_active(user_id):
    activity = await take_activity(user_id=user_id)
    if activity == "inactive":
        cur.execute("UPDATE userlist SET activity = %s WHERE user_id = %s", ("active", user_id))
    base.commit()


async def change_activity_to_inactive(user_id):
    activity = await take_activity(user_id=user_id)
    if activity == "active":
        cur.execute("UPDATE userlist SET activity = %s WHERE user_id = %s", ("active", user_id))
    base.commit()


async def users_list():
    user_list = [user_id[0] for user_id in cur.execute("SELECT user_id FROM userlist").fetchall()]
    base.commit()
    return user_list


def add_new_user(user_id, user_state=1, activity="inactive"):
    cur.execute("INSERT INTO userlist VALUES(%s, %s, %s)", (user_id, user_state, activity))
    base.commit()
    return


async def take_user_info(user_id):
    user_info = cur.execute("SELECT * FROM userlist WHERE user_id = %s", (user_id,)).fetchone()
    base.commit()
    return user_info


async def update_user_state(user_id):
    user_info = await take_user_info(user_id)
    user_state = user_info[1]
    if user_state < 5:
        new_user_state = user_state + 1
        cur.execute("UPDATE userlist SET user_state = %s WHERE user_id = %s", (new_user_state, user_id))
        base.commit()
        return
    else:
        return


async def take_user_state(user_id):
    user_state = cur.execute("SELECT user_state FROM userlist WHERE user_id = %s", (user_id,)).fetchone()[0]
    base.commit()
    return user_state


async def safe_shutdown_users():
    if base:
        base.commit()
    print("-------------------------------USERS DB SAVED-------------------------------")
