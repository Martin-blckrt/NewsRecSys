from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

    model.login_user(user_id, local=False)


@app.get('/recommend-news/{user_id}')
def recommend_news(user_id: str):
    model.login_user(user_id, local=False)
    print("user loggedid")
    # l'user_id n'est plus là car on l'a déjà grâce au login
    recommended = model.recommend_news()
    print(recommended)
    df = recommended[['source', 'title', 'image', 'description', 'url']]
    json_obj = df.to_json(orient='records')

    return JSONResponse(content=json_obj)


@app.get('/response/{user_response}')
def get_user_response(user_response: str) -> None:
    # for now, user response = id de la news cliquée
    model.get_user_response(user_response)


if __name__ == '__main__':
    run(app=app, host=HOST, port=PORT)
    model.env.synchronize_history(model.user_id)

    #model = Model()
    #model.login_user("0", local=False)
    #recommended = model.recommend_news()
    #df = recommended[['source', 'title', 'image', 'description', 'url']]

    # Convert the dataframe to a JSON object
    #json_obj = df.to_json(orient='records')
    #print(recommended.iloc[0])

    # rl = input()
    # model.get_user_response(rl)
    # model.recommend_news()
    # when app turns off, save history
    #
    print("\nEnd of the program, thx bye bye")
