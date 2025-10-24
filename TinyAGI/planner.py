# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/planner.py

import json

class Planner:
    def __init__(self, agent_system):
        self.agent_system = agent_system
        self.tasks = []
        self.task_status = {}

    def create_plan(self, goal: str):
        """Creates a plan to achieve a goal."""
        prompt = f"""Create a plan to achieve the following goal: {goal}

The plan should be a list of tasks in JSON format. Each task should have the following fields:
- task_id: A unique identifier for the task.
- command: The command to execute.
- input: The input for the command.
- dependencies: A list of task IDs that this task depends on.

Here is an example of a plan:
[
    {{
        "task_id": "1",
        "command": "generate",
        "input": {{
            "prompt": "Write a poem about a cat."
        }},
        "dependencies": []
    }},
    {{
        "task_id": "2",
        "command": "save_to_file",
        "input": {{
            "filename": "poem.txt",
            "content": "{{{{tasks.1.output}}}}"
        }},
        "dependencies": ["1"]
    }}
]"""
        response = self.agent_system.chat(prompt)
        self.tasks = json.loads(response)
        for task in self.tasks:
            self.task_status[task['task_id']] = 'pending'

    def get_runnable_tasks(self):
        """Gets a list of tasks that can be executed in parallel."""
        runnable_tasks = []
        for task in self.tasks:
            if self.task_status[task['task_id']] == 'pending':
                dependencies_met = True
                for dep_id in task['dependencies']:
                    if self.task_status.get(dep_id) != 'completed':
                        dependencies_met = False
                        if self.task_status.get(dep_id) == 'failed':
                            self.update_task_status(task['task_id'], 'failed')
                        break
                if dependencies_met:
                    runnable_tasks.append(task)
        return runnable_tasks

    def update_task_status(self, task_id: str, status: str):
        """Updates the status of a task."""
        self.task_status[task_id] = status
