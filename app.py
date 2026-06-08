from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the Coins API"}

@app.get("/coins")
def list_coins():
    return []