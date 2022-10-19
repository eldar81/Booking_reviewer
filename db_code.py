import sqlite3


def create_db():
    try:
        sqlite_connection = sqlite3.connect('db.db', check_same_thread=False)
        create_table = '''CREATE TABLE hotels(
                       id TEXT,
                       rendered int DEFAULT 0 NOT NULL,
                       uploaded int DEFAULT 0 NOT NULL,
                       link TEXT,
                       country TEXT,
                       city TEXT,
                       district TEXT,
                       hotel TEXT,
                       stars int,
                       rating int,
                       price int,
                       currency TEXT,
                       airport TEXT,
                       airport_dist int,
                       description TEXT,
                       img1 TEXT,
                       img2 TEXT,
                       img3 TEXT,
                       img4 TEXT,
                       img5 TEXT,
                       img6 TEXT,
                       img7 TEXT,
                       img8 TEXT,
                       img9 TEXT,
                       img10 TEXT,
                       img11 TEXT,
                       img12 TEXT,
                       img13 TEXT,
                       img14 TEXT,
                       img15 TEXT,
                       img16 TEXT,
                       img17 TEXT,
                       img18 TEXT,
                       img19 TEXT,
                       img20 TEXT,
                       img21 TEXT,
                       img22 TEXT,
                       img23 TEXT,
                       img24 TEXT,
                       img25 TEXT,
                       img26 TEXT,
                       img27 TEXT,
                       img28 TEXT,
                       img29 TEXT,
                       img30 TEXT,
                       PRIMARY KEY(id)
                       );
    '''
        cursor = sqlite_connection.cursor()
        cursor.execute(create_table)
        print("База данных создана")
        record = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print(error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()


def write_ids_links_prices(data):
    try:
        conn = sqlite3.connect('db.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('INSERT INTO hotels(id, link, price, currency) VALUES(?, ?, ?, ?);', data)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e, data[0])


def get_links_from_db():
    conn = sqlite3.connect('db.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT link FROM hotels WHERE hotel is NULL ')
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data


def write_data_to_db(column, data, hotel_id):
    try:
        conn = sqlite3.connect('db.db', check_same_thread=False)
        c = conn.cursor()
        c.execute(f'UPDATE hotels SET {column}=? WHERE id=?', (data, hotel_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'Значение {column} не записано: {e}')


def get_hotel_data_from_db(where_column, data):
    try:
        conn = sqlite3.connect('db.db', check_same_thread=False)
        c = conn.cursor()
        c.execute(f'SELECT county, city, district, hotel, stars, rating, price, currency, airport, '
                  f'airport_dist, description FROM hotels WHERE {where_column}=?', (data,))
        outcome = c.fetchone()
        conn.commit()
        conn.close()
        return outcome
    except Exception as e:
        print(e)


def write_imgs_to_db(data, hotel_id):
    img_colunm = 'img1'
    n = 1
    for link in data:
        try:
            conn = sqlite3.connect('db.db', check_same_thread=False)
            c = conn.cursor()
            c.execute(f'UPDATE hotels SET {img_colunm}=? WHERE link=?', (link, hotel_id))
            conn.commit()
            conn.close()
            n +=1
            img_colunm = 'img'+f'{n}'
        except Exception as e:
            print(e)


def write_whole_data_to_db(data):
    try:
        conn = sqlite3.connect('db.db', check_same_thread=False)
        c = conn.cursor()
        c.execute(f'''UPDATE hotels SET county=?,
         city=?,
         district=?,
         stars=?,
         rating=?,
         airport=?,
         airport_dist=?,
         hotel=?,
         description=?,
         img1=?,
         img2=?,
         img3=?,
         img4=?,
         img5=?,
         img6=?,
         img7=?,
         img8=?,
         img9=?,
         img10=?,
         img11=?,
         img12=?,
         img13=?,
         img14=?,
         img15=?,
         img16=?,
         img17=?,
         img18=?,
         img19=?,
         img20=?,
         img21=?,
         img22=?,
         img23=?,
         img24=?,
         img25=?,
         img26=?,
         img27=?,
         img28=?,
         img29=?,
         img30=?
         WHERE link=?''', data)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'Ошибка: {e}')


def get_all_imgs(hotel_id):
    try:
        conn = sqlite3.connect('db.db', check_same_thread=False)
        c = conn.cursor()
        c.execute(f'SELECT img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, img11, img12, img13, img14, '
                  f'img15, img16, img17, img18, img19, img20, img21, img22, img23, img24, img25, img26, img27, '
                  f'img28, img29, img30 FROM hotels WHERE id=?', (hotel_id,))
        outcome = c.fetchone()
        conn.commit()
        conn.close()
        return outcome
    except Exception as e:
        print(e)


def get_n_imgs(n, hotel_id):
    try:
        column_list = []
        while n != 0:
            column_list.append(f'img{n}')
            n -= 1
        column_list.reverse()
        column_list = str(column_list).replace('[', '').replace(']', '').replace("'", '')
        conn = sqlite3.connect('db.db', check_same_thread=False)
        c = conn.cursor()
        c.execute(f'SELECT {column_list} FROM hotels WHERE id=?', (hotel_id,))
        outcome = c.fetchone()
        conn.commit()
        conn.close()
        return outcome
    except Exception as e:
        print(e)


def get_hotels_to_render(county):
    conn = sqlite3.connect('db.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT id FROM hotels WHERE uploaded=0 and county=? ', (county,))
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data
