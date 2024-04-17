import uvicorn
from fastapi import FastAPI, Request

from api.scraper import Vlr
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="VLRScraper",
    description="An Unofficial API for [vlr.gg](https://www.vlr.gg/), a site for Valorant Esports match and news "
    "coverage. ",
    docs_url="/",
    redoc_url=None,
)
vlr = Vlr()

TEN_MINUTES = 600

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/news")
@limiter.limit("250/minute")
async def VLR_news():
    return vlr.get_latest_data()



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001)
