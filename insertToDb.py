import sqlite3

def stringToLowercase(name):
    nameStr = "".join(name.split(' '))
    return nameStr.lower()

def convertToBinaryData(filename):
    # Konverto te dhenat digjitale ne formatin binar
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
        # Konverto te dhenat ne formatin tuple
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

	
users = ["Ideja Ferati", "Jeta Kajtazi", "Jete Lajqi"]
for user in users:
    insertBLOB(user, "./" +  stringToLowercase(user) + ".jpg")
