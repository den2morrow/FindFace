import os.path
import time
import sqlite3
import numpy as np
import face_recognition

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton

from plyer import filechooser
from plyer import camera


class Logic:

    def __init__(self, path):
        self.path = path


    def select_db(self):
        s = f"{os.path.realpath(__file__)}".replace('\\', '/')
        s = s[:s.rfind('/')]
        db = sqlite3.connect(s + '/face_id.db')
        print("connect db")
        c = db.cursor()
        c.execute("SELECT name, encodings, imagePath FROM user;")
        print("Cursor execute")
        return c.fetchall()




    def face_rec(self):
        path = self.path
        img = face_recognition.load_image_file(path)
        encod_img = face_recognition.face_encodings(img)


        database = self.select_db()
        results = []
        for one_person in database:
            name = one_person[0]
            encod = np.fromstring(one_person[1])
            # I change database. When app start first time path of image added to database
            imgPath = one_person[2]

            try:
                result = face_recognition.compare_faces(encod, encod_img, tolerance=0.5)
            except ValueError as e:
                raise ValueError
            if result[0]:
                results.append([result[0], name, imgPath])


        return results


class BxLayout(BoxLayout):
    name = 'Имя: '

    def __init__(self, **kwargs):
        super(BxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Name
        self.label_name = Label(text=self.name, color=(0, 1, 0, 1), font_size=20, size_hint_y=0.3)
        self.add_widget(self.label_name)

        # Image visual
        image_layout = BoxLayout(orientation='vertical', padding=10)

        image_bx1 = BoxLayout(orientation='horizontal')
        self.image_1 = Image(size_hint=(1, 1), height=200, allow_stretch=True, keep_ratio=True)
        image_bx1.add_widget(self.image_1)
        image_layout.add_widget(image_bx1)

        image_bx2 = BoxLayout(orientation='horizontal')
        self.image_2 = Image(size_hint=(1, 1), height=200, allow_stretch=True, keep_ratio=True)
        image_bx2.add_widget(self.image_2)
        image_layout.add_widget(image_bx2)

        self.add_widget(image_layout, 1)

        # Button
        photo_layout1 = GridLayout(cols=2, size_hint_y=None, height=100, padding=5, spacing=10)
        photo_layout1.add_widget(Button(text='Сделать фото', on_press=self.create_image, size_hint_x=100, width=150))
        photo_layout1.add_widget(Button(text='Загрузить фото', on_press=self.select_image, size_hint_x=100, width=150))
        self.add_widget(photo_layout1)
        photo_layout2 = BoxLayout(size_hint_y=None, height=100, padding=5)
        photo_layout2.add_widget(Button(text='Старт', on_press=self.start_rec, size_hint_x=100, width=150))
        self.add_widget(photo_layout2)


    def select_image(self, instance):
        try:
            photos = filechooser.open_file(title="Select photos", filters=[("Images", "*.jpg;*.jpeg;*.png")], multiple=True)
            photos = photos[0].replace('\\', '/')
            self.image_1.source = photos
        except IndexError as e:
            print(f'Error: {e}')

    def create_image(self, instance):
        try:
            filename = camera.take_picture('test.png', 'test.png')
            print("Фото сохранено в {}".format(filename))
        except NotImplementedError:
            print("Функция сделать фото не поддерживается на данной платформе")

    def start_rec(self, instance):
        try:
            logic = Logic(self.image_1.source)
            try:
                result = logic.face_rec()

                path_img_results = []
                name_result = ''
                for res in result:
                    name_result += res[1] + '\n             или\n'
                    # res[2] --> res[3]
                    path_img_results.append(res[2])
                name_result = name_result[:-18]

                if name_result != '':
                    self.label_name.text = name_result
                    self.image_2.source = path_img_results[0]
                else:
                    self.label_name.text = 'Нет такого лица в базе.'
                    self.image_2.source = ''
            except Exception as e:
                print(f"Error: {e}")


        except IndexError as e:
            self.label_name.text = 'Обработка завершилась с ошибкой ;(' # На фото нет лиц
            print(f'Error: {e}')
        except ValueError as e:
            self.label_name.text = 'Проблема с размерностью ;(' # Фото не могут быть сравнены


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        actionbar = ActionBar()
        actionview = ActionView()
        actionbar.add_widget(actionview)

        action_previous = ActionPrevious(title='Меню', with_previous=False, app_icon="icon.png")
        actionview.add_widget(action_previous)

        action_button_1 = ActionButton(text='Начать')
        action_button_1.bind(on_press=self.goto_logic_menu)
        actionview.add_widget(action_button_1)

        layout.add_widget(actionbar)

        return layout

    def goto_logic_menu(self, instance):
        if os.path.isdir("db_data"):
            pass
        else:
            os.mkdir("db_data")
            s = f"{os.path.realpath(__file__)}".replace('\\', '/')
            s = s[:s.rfind('/')]
            db = sqlite3.connect(s + '/face_id.db')
            c = db.cursor()

            c.execute("SELECT name, image FROM user;")
            for one_person in c.fetchall():
                name = one_person[0]
                photo = one_person[1]
                photo_path = os.path.join(f"db_data/{name}" + ".png")
                with open(photo_path, 'wb') as file:
                    file.write(photo)
                c.execute("UPDATE user SET imagePath = (?) WHERE name = (?);", (photo_path, name))

            db.commit()
            db.close()

        bx = BxLayout()
        self.root.clear_widgets()
        self.root.add_widget(bx)



if __name__ == '__main__':
    MyApp().run()
