from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.core.config import TEMPLATES_DIR

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/rag")
async def rag(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="rag.html",
        context={"title": "RAG"},
    )
