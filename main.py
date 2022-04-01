from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

my_posts = []


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get('/')
def root():
    return {'Index': 'Main'}
    

@app.get('/posts')
def app_get():
    return {'Data': my_posts}


@app.post('/posts')
def app_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000) 
    my_posts.append(post_dict)
    return {'Data':post_dict}


@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {'Post detail':post}
