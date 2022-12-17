import mysql.connector
from mysql.connector.errors import IntegrityError
import os, io
import PIL.Image as Image
import base64

insert_query = 'INSERT INTO my_images VALUES (%s, %s)'
select_query = 'SELECT * FROM my_images WHERE username = %s'


connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Shyam@2004\\mysql',
    db = 'test'
)

def insert_image(username, filepath):
    try :
        username = username
        image_path = filepath
        image_bytes = ''
        with open(image_path, 'rb') as file:
            image_bytes = base64.b64encode(file.read())

        values = (username, image_bytes, )

        my_cur = connection.cursor()
        my_cur.execute(insert_query, values)

        my_cur.close()

        connection.commit()

        return True

    except IntegrityError :
        print('user already present in data base')
        return False

def read_image(username, save_path):
    username = username
    my_cur = connection.cursor()
    values = (username, )

    my_cur.execute(select_query, values)

    result = my_cur.fetchone()

    if result:
        image_source = result[1]
        image_bytes = base64.b64decode(image_source)
        img = Image.open(io.BytesIO(image_bytes))
        # img.show()
        img.save(save_path)
        return True

    else :
        print('Invalid user')
        return False

    my_cur.close()

    


if __name__ == '__main__' : 
    insert_image('pawan', 'static/uploads/img1.png')
    # read_image('pawan', 'current_img.png')