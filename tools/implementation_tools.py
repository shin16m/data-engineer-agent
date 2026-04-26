def task_entry(task_id: str, description: str, owner: str) -> dict:
    return {
        "task_id": task_id,
        "description": description,
        "owner": owner,
    }

