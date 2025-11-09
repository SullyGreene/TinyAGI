// TinyAGI/static/js/features/music-studio.js

import { toggleModal } from '../ui/modal.js';

const musicStudioButton = document.getElementById('music-studio-button');
const startMusicButton = document.getElementById('start-music-button');
const steerMusicButton = document.getElementById('steer-music-button');
const stopMusicButton = document.getElementById('stop-music-button');
const musicPromptInput = document.getElementById('music-prompt');
const musicSteerPromptInput = document.getElementById('music-steer-prompt');
const statusEl = document.getElementById('music-status');

let musicSocket = null;
let audioContext = null;
let audioQueue = [];
let isPlayingMusic = false;

function updateMusicStatus(text, isError = false) {
    if (statusEl) {
        statusEl.textContent = text;
        statusEl.style.color = isError ? 'var(--accent-danger)' : 'var(--text-secondary)';
    }
}

function setupMusicSocket() {
    if (musicSocket) return;

    musicSocket = io('/music');

    musicSocket.on('connect', () => console.log('Connected to music server.'));

    musicSocket.on('stream_started', () => {
        updateMusicStatus('Streaming...');
        startMusicButton.disabled = true;
        steerMusicButton.disabled = false;
        stopMusicButton.disabled = false;
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 48000 });
        }
        if (audioContext.state === 'suspended') audioContext.resume();
        isPlayingMusic = true;
        playAudioQueue();
    });

    musicSocket.on('audio_chunk', (chunk) => {
        const int16Array = new Int16Array(chunk);
        const float32Array = new Float32Array(int16Array.length);
        for (let i = 0; i < int16Array.length; i++) {
            float32Array[i] = int16Array[i] / 32768.0;
        }
        audioQueue.push(float32Array);
    });

    musicSocket.on('stream_error', (data) => {
        updateMusicStatus(`Error: ${data.error}`, true);
        stopMusicStream();
    });
}

function playAudioQueue() {
    if (!isPlayingMusic || audioQueue.length === 0) return;

    const audioData = audioQueue.shift();
    const audioBuffer = audioContext.createBuffer(2, audioData.length / 2, audioContext.sampleRate);
    audioBuffer.copyToChannel(audioData.filter((_, i) => i % 2 === 0), 0); // Left
    audioBuffer.copyToChannel(audioData.filter((_, i) => i % 2 !== 0), 1); // Right

    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
    source.onended = playAudioQueue;
}

function stopMusicStream() {
    if (musicSocket) musicSocket.disconnect();
    musicSocket = null;
    isPlayingMusic = false;
    audioQueue = [];
    updateMusicStatus('Ready to generate music.');
    startMusicButton.disabled = false;
    steerMusicButton.disabled = true;
    stopMusicButton.disabled = true;
}

export function initializeMusicStudio() {
    musicStudioButton.addEventListener('click', () => toggleModal('music-studio-modal', true));
    startMusicButton.addEventListener('click', () => {
        setupMusicSocket();
        musicSocket.emit('start_music_stream', { prompt: musicPromptInput.value });
    });
    steerMusicButton.addEventListener('click', () => musicSocket.emit('steer_music', { prompt: musicSteerPromptInput.value }));
    stopMusicButton.addEventListener('click', stopMusicStream);
    document.querySelector('#music-studio-modal .close-button').addEventListener('click', stopMusicStream);
}