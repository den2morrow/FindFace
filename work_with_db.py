import os
import sqlite3
import numpy as np
import face_recognition.api
import time
from PIL import Image

def main():
    s = f"{os.path.realpath(__file__)}".replace('\\', '/')
    s = s[:s.rfind('/')]
    db = sqlite3.connect(s + "/face_id.db")
    print('=' * 20 + ' Connected face_user_id.db ' + '=' * 20)
    c = db.cursor()

    c.execute("""CREATE TABLE user (
              name text,
              encodings text,
              image blob,
              imagePath text)""")
    print('=' * 20 + ' Created table user ' + '=' * 20)


    main_path = "C:/Users/N/PycharmProjects/FindFace/Photo_number_one"
    images = os.listdir("Photo_number_one")
    for image in images:

        nameFile = image.split('.')[0]
        path = main_path + '/' + image

        face_encod = face_recognition.face_encodings(face_recognition.load_image_file(path))[0]
        string_face_encod = face_encod.tostring()

        with open(path, 'rb') as file:
            blob_data = file.read()

            params = (nameFile, string_face_encod, blob_data, '')

            c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", params)
            print('=' * 20 + ' Add new user ' + '=' * 20)
    db.commit()
    db.close()

#Test
# start_time = time.time()
#
# db = sqlite3.connect("../face_id.db")
# c = db.cursor()
# c.execute("SELECT name, encodings, imagePath FROM user")
#
# test_path = r"/Photo_number_one/Денис_Томилов.jpg"
# test_img = face_recognition.load_image_file(test_path)
# test1_encod = face_recognition.face_encodings(test_img)
#
# encod_start = time.time()
# for one_person in c.fetchall():
#     name = one_person[0]
#     encod = np.fromstring(one_person[1])
#     imgPath = one_person[2]
#
#     result = face_recognition.compare_faces(encod, test1_encod)
#     if result[0]:
#         print(name)
#         print(imgPath)

    # print('=' * 200)
    # print('\n\n')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"ALL work time: {time.time() - start_time}")
