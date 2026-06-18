import uuid
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from api.database import create_job
from api.workers.pipeline import run_pipeline

router = APIRouter()

class DeployRequest(BaseModel):
    repo_url: str

@router.post("/deploy")
def deploy(request: DeployRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())[:8]

    create_job(job_id, request.repo_url)
    background_tasks.add_task(run_pipeline, job_id, request.repo_url)

    return {"job_id": job_id, "status": "queued"}