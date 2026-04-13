import hmac
import os

from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, HttpUrl

from retriever import retrieve_cookies, walk_once

APP_SECRET = os.environ.get("APP_SECRET")
if not APP_SECRET:
    raise RuntimeError("APP_SECRET environment variable is required")

app = FastAPI(title="get-cookie")
security = HTTPBearer()


class WalkAction(BaseModel):
    action: Literal["wait"]
    value: int = 1000


class CookieRequest(BaseModel):
    url: HttpUrl
    actions: list[WalkAction] | None = None


class CookieResponse(BaseModel):
    cookies: str


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not hmac.compare_digest(credentials.credentials, APP_SECRET):
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/cookies", response_model=CookieResponse, dependencies=[Depends(verify_token)])
def get_cookies(body: CookieRequest):
    try:
        if body.actions:
            cookies = walk_once(
                str(body.url),
                [a.model_dump() for a in body.actions],
            )
        else:
            cookies = retrieve_cookies(str(body.url))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return CookieResponse(cookies=cookies)
    return CookieResponse(cookies=cookies)
