import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application.init_routers import init_routers

app = FastAPI(title='toolbox_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_routers(app,'application/routers')

if __name__=='__main__':
    uvicorn.run(app)
