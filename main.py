from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ProjectAnalyzer import ProjectAnalyzer

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    context = {"request": request, "title": "Home Page", "username": "John Doe"}
    return templates.TemplateResponse(name="index.html", context=context, request=request)


@app.get("/analyze_project/{proj_id}")
def read_item(proj_id):
    project_path = f"./{proj_id}"
    pa = ProjectAnalyzer(project_path)
    findings = pa.analyze_project()
    return findings
