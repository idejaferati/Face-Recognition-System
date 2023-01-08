import face_recognition
import cv2
import numpy as np
import sqlite3

def stringToLowercase(name):
    nameStr = "".join(name.split(' '))
    return nameStr.lower()

def writeTofile(data, filename):
    # Konverto te dhenat binare ne formatin adekuat dhe shkruaji ne Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(fullname):
    try:
        sqliteConnection = sqlite3.connect('./face-recog', uri=True)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from users where Fullname = ?"""
        cursor.execute(sql_fetch_blob_query, (fullname,))
        record = cursor.fetchall()
        for row in record:
            print("Name = ", row[0])
            name = row[0]
            photo = row[1]

            print("Storing user image locally \n")
            photoPath = "./" +  stringToLowercase(name) + ".jpg"
            writeTofile(photo, photoPath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table: ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Sqlite connection is closed")

users = ["Ideja Ferati", "Jeta Kajtazi", "Jete Lajqi"]


# Krijimi i vargjeve me kodim te fytyrave te njohura dhe emrave perkates
known_face_encodings = []
known_face_names = []

for user in users:
    readBlobData(user)
    # Ngarkimi i fotos
    user_image = face_recognition.load_image_file("./" +  stringToLowercase(user) + ".jpg")
    user_face_encoding = face_recognition.face_encodings(user_image)[0]
    known_face_encodings.append(user_face_encoding)
    known_face_names.append(user)

# Inicializimi i disa variablave
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


capture = cv2.VideoCapture(0)

while True:
    
    # Marrja e nje frame-i (kornize) te vetme te videos
    ret, frame = capture.read()

    # Ndryshimi i permasave te videos ne 1/4 e permases, per procesim me te shpejte te njohjes se fytyres
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Konvertimi i fotos nga ngjyra BGR (qe e perdod OpenCV) ne ngjyra RGB (qe i perdor face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Perpunimi i cdo frame-i (kornize) tjeter te videos 
    if process_this_frame:
        # Gjetja e cdo fytyre ne kuadrin aktual te videos 
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Shiko nese fytyra pershtatet me fytyrat e njohura
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # Nese gjendet nje pershtatje ne known_face_encodings, perdor te paren.
            # if True ne matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Perndryshe, perdor fytyren e njohur me distancen me te vogel nga fytyra e re
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    
    # Shfaq rezultatet
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Vizato nje kuti rreth fytyres
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Vizato nje label me emer poshte fytyres
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 4, bottom - 4), font, 1, (0,0,255), 2)


    # Shfaq imazhin rezultues
    cv2.imshow('Image', frame)

    # Shtyp 'q' ne tastiere per te perfunduar!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ndalja e kameres
capture.release()
cv2.destroyAllWindows()
