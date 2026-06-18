import threading

_lock = threading.Lock()

_jobs: dict = {}

def create_job(job_id: str, repo_url: str) -> dict:
    job = {
        "id": job_id,
        "repo_url": repo_url,
        "status": "queued",
        "port": None,
        "url": None,
        "logs": [],
        "created_at": __import__("datetime").datetime.utcnow().isoformat()
    }
    with _lock:
        _jobs[job_id] = job
    return job

def get_job(job_id: str) -> dict | None:
    return _jobs.get(job_id)

def update_job(job_id: str, **kwargs):
    with _lock:
        if job_id in _jobs:
            _jobs[job_id].update(kwargs)

def append_log(job_id: str, line: str):
    with _lock:
        if job_id in _jobs:
            _jobs[job_id]["logs"].append(line)

def all_jobs() -> dict:
    return list(_jobs.values())