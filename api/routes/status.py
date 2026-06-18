from fastapi import APIRouter, HTTPException
from api.database import get_job

router = APIRouter()

@router.get("/status/{job_id}")
def get_status(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "id": job["id"],
        "status": job["status"],
        "repo_url": job["repo_url"],
        "url": job["url"],
        "created_at": job["created_at"],
    }