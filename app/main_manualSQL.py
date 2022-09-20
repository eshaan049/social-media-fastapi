# from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
# import psycopg2
# from psycopg2.extras import RealDictCursor# for getting column titles also coz it doesnt print column titles
# # by default
# import time

   
# class Post(BaseModel):# to start program we use: uvicorn app.main:app
#     title : str
#     content : str
#     published : bool = True# if nothing is specified from postman body then defaulted to True
#     # id : int

# app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',password='datta@2498', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#             print('Connecting to Database failed')
#             print('Error: ', error)
#             time.sleep(2)

# def id_check(id:int):
#     cursor.execute("""SELECT * FROM posts WHERE id=(%s);""", str(id))
#     data = cursor.fetchone()
#     return data

# @app.get('/')
# async def root():# in flask we use route func both are same tho
#     return {"message": "Hello Amma"}
    
# @app.get('/posts')
# def post_updates():
#     cursor.execute("""SELECT * FROM posts""")
#     data = cursor.fetchall()
#     return {'data': data}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def posting(msg:Post):# adds data to different id
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
#                    """, (msg.title, msg.content, msg.published)
#                   )
#     cursor.execute("""SELECT * FROM posts ORDER BY id DESC FETCH FIRST 1 ROW ONLY;""")
#     data = cursor.fetchall()
#     conn.commit()
#     return {"Post" : data}

# @app.get("/posts")
# def post_latest():
#     cursor.execute("""SELECT * FROM posts ORDER BY id DESC FETCH FIRST 1 ROW ONLY;""")
#     data = cursor.fetchone()
#     return {"latest": data}

# @app.get('/posts/{id}')
# def retrieve_posts(id : int, response : Response):
#     # id = int(id)# optional if we dont mention id:int in above func parameters
#     data = id_check(id)
#     if data == None:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return response.status_code
#     return {"data" : data}    

# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     data = id_check(id)
#     if data == None:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="None type cannot be deleted")
#     cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING * """, str(id))
#     cursor.execute("""SELECT * FROM posts""")
#     remaining_data = cursor.fetchall()
#     conn.commit()
#     return Response(status_code = status.HTTP_204_NO_CONTENT)

# @app.put('/posts/{id}')
# def update_posts(id:str, post:Post):# adds new data to the same id as prev whereas post adds data to different id
#     data = id_check(id)
#     if data == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} post doesnt exist")
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
#                    """, (post.title, post.content, post.published, id)
#                    )# SET we dont encapsulate using ' () ' rather we leave it as it is
#     cursor.execute("""SELECT * FROM posts""")
#     new_data = cursor.fetchall()
    
#     return {'message': new_data}