import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import status

from .img_processing import cut_floor_plan_from_image

router = APIRouter(
    prefix='/crop-floor-plan',
)

templates = Jinja2Templates(directory="templates")


@router.post("/get-result")
def submit(file: UploadFile = File(...)):
    if file.filename.split('.')[-1] != 'jpg':
        return RedirectResponse(
            '/crop-floor-plan',
            status_code=status.HTTP_302_FOUND)
    
    with open(f'{file.filename}', "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    result_file = cut_floor_plan_from_image(file.filename)

    return FileResponse(path=result_file, filename=result_file)
    

@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
