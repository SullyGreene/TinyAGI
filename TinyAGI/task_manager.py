# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/task_manager.py

import logging
import json
import os

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self, agent_manager, plugin_manager, tool_manager, command_executor):
        """
        Initialize the TaskManager with the provided agent manager, plugin_manager, tool manager, and command executor.

        :param agent_manager: Instance of AgentManager.
        :param plugin_manager: Instance of PluginManager.
        :param tool_manager: Instance of ToolManager.
        :param command_executor: Instance of CommandExecutor.
        """
        self.agent_manager = agent_manager
        self.plugin_manager = plugin_manager
        self.tool_manager = tool_manager
        self.command_executor = command_executor
        self.tasks = []
        self.task_results = {}

    def add_task(self, task):
        """Adds a task to the task list."""
        self.tasks.append(task)

    def _resolve_inputs(self, data):
        """
        Recursively resolve placeholders in task input data.
        Placeholders are in the format {{tasks.task_id.output}}.
        """
        if isinstance(data, dict):
            return {k: self._resolve_inputs(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._resolve_inputs(i) for i in data]
        elif isinstance(data, str) and data.startswith('{{') and data.endswith('}}'):
            ref = data.strip('{}').strip()
            parts = ref.split('.')

            # Expecting format "tasks.task_id.output"
            if len(parts) == 3 and parts[0] == 'tasks' and parts[2] == 'output':
                task_id_ref = parts[1]
                if task_id_ref in self.task_results:
                    logger.info(f"Resolving input from previous task '{task_id_ref}'.")
                    return self.task_results[task_id_ref]
                else:
                    logger.warning(f"Could not resolve reference to task '{task_id_ref}'. It may not have been executed yet.")
                    return data  # Return placeholder if not found
        return data

    def execute_tasks(self, tasks):
        """
        Iterate through all tasks defined in the configuration and execute them using the appropriate agents, plugins, and tools.
        Supports chaining tasks by referencing outputs of previous tasks.
        """
        logger.debug(f"Available plugins: {list(self.plugin_manager.loaded_plugins.keys())}")
        logger.debug(f"Available agents: {list(self.agent_manager.loaded_agents.keys())}")
        logger.debug(f"Available tools: {list(self.tool_manager.loaded_tools.keys())}")

        for task in tasks:
            task_id = task.get('task_id')
            command_name = task.get('command')
            plugin_name = task.get('plugin')
            agent_name = task.get('agent')  # Specify which agent to use
            tool_name = task.get('tool')    # Specify which tool to use (optional)
            input_data = self._resolve_inputs(task.get('input', {}))
            output_config = task.get('output', {})
            options = task.get('options', {})

            if command_name:
                logger.info(f"Executing command: {command_name} with args: {input_data}")
                response = self.command_executor.execute_command(command_name, input_data)
                print(f"\nTask: {task_id} - Response:\n{response}\n")
                self.task_results[task_id] = response
            elif plugin_name:
                logger.info(f"Executing task: {task_id} using plugin: {plugin_name}, agent: {agent_name}, tool: {tool_name}")

                # Validate plugin
                if plugin_name not in self.plugin_manager.loaded_plugins:
                    logger.error(f"Plugin '{plugin_name}' not found. Skipping task '{task_id}'.")
                    continue
                plugin = self.plugin_manager.get_plugin(plugin_name)

                # Validate agent
                agent = self.agent_manager.get_agent(agent_name)
                if not agent:
                    logger.error(f"Agent '{agent_name}' not found. Skipping task '{task_id}'.")
                    continue

                # Validate tool if specified
                tool = None
                if tool_name:
                    tool = self.tool_manager.get_tool(tool_name)
                    if not tool:
                        logger.error(f"Tool '{tool_name}' not found. Skipping task '{task_id}'.")
                        continue

                # Execute the plugin with the specified agent and tool
                try:
                    # Generic plugin execution
                    response = plugin.execute(
                        agent=agent,
                        tool=tool,
                        input_data=input_data,
                        options=options,
                        stream=options.get('stream', False)
                    )
                    print(f"\nTask: {task_id} - Response:\n{response}\n")

                    # Store the result for potential use in subsequent tasks
                    self.task_results[task_id] = response

                    # Save the output if configured
                    if output_config:
                        self.save_output(response, output_config)

                except Exception as e:
                    logger.error(f"Error during task '{task_id}' execution: {e}")

    def save_output(self, data, output_config):
        """
        Save the output data based on the output configuration.

        :param data: Data to save.
        :param output_config: Dictionary containing output configuration.
        """
        if output_config.get('save_to_file', False):
            try:
                file_path = output_config.get('file_path', 'output.json')
                # Ensure the output directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Check if data is already a JSON string, otherwise dump it
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Output saved to '{file_path}'.")
            except Exception as e:
                logger.error(f"Error saving output to file: {e}")


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
