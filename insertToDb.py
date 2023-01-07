import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(name, img):
    try:
        sqliteConnection = sqlite3.connect('./face-recog', uri=True)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO users
                                  (Fullname, Image) VALUES (?, ?)"""

        userPhoto = convertToBinaryData(img)
        # Convert data into tuple format
        data_tuple = (name, userPhoto)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table: ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The sqlite connection is closed")

insertBLOB("Barack Obama", r"C:\Users\Natyra\Desktop\face-recognition-project\barackObama.jpg")
