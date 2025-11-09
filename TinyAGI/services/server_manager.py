# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/services/server_manager.py
import time
import uuid

from flask import Flask, request, jsonify, Response, render_template
from flask_socketio import SocketIO, emit
import asyncio
from ..agent import AgentSystem
import os
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.panel import Panel
import json

logger = logging.getLogger(__name__)
console = Console()

# Dictionary to hold background tasks for music generation
music_sessions = {}


def setup_rich_logging():
    """Sets up logging to use RichHandler for beautiful output."""
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=True)]
    )


def create_app():
    """
    Create and configure the Flask application.

    :return: Configured Flask app
    """
    # Define paths relative to the project root to find templates and static files
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_folder = os.path.join(project_root, 'templates')
    static_folder = os.path.join(project_root, 'static') # This should point to TinyAGI/static

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    socketio = SocketIO(app, async_mode='threading')

    setup_rich_logging()

    def initialize_agent_system(config_files='config/agent_config.json'):
        """Initializes the AgentSystem and attaches it to the app context."""
        try:
            agent_system = AgentSystem(config_files=config_files)
            app.agent_system = agent_system
            app.config['AGENT_CONFIG_PATH'] = agent_system.config_files[0] if agent_system.config_files else None
        except Exception as e:
            logger.error(f"Failed to initialize AgentSystem: {e}")
            # We can let the app start and fail on requests, or exit here.
            # For a web UI, it's better to let it start and show an error.
            app.agent_system = None
        app.config['AGENT_CONFIG'] = agent_system.config if app.agent_system else {}
        app.plugin_manager = agent_system.plugin_manager if app.agent_system else None
        app.task_manager = agent_system.task_manager if app.agent_system else None
        app.tool_manager = agent_system.tool_manager if app.agent_system else None
        logger.info("AgentSystem initialized and attached to Flask app.")

    # Initial setup
    with app.app_context():
        initialize_agent_system()

    @app.route('/')
    def index():
        """Serve the main web UI."""
        return render_template('index.html')

    @app.route('/api/agents', methods=['GET'])
    def get_agents():
        """Endpoint to get the list of available agents."""
        if not app.agent_system:
            return jsonify({'error': 'AgentSystem not initialized'}), 500
        agents = list(app.agent_system.agent_manager.loaded_agents.keys())
        return jsonify(agents)

    @app.route('/api/agents', methods=['POST'])
    def create_agent():
        """Endpoint to create a new agent."""
        config_path = app.config.get('AGENT_CONFIG_PATH')
        if not config_path or not os.path.exists(config_path):
            return jsonify({'error': 'Agent configuration file not found or accessible.'}), 500

        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            return jsonify({'error': f'Failed to read or parse agent config: {str(e)}'}), 500

        new_agent_data = request.get_json()
        agent_name = new_agent_data.get('name')

        if not agent_name:
            return jsonify({'error': 'Agent name is required.'}), 400

        # Check for uniqueness
        if any(agent.get('name') == agent_name for agent in config_data.get('agents', [])):
            return jsonify({'error': f"An agent with the name '{agent_name}' already exists."}), 409

        # Create a new agent config based on a simple template (e.g., Gemini)
        new_agent_config = {
            "name": agent_name,
            "module": "gemini_agent",
            "class": "GeminiAgent",
            "source": "local",
            "description": new_agent_data.get('description', ''),
            "system_prompt": new_agent_data.get('system_prompt', ''),
            "config": {
                "generation_model": new_agent_data.get('model', 'gemini-1.5-flash'),
                "embedding_model": "models/embedding-001"
            }
        }

        config_data['agents'].append(new_agent_config)

        try:
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            # Reload the agent system to apply changes
            initialize_agent_system(config_files=config_path)
            return jsonify({'message': f"Agent '{agent_name}' created successfully.", 'agent': new_agent_config}), 201
        except Exception as e:
            logger.error(f"Error creating agent '{agent_name}': {e}")
            return jsonify({'error': f'Failed to create agent: {str(e)}'}), 500

    @app.route('/api/agents/<string:agent_name>', methods=['GET', 'PUT', 'DELETE'])
    def manage_agent(agent_name):
        """Endpoint to get, update, or delete a specific agent's config."""
        config_path = app.config.get('AGENT_CONFIG_PATH')
        if not config_path or not os.path.exists(config_path):
            return jsonify({'error': 'Agent configuration file not found or accessible.'}), 500

        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            return jsonify({'error': f'Failed to read or parse agent config: {str(e)}'}), 500

        # Find the agent's configuration
        agent_config = None
        agent_index = -1
        for i, agent in enumerate(config_data.get('agents', [])):
            if agent.get('name') == agent_name:
                agent_config = agent
                agent_index = i
                break

        # Add modes to the response if they exist
        if agent_config and 'modes' in agent_config:
            agent_config['modes'] = agent_config.get('modes', {})

        if agent_index == -1:
            return jsonify({'error': f"Agent '{agent_name}' not found in configuration."}), 404

        if request.method == 'GET':
            return jsonify(agent_config)

        if request.method == 'DELETE':
            try:
                # Remove the agent from the list
                config_data['agents'].pop(agent_index)
                with open(config_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                # Reload the agent system to apply changes
                initialize_agent_system(config_files=config_path)
                return jsonify({'message': f"Agent '{agent_name}' deleted successfully."}), 200
            except Exception as e:
                logger.error(f"Error deleting agent '{agent_name}': {e}")
                return jsonify({'error': f'Failed to delete agent: {str(e)}'}), 500

        if request.method == 'PUT':
            try:
                update_data = request.get_json()
                
                # Update the agent's configuration
                # We only update specific, editable fields to avoid breaking the config
                editable_fields = ['description', 'model', 'system_prompt']
                for field in editable_fields:
                    if field in update_data:
                        config_data['agents'][agent_index][field] = update_data[field]
                
                # Handle nested config for provider-specific settings like 'temperature'
                if 'config' in update_data and 'config' in config_data['agents'][agent_index]:
                    nested_editable_fields = ['temperature', 'max_tokens']
                    for field in nested_editable_fields:
                         if field in update_data['config']:
                            config_data['agents'][agent_index]['config'][field] = update_data['config'][field]

                with open(config_path, 'w') as f:
                    json.dump(config_data, f, indent=2)

                # Reload the agent system to apply changes
                initialize_agent_system(config_files=config_path)
                return jsonify({'message': f"Agent '{agent_name}' updated successfully.", 'agent': config_data['agents'][agent_index]}), 200

            except Exception as e:
                logger.error(f"Error updating agent '{agent_name}': {e}")
                return jsonify({'error': f'Failed to update agent: {str(e)}'}), 500
        
        return jsonify({'error': 'Method not allowed'}), 405

    @app.route('/chat', methods=['POST'])
    def chat():
        """
        Handle chat requests.
        """
        data = request.get_json()
        messages = data.get('messages')
        agent_name = data.get('agent')
        stream = data.get('stream', False)
        settings = data.get('settings', {})  # Get settings, default to empty dict
        mode = data.get('mode')

        if not messages:
            return jsonify({'error': 'Messages are required'}), 400
        if not agent_name:
            return jsonify({'error': 'Agent name is required'}), 400
        if not app.agent_system:
            return jsonify({'error': 'AgentSystem not initialized'}), 500

        agent = app.agent_system.agent_manager.get_agent(agent_name)
        if not agent:
            return jsonify({'error': f"Agent '{agent_name}' not found"}), 404

        try:
            # Pass the entire conversation history to the agent's chat method.
            # Also, unpack the settings dictionary as keyword arguments.
            if stream:
                def generate():
                    for chunk in agent.chat(messages, stream=True, mode=mode, **settings):
                        yield chunk
                return Response(generate(), mimetype='text/plain')
            else:
                generated_text = agent.chat(messages, mode=mode, **settings)
                return jsonify({'response': generated_text})
        except Exception as e:
            logger.error(f"Error during chat: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/generate', methods=['POST'])
    def generate():
        """
        Handle text generation requests.
        """
        data = request.get_json()
        prompt = data.get('prompt')
        agent_name = data.get('agent')
        stream = data.get('stream', False)

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        if not agent_name:
            return jsonify({'error': 'Agent name is required'}), 400
        if not app.agent_system:
            return jsonify({'error': 'AgentSystem not initialized'}), 500

        agent = app.agent_system.agent_manager.get_agent(agent_name)
        if not agent:
            return jsonify({'error': f"Agent '{agent_name}' not found"}), 404

        try:
            if stream:
                def generate_stream():
                    for chunk in agent.generate_text(prompt, stream=True):
                        yield chunk
                return Response(generate_stream(), mimetype='text/plain')
            else:
                generated_text = agent.generate_text(prompt)
                return jsonify({'response': generated_text})
        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/generate-image', methods=['POST'])
    def generate_image():
        """
        Handle image generation requests.
        """
        data = request.get_json()
        prompt = data.get('prompt')
        agent_name = data.get('agent')
        settings = data.get('settings', {})

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        if not agent_name:
            return jsonify({'error': 'Agent name is required'}), 400
        if not app.agent_system:
            return jsonify({'error': 'AgentSystem not initialized'}), 500

        agent = app.agent_system.agent_manager.get_agent(agent_name)
        if not agent:
            return jsonify({'error': f"Agent '{agent_name}' not found"}), 404
        
        if not hasattr(agent, 'generate_images'):
            return jsonify({'error': f"Agent '{agent_name}' does not support image generation."}), 400

        try:
            images_base64 = agent.generate_images(prompt, **settings)
            return jsonify({'images': images_base64})
        except Exception as e:
            logger.error(f"Error during image generation: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/robotics/process', methods=['POST'])
    def robotics_process():
        """
        Handle robotics-related image and prompt processing.
        """
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        prompt = request.form.get('prompt')
        agent_name = request.form.get('agent', 'robotics_agent')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        agent = app.agent_system.agent_manager.get_agent(agent_name)
        if not agent or not hasattr(agent, 'process_image_with_prompt'):
            return jsonify({'error': f"Robotics agent '{agent_name}' not found or is invalid."}), 404

        try:
            image_bytes = file.read()
            image_part = {
                "mime_type": file.mimetype,
                "data": image_bytes,
            }

            # The agent expects a Part object from the SDK
            from google.generativeai import types
            sdk_image_part = types.Part.from_dict(image_part)

            result_text = agent.process_image_with_prompt(sdk_image_part, prompt)
            return jsonify({'result': result_text})
        except Exception as e:
            logger.error(f"Error during robotics processing: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/generate-video', methods=['POST'])
    def start_video_generation():
        """
        Starts an asynchronous video generation job.
        """
        data = request.get_json()
        prompt = data.get('prompt')
        agent_name = data.get('agent', 'veo_agent')
        settings = data.get('settings', {})

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        agent = app.agent_system.agent_manager.get_agent(agent_name)
        if not agent or not hasattr(agent, 'generate_video'):
            return jsonify({'error': f"Video generation agent '{agent_name}' not found or is invalid."}), 404

        try:
            operation = agent.generate_video(prompt, **settings)
            return jsonify({'operation_name': operation.name}), 202  # 202 Accepted
        except Exception as e:
            logger.error(f"Error starting video generation: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/video-operations/<string:operation_name>', methods=['GET'])
    def get_video_operation_status(operation_name):
        """
        Polls the status of a video generation operation.
        """
        try:
            # The genai library needs to be configured in this context if it's not already
            if not genai.operations:
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not set for polling.")
                genai.configure(api_key=api_key)

            operation = genai.operations.get(name=operation_name)

            if not operation.done:
                return jsonify({'status': 'processing'})

            if operation.error:
                logger.error(f"Video generation failed for operation {operation_name}: {operation.error.message}")
                return jsonify({'status': 'failed', 'error': operation.error.message}), 500

            # Video is ready, download and serve it
            generated_video = operation.response.generated_videos[0]
            
            # Ensure the directory exists
            video_dir = os.path.join(app.static_folder, 'generated_videos')
            os.makedirs(video_dir, exist_ok=True)

            # Generate a unique filename
            video_filename = f"{uuid.uuid4()}.mp4"
            video_path = os.path.join(video_dir, video_filename)
            
            # The SDK's download method saves the file
            generated_video.video.save(video_path)
            logger.info(f"Saved generated video to {video_path}")

            video_url = f"/static/generated_videos/{video_filename}"
            return jsonify({'status': 'complete', 'url': video_url})

        except Exception as e:
            logger.error(f"Error polling video operation {operation_name}: {e}", exc_info=True)
            return jsonify({'status': 'failed', 'error': str(e)}), 500

    @app.route('/embed', methods=['POST'])
    def embed():
        """
        Handle embedding requests.
        """
        data = request.get_json()
        input_data = data.get('input')
        agent_name = data.get('agent')

        if not input_data:
            return jsonify({'error': 'Input text is required'}), 400
        if not agent_name:
            return jsonify({'error': 'Agent name is required'}), 400
        if not app.agent_system:
            return jsonify({'error': 'AgentSystem not initialized'}), 500

        agent = app.agent_system.agent_manager.get_agent(agent_name)
        if not agent:
            return jsonify({'error': f"Agent '{agent_name}' not found"}), 404

        try:
            embeddings = agent.embed(input_data)
            return jsonify({'embedding': embeddings})
        except Exception as e:
            logger.error(f"Error during embedding: {e}")
            return jsonify({'error': str(e)}), 500

    # --- Music Generation Socket.IO Handlers ---

    @socketio.on('connect', namespace='/music')
    def music_connect():
        logger.info(f"Client connected to music namespace: {request.sid}")

    @socketio.on('disconnect', namespace='/music')
    def music_disconnect():
        logger.info(f"Client disconnected from music namespace: {request.sid}")
        # Clean up the associated music session if it exists
        if request.sid in music_sessions:
            task = music_sessions.pop(request.sid)
            task.cancel()
            logger.info(f"Cancelled and removed music session for {request.sid}")

    @socketio.on('start_music_stream', namespace='/music')
    def start_music_stream(data):
        """Starts a music generation stream in a background thread."""
        sid = request.sid
        prompt = data.get('prompt', 'ambient electronic')
        agent = app.agent_system.agent_manager.get_agent('lyria_agent')

        if not agent:
            emit('stream_error', {'error': 'Lyria agent not found.'})
            return

        # Define the async task to be run
        async def music_task():
            q = asyncio.Queue()
            lyria_task = asyncio.create_task(agent.connect_and_stream(q, prompt))
            
            # The first item from the queue is the session object
            session = await q.get()
            if isinstance(session, Exception):
                emit('stream_error', {'error': str(session)})
                return
            
            music_sessions[sid] = {'session': session, 'task': lyria_task}
            emit('stream_started')

            while True:
                item = await q.get()
                if isinstance(item, bytes): # It's audio data
                    emit('audio_chunk', item)
                elif isinstance(item, Exception): # An error occurred
                    emit('stream_error', {'error': str(item)})
                    break
                elif item is None: # Stream finished
                    break
        
        # Run the async task in a new thread
        socketio.start_background_task(asyncio.run, music_task())

    @socketio.on('steer_music', namespace='/music')
    def steer_music(data):
        sid = request.sid
        if sid in music_sessions:
            new_prompt = data.get('prompt')
            if new_prompt:
                async def do_steer():
                    session = music_sessions[sid]['session']
                    await session.set_weighted_prompts(
                        prompts=[types.WeightedPrompt(text=new_prompt, weight=1.0)]
                    )
                    logger.info(f"Steering music for {sid} with prompt: {new_prompt}")
                asyncio.run(do_steer())

    @app.route('/reload', methods=['POST'])
    def reload_model():
        """
        Reload the model with new configuration.
        """
        data = request.get_json()
        config_file = data.get('config_file')
        if not config_file:
            return jsonify({'error': 'Config file path is required'}), 400

        try:
            # Re-initialize the agent system with the new config
            initialize_agent_system(config_files=config_file)
            return jsonify({'message': 'Model reloaded successfully'}), 200
        except Exception as e:
            logger.error(f"Error during model reload: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/config', methods=['GET'])
    def get_config():
        """
        Retrieve the current configuration.
        """
        return jsonify(app.config.get('AGENT_CONFIG', {})), 200

    return app, socketio

def run_server():
    """
    Run the Flask server.
    """
    app, socketio = create_app()
    
    welcome_panel = Panel(
        "[bold green]TinyAGI Server is running![/bold green]\n\n"
        "Access the web UI at: [bold cyan]http://localhost:5000[/bold cyan]",
        title="[bold]🚀 Server Online[/bold]", border_style="blue"
    )
    console.print(welcome_panel)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)


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
