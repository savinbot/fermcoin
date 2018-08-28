import sqlite3


def get_user(chat_id):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE chat_id=' + str(chat_id))
    row = c.fetchone()
    return row


def set_qiwi(chat_id, qiwi):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET qiwi=? WHERE chat_id=?', (qiwi, chat_id))
    conn.commit()


def set_ref(chat_id, num):
    if num == 10:   # level referal system
        return
    else:
        conn = sqlite3.connect('bot_users.db')
        c = conn.cursor()
        user = get_user(chat_id)
        c.execute('UPDATE users SET sent_ref=? WHERE chat_id=?', (user[3]+1, user[1]))
        c.execute('UPDATE users SET money=? WHERE chat_id=?', ((round(user[4] +  0.1, 1)), user[1]))
        conn.commit()
        if user[2] != None:
            set_ref(user[2], num + 1)
        else:
            return


def add_user_ref(chat_id, from_user):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (chat_id, from_ref) VALUES ('%s','%s')"%(chat_id, from_user))
        conn.commit()
        set_ref(from_user, 0)
    except:
        print('____\n', chat_id, 'add_user_ref')


def add_user(chat_id):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (chat_id) VALUES ('%s')"%(chat_id))
        conn.commit()
    except:
        print('____\n', chat_id, 'add_user')


def get_ref_lvl(chat_id):
    lvl_ref = []
    conn = sqlite3.connect('bot_users.db')
    c1 = conn.cursor()
    c2 = conn.cursor()
    c3 = conn.cursor()
    c4 = conn.cursor()
    c5 = conn.cursor()
    c6 = conn.cursor()
    c7 = conn.cursor()
    c8 = conn.cursor()
    c9 = conn.cursor()
    c10 = conn.cursor()

    for i in range(1, 11):
        name = 0
        lvl_ref.append(name)

    for row_1 in c1.execute('SELECT * FROM users WHERE from_ref=' + str(chat_id)):
        for row_2 in c2.execute('SELECT * FROM users WHERE from_ref=' + str(row_1[1])):
            for row_3 in c3.execute('SELECT * FROM users WHERE from_ref=' + str(row_2[1])):
                for row_4 in c4.execute('SELECT * FROM users WHERE from_ref=' + str(row_3[1])):
                    for row_5 in c5.execute('SELECT * FROM users WHERE from_ref=' + str(row_4[1])):
                        for row_6 in c6.execute('SELECT * FROM users WHERE from_ref=' + str(row_5[1])):
                            for row_7 in c7.execute('SELECT * FROM users WHERE from_ref=' + str(row_6[1])):
                                for row_8 in c8.execute('SELECT * FROM users WHERE from_ref=' + str(row_7[1])):
                                    for row_9 in c9.execute('SELECT * FROM users WHERE from_ref=' + str(row_8[1])):
                                        for row_10 in c10.execute('SELECT * FROM users WHERE from_ref=' + str(row_9[1])):
                                            lvl_ref[9] += 1
                                        lvl_ref[8] += 1
                                    lvl_ref[7] += 1
                                lvl_ref[6] += 1
                            lvl_ref[5] += 1
                        lvl_ref[4] += 1
                    lvl_ref[3] += 1
                lvl_ref[2] += 1
            lvl_ref[1] += 1
        lvl_ref[0] += 1

    print('____\n', chat_id, '\n', lvl_ref)
    return lvl_ref


def set_coin(chat_id):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    user = get_user(chat_id)
    c.execute('UPDATE users SET money=? WHERE chat_id=?', ((user[4] +  0.1), chat_id))
    c.execute('UPDATE users SET xbc=? WHERE chat_id=?', (1, chat_id))
    conn.commit()


def update_coin():
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    k = conn.cursor()
    for row in c.execute('SELECT * FROM users WHERE xbc=1'):
        k.execute('UPDATE users SET xbc=? WHERE chat_id=?', (0, row[1]))
    conn.commit()


def get_no_xbc():
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE xbc=0')
    rows = c.fetchall()
    return rows


def get_all():
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    rows = c.fetchall()
    return rows
