from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount('/', StaticFiles(directory='public', html=True), name='static')


@app.get("/")
async def index():
    return FileResponse('index.html', media_type='text/html')

