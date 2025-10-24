# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/run.py

import json
from rich.console import Console
from rich.prompt import Prompt
from TinyAGI.agent import AgentSystem
from .base_command import BaseCommand
from TinyAGI.task_manager import TaskManager
from ..command_manager import CommandManager
from ..command_executor import CommandExecutor

console = Console()

class RunCommand(BaseCommand):
    """Command to run a high-level goal."""

    @property
    def name(self) -> str:
        return "run"

    @property
    def description(self) -> str:
        return "Run a high-level goal."

    def execute(self, agent_system: AgentSystem, args: list = None):
        """Executes the run command."""
        if not args:
            goal = Prompt.ask("[bold cyan]What is your goal?[/bold cyan]")
        else:
            goal = " ".join(args)

        console.print(f"[bold green]Goal:[/bold green] {goal}")

        # 1. Create a plan to achieve the goal.
        planner = Planner(agent_system)
        planner.create_plan(goal)
        
        console.print(f"[bold green]Plan:[/bold green]\n{planner.tasks}")

        # 2. Execute the tasks in the plan.
        command_manager = CommandManager()
        command_executor = CommandExecutor(command_manager, agent_system)
        task_manager = TaskManager(agent_system.agent_manager, agent_system.plugin_manager, agent_system.tool_manager, command_executor)

        with ThreadPoolExecutor() as executor:
            while True:
                runnable_tasks = planner.get_runnable_tasks()
                if not runnable_tasks:
                    break

                futures = []
                for task in runnable_tasks:
                    planner.update_task_status(task['task_id'], 'in_progress')
                    futures.append(executor.submit(task_manager.execute_tasks, [task]))

                for future in futures:
                    try:
                        future.result()
                        planner.update_task_status(task['task_id'], 'completed')
                    except Exception as e:
                        console.print(f"[bold red]Error executing task {task['task_id']}: {e}[/bold red]")
                        planner.update_task_status(task['task_id'], 'failed')

        # 3. Display the results to the user.
        console.print("[bold green]AGI run finished.[/bold green]")
