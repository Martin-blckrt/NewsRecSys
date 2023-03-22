from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


@app.get('/login/{user_id}')
def create_model(user_id: str) -> None:
    model.login_user(user_id, local=True)


@app.get('/recommend-news/')
def recommend_news() -> dict:
    # l'user_id n'est plus là car on l'a déjà grâce au login
    recommended = model.recommend_news()
    return {
        'news': recommended
    }


@app.get('/response/{user_response}')
def get_user_response(user_response: str) -> None:
    # for now, user response = id de la news cliquée
    model.get_user_response(user_response)


if __name__ == '__main__':
    #run(app=app, host=HOST, port=PORT)

    model = Model()
    model.login_user("0", local=False)
    # do stuff

    # when app turns off, save history
    #model.env.synchronize_history(model.user_id)
    print("End of the program, thx bye bye")
