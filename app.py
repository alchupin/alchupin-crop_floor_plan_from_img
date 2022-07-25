from imp import reload
from fastapi import FastAPI
import uvicorn

from starlette_validation_uploadfile import ValidateUploadFileMiddleware



from settings import settings
from api import router

app = FastAPI()
app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/crop-floor-plan/get-result",
        max_size=5048576
)
app.include_router(router)




if __name__ == '__main__':
    uvicorn.run("app:app", host=settings.server_host, port=settings.server_port, reload=True)