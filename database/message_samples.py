from .users import take_user_state
import psycopg2 as ps
import os


def message_samples_start():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print("-------------------------------SAMPLES DATABASE CONNECTED-------------------------------")
    cur.execute("CREATE TABLE IF NOT EXISTS message_samples(sample_id INTEGER PRIMARY KEY, sample TEXT)")
    base.commit()
    return


async def add_new_sample(sample_id, sample):
    cur.execute("INSERT INTO message_samples VALUES(%s, %s)", (sample_id, sample))
    base.commit()
    return


async def take_user_sample(user_id):
    user_state = await take_user_state(user_id)
    sample = cur.execute("SELECT sample FROM message_samples WHERE sample_id = %s", (user_state,)).fetchone()
    base.commit()
    return sample


async def take_all_samples():
    sample_list = cur.execute('SELECT * FROM message_samples').fetchall()
    base.commit()
    return sample_list


async def deleting_sample(sample_id):
    cur.execute("DELETE FROM message_samples WHERE sample_id = %s", (sample_id,))
    base.commit()
    return


async def safe_shutdown_message_samples():
    if base:
        base.commit()
    print("-------------------------------SAMPLES DB SAVED-------------------------------")
