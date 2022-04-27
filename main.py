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
        cnnt = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='', cursor_factory=RealDictCursor)
        cursor = cnnt.cursor()
        print('Database connection was succesfull')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error: ', error)
        time.sleep(3)
        

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
           return p

    
def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        

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
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000) 
    my_posts.append(post_dict)
    return {'Data':post_dict}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
         msg_404(id)
    return {'Post detail':post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index == None:
       msg_404(id)
    my_posts.pop(index)
    return Response (status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index(id)
    if index == None:
       msg_404(id)
    post_dict = post.dict()    
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}
