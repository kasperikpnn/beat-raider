var currentAudio = null;
const totalParts = 20; // Total parts in the seek bar
let isPlaying = false; // Track if the audio is currently playing

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`; // Format to mm:ss
}

function setDuration(audio) {
    console.log('Setting duration for:', audio.dataset.index); // Debug log
    const durationDisplay = document.getElementById('duration-display-' + audio.dataset.index);
    durationDisplay.textContent = `Duration: ${formatTime(audio.duration)}`;
}

function playMusic(index) {
    const audio = document.getElementById('audio-' + index);
    if (currentAudio && currentAudio !== audio) {
        currentAudio.pause();
        isPlaying = false; 
    }
    if (audio.paused) {
        audio.play();
        isPlaying = true;
        currentAudio = audio;
    } else {
        audio.pause();
        isPlaying = false;
        currentAudio = null;
    }

    if (isPlaying) {
        updateSeekBar(audio);
    }
}

function updateSeekBar(audio) {
    if (!audio.duration) return; // Ensure audio is loaded
    const duration = audio.duration;
    const currentTime = audio.currentTime;

    const percentage = (currentTime / duration); 
    const segments = [];

    segments.push('[');
    for (let i = 0; i < totalParts; i++) {
        if (i < Math.floor(percentage * totalParts)) {
            segments.push(`<span class="seek-segment">=</span>`);
        } else if (i === Math.floor(percentage * totalParts)) {
            segments.push(`<span class="seek-segment">></span>`);
        } else {
            segments.push(`<span class="seek-segment">·</span>`);
        }
    }
    segments.push(']');

    document.getElementById('seek-bar-' + audio.dataset.index).innerHTML = segments.join('');

    document.getElementById('time-display-' + audio.dataset.index).textContent = `[ ${formatTime(currentTime)} - ${formatTime(duration)} ]`;
}

function handleSeekClick(event, index) {
    const audio = document.getElementById('audio-' + index);
    const seekBar = document.getElementById('seek-bar-' + index);
    const clickX = event.offsetX;
    const totalWidth = seekBar.clientWidth;
    const segmentWidth = totalWidth / totalParts;
    const segmentIndex = Math.floor(clickX / segmentWidth);
    const newTime = (segmentIndex / totalParts) * audio.duration;
    audio.currentTime = newTime;

    if (currentAudio && currentAudio !== audio) {
        currentAudio.pause();
        audio.play()
        currentAudio = audio;
        isPlaying = true;
    }

    if (audio.paused && isPlaying) {
        audio.play();
        currentAudio = audio;
        isPlaying = true;
    }

    updateSeekBar(audio);
}

window.onload = function() {
    const audioElements = document.querySelectorAll('audio');
    audioElements.forEach(audio => {
        setDuration(audio);
    });
};