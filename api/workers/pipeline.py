import os
import docker
import socket
import shutil
from git import Repo
from api.config import WORKDIR, DEPLOY_HOST, PORT_RANGE_START, PORT_RANGE_END
from api.database import update_job, append_log

client = docker.from_env()

def clone_repo(job_id: str, repo_url: str) -> str:
    job_path = os.path.join(WORKDIR, job_id)

    if os.path.exists(job_path):
        shutil.rmtree(job_path)

    os.makedirs(job_path, exist_ok=True)

    append_log(job_id, f"Cloning {repo_url}...")
    Repo.clone_from(repo_url, job_path)
    append_log(job_id, "Clone Complete.")

    return job_path


def build_image(job_id: str, job_path: str) -> str:
    dockerfile_path = os.path.join(job_path, "Dockerfile")

    if not os.path.exists(dockerfile_path):
        raise FileNotFoundError("No Dockerfile found in repository.")

    image_tag = f"mini-paas-{job_id}"

    append_log(job_id, "Building Docker Image...")
    image, build_logs = client.images.build(path=job_path, tag=image_tag)

    for chunk in build_logs:
        if "stream" in chunk:
            line = chunk["stream"].strip()
            if line:
                append_log(job_id, line)

    append_log(job_id, "Build Complete.")
    return image_tag


def find_free_port():
    for port in range(PORT_RANGE_START, PORT_RANGE_END):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    raise RuntimeError("No free port available.")


def run_container(job_id: str, image_tag: str) -> dict:
    port = find_free_port()

    append_log(job_id, f"Starting container on port {port} ...")
    container = client.containers.run(
        image_tag,
        detach = True,
        ports = {"3000/tcp": port},
        name = f"mini-paas-{job_id}",
    )

    url = f"http://{DEPLOY_HOST}:{port}"
    append_log(job_id, f"Deployed at {url}")

    return {"port": port, "url": url, "container_id": container.id}


def run_pipeline(job_id: str, repo_url: str):
    try:
        update_job(job_id, status="cloning")
        job_path = clone_repo(job_id, repo_url)

        update_job(job_id, status="building")
        image_tag = build_image(job_id, job_path)

        update_job(job_id, status="deploying")
        result = run_container(job_id, image_tag)

        update_job(
            job_id,
            status="running",
            port=result["port"],
            url=result["url"],
        )

    except Exception as e:
        append_log(job_id, f"Error: {str(e)}")
        update_job(job_id, status="failed")