from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import deploy, status, logs
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Mini PaaS")
app.mount("/dashboard", StaticFiles(directory="dashboard", html=True), name="dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deploy.router)
app.include_router(status.router)
app.include_router(logs.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/deployments")
def list_deployments():
    from api.database import all_jobs
    return all_jobs()
