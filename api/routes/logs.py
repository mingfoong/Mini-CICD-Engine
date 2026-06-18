from fastapi import APIRouter, HTTPException
from api.database import get_job

router = APIRouter()

@router.get("/logs/{job_id}")
def get_logs(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "id": job["id"],
        "status": job["status"],
        "logs": job["logs"]
    }