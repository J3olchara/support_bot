import psycopg2 as ps
import os


def admin_start():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print("-------------------------------ADMIN DATABASE CONNECTED-------------------------------")
    cur.execute("CREATE TABLE IF NOT EXISTS admins(admin_id INTEGER, username TEXT)")
    base.commit()
    return


async def add_new_admin(new_admin_id, username):
    cur.execute("INSERT INTO admins VALUES (%s, %s)", (new_admin_id, username))
    base.commit()
    return


async def take_admin_list():
    admin_list = [admin[0] for admin in cur.execute("SELECT admin_id FROM admins").fetchall()]
    return admin_list


async def delete_from_admin(admin_id):
    cur.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
    base.commit()
    return

async def safe_shutdown_admin():
    if base:
        base.commit()
    print("-------------------------------ADMIN DB SAVED-------------------------------")
    return
