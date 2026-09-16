from fastapi import FastAPI, Form
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.static import PUBLIC_DIR

#from routers.router_example import router as example_router
from routers.user_router import router as user_router
from routers.shop_router import router as shop_router

# 서버 뿅 하고 완성 됨
app=FastAPI() # <- 서버 만드는 코드
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")
app.add_middleware(
    CORSMiddleware
    ,allow_origins=["*"]
    ,allow_credentials=True
    ,allow_methods=["*"]
    ,allow_headers=["*"]
)

#app.include_router(example_router,tags=["예제 API"])
#app은 서버. 라우터를 서버에 포함시키다. tag는 제목
app.include_router(user_router,tags=["유저 API"])
app.include_router(shop_router,tags=["쇼핑몰 API"])


# api endpoint, router, controller
@app.get("/") #주소 홈 포인터 http://127.0.0.1:8000/ <- 이거 ("/abc")면 8000/abc
def healthcheck():
    return {"success":True,"msg":"서버 건강함"}


if __name__=="__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000, # 3000~65000 중 맘대로 정함
        reload=True # ctrl + s 했을때 서버 자동으로 재시작
    )