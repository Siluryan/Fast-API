from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


while True:
    try:
        cnnt = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='******', cursor_factory=RealDictCursor)
        cursor = cnnt.cursor()
        print('Database connection was succesfull')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error: ', error)
        time.sleep(3)


def msg_404(id):    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Id:{id} does not exist')
    

@app.get('/')
def root():    
    return {'Index': 'Main'}
    

@app.get('/posts')
def app_get():
    cursor.execute('''SELECT * FROM posts ''')
    posts = cursor.fetchall()
    
    return {'Data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''',
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    cnnt.commit()
    
    return {'Data':new_post}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id),))
    post = cursor.fetchone()
    if not post:
         msg_404(id)
    
    return {'Post detail':post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING*''', (str(id),))
    delete_post = cursor.fetchone()
    cnnt.commit()
    if delete_post == None:
       msg_404(id)
    
    return Response (status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''',
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    cnnt.commit()
    if updated_post == None:
       msg_404(id)
    
    return {"data":updated_post}
