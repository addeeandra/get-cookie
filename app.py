import hmac
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, HttpUrl

from retriever import retrieve_cookies

APP_SECRET = os.environ.get("APP_SECRET")
if not APP_SECRET:
    raise RuntimeError("APP_SECRET environment variable is required")

app = FastAPI(title="get-cookie")
security = HTTPBearer()


class CookieRequest(BaseModel):
    url: HttpUrl


class CookieResponse(BaseModel):
    cookies: str


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not hmac.compare_digest(credentials.credentials, APP_SECRET):
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/cookies", response_model=CookieResponse, dependencies=[Depends(verify_token)])
def get_cookies(body: CookieRequest):
    try:
        cookies = retrieve_cookies(str(body.url))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return CookieResponse(cookies=cookies)
