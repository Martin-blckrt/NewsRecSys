from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uvicorn import run

from constants import HOST, PORT
from rl_model import Model

app = FastAPI()
model = Model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NewsClick(BaseModel):
    url: str


@app.get('/login/{user_id}')
def create_model(user_id: str) -> None:
    model.login_user(user_id, local=False)


@app.get('/recommend-news/{user_id}')
def recommend_news(user_id: str):
    # l'user_id n'est plus là car on l'a déjà grâce au login
    recommended = model.recommend_news(user_id)
    print(recommended)
    df = recommended[['source', 'title', 'image', 'description', 'url']]
    json_obj = df.to_json(orient='records')

    return JSONResponse(content=json_obj)


@app.post('/response/')
def get_user_response(news_click: NewsClick):
    model.get_user_response(news_click.url)

    return JSONResponse(content="ok")


"""
Scénar Pipeline A -> Z

model = Model()
model.login_user("0", local=False)
recommended = model.recommend_news()
user_choice = recommended.iloc[0]['url']
model.get_user_response(user_choice)
# go again
model.recommend_news()

"""
"""
Scénar qualité de recommandation

model = Model()
model.login_user("0", local=False)
choices = []
while True:
    recommended = model.recommend_news()
    print(recommended)
    print("You already choose:", *choices)
    user = input("Choose ID (nb, not url): ")
    choices.append(user)
    url = recommended.loc[recommended['id'] == user]['url'].values[0]
    model.get_user_response(url)
"""

if __name__ == '__main__':
    # run(app=app, host=HOST, port=PORT)

    # when app turns off, save history
    # model.quit()
    model = Model()
    recommended = model.recommend_news("0")
    print(recommended)
    choices = []
    while True:
        print("You already chose:", *choices)
        user = input("Choose ID : ")
        if user == "-1":
            model.quit()
            recommended = model.recommend_news("0")
            print(recommended)
            choices = []
        else:
            choices.append(user)
            url = recommended.loc[recommended['id'] == user]['url'].values[0]
            model.get_user_response(url)

    print("\nEnd of the program, thx bye bye")
