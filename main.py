from fastapi import FastAPI

from ProjectAnalyzer import ProjectAnalyzer

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/analyze_project/{proj_id}")
def read_item(proj_id):
    project_path = f"./{proj_id}"
    pa = ProjectAnalyzer(project_path)
    findings = pa.analyze_project()
    return findings
