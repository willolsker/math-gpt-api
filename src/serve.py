from fastapi import FastAPI, Request
from solve import run_conversation

app = FastAPI()


@app.post("/v0/solve")
async def solve(request: Request):
    authorization = request.headers.get("Authorization")

    if authorization is None:
        return {"error": "No authorization header provided."}
    elif authorization != "Bearer 9W7WoHIYieOgLMInQX2Q":
        return {"error": "Invalid authorization header provided."}
    else:
        item = await request.json()
        return {"solution": run_conversation(item["problem"])}
