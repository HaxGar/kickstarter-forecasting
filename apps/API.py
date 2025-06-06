from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def predict_api(kickstarterurl : str):
    return {"Hello": kickstarterurl}
