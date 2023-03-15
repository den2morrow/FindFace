import time
import face_recognition
from PIL import Image



def extracting_faces(img_path):
    count = 0
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_locations in faces_locations:
        top, right, bottom, left = face_locations

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"found_faces/{count}_face_img.jpg")
        count += 1
    return "found_faces/"




def main():
    img = face_recognition.load_image_file(r"C:\Users\N\PycharmProjects\FindFace\faces_for_test_create_db\Denis_Tomilov1.jpg")
    print(face_recognition.face_encodings(img))

if __name__ == '__main__':
    start_time = time.time()
    main()
    finish_time = time.time()
    print(f"Work time: {finish_time - start_time} sec")



#Stuff
# def add_db(img_path):
#     img = face_recognition.load_image_file(img_path)
#     img_encod = face_recognition.face_encodings(img)[0]
#     img_name = img_path.split('\\')[-1].split('.')[0]
#     data = {
#         img_encod.tostring(): [
#             f"{img_name}",
#             img_path
#         ]
#     }
#
#     pass

#About example file
# data = {
#     img_encodings: [
#         f"{name}",
#         "img_path"
#     ]
# }

# Запросы можно сделать через data.get(img_encodings) -> Если выйдет, то скорость будет ошеломляющей
# Иначе уже буду делать через перебор (пока такая рабочая версия)
# Запросы будут к data.keys() -> То есть я смогу пройтись по лицевым признакам через такую лаконичную функцию