import json


if __name__ == '__main__':


    arr = []
    i = 0
    while(i<=58):
        task = {
            "task_key": "Index-" + str(i),
                "depends_on": [
                    {
                        "task_key": "Task1"
                    }
                ],
                "notebook_task": {
                    "notebook_path": "/Repos/joao.marcos@medway.com.br/analytics-produto-residencia/src/02-raw-archive/databricks/jobs/bronze/RA-BRO - Extração do Postgres",
                    "base_parameters": {
                        "index": i
                    },
                    "source": "WORKSPACE"
                },
                "existing_cluster_id": "0613-103649-53t94lff",
                "max_retries": -1,
                "min_retry_interval_millis": 900000,
                "retry_on_timeout": "false",
                "email_notifications": {}
        }

        arr.append(task)
        i = i + 1

    with open(f'task.json', 'w', encoding='utf-8') as f:
                json.dump(arr, f, ensure_ascii=False, indent=4)