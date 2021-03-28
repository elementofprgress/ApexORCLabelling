import sqlite3
import os


def populateDatabase():
    root = r"D:\Git\ApexORCLabelling\static\images"
    records = []

    for dir0, dirs, ff in os.walk(root):
        for fname in ff:
            if fname[-4:] == ".png":
                fname.split(".")
                filename = fname[:-4]
                filename_base = fname.split(".", 1)[0]
                img_data = fname.split(".", 1)[1][:-4]
                pos_x, pos_y, pos_z = img_data.split(" ")
                values = (filename_base, filename, pos_x, pos_y, pos_z, None, None, None)
                records.append(values)
                print(fname, 0)

    try:
        sqliteConn = sqlite3.connect('images_database.db')
        cur = sqliteConn.cursor()
        cur.executemany('INSERT INTO apex_images VALUES(?,?,?,?,?,?,?,?);', records)
        sqliteConn.commit()
    except sqlite3.Error as e:
        print("Error while populating table", e)
    finally:
        if sqliteConn:
            sqliteConn.close()
            print("sqlite connection is closed")


# create a database and table for unverified images_test data
try:
    sqliteConnection = sqlite3.connect('images_database.db')
    sqlite_create_table_query = '''CREATE TABLE apex_images (
                                    filename_base TEXT, filename TEXT,
                                    pos_x TEXT, pos_y TEXT, pos_z TEXT,
                                    verify_pos_x TEXT,
                                    verify_pos_y TEXT,
                                    verify_pos_z TEXT);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite apex_images table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating apex_images table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")

# create a database table for verified images_test that contains their old file name and new file name based on verified cords
try:
    sqliteConnection = sqlite3.connect('images_database.db')
    sqlite_create_table_query = '''CREATE TABLE verified_apex_images (
                                    orig_filename TEXT, new_filename TEXT,
                                    orig_pos_x TEXT, orig_pos_y TEXT, orig_pos_z TEXT,
                                    new_pos_x TEXT, new_pos_y TEXT, new_pos_z TEXT);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite verified_apex_images table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating verified_apex_images table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")

populateDatabase()
print("done")
