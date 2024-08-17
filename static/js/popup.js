// Function to handle all modals
function handleModals() {
    // Handle close buttons
    var closeButtons = document.getElementsByClassName('close');
    for (var i = 0; i < closeButtons.length; i++) {
        closeButtons[i].onclick = function() {
            this.parentElement.parentElement.style.display = "none";
        }
    }

    // Handle clicks outside the modal to close it
    window.onclick = function(event) {
        var modals = document.getElementsByClassName('modal');
        for (var i = 0; i < modals.length; i++) {
            if (event.target == modals[i]) {
                modals[i].style.display = "none";
            }
        }
    }
}

// Initialize modals when the page loads
document.addEventListener('DOMContentLoaded', function() {
    handleModals();
});

function addToPlaylist(songId, nextUrl) {
    var modal = document.getElementById("addToPlaylistModal-" + songId);
    var form = document.getElementById("addToPlaylistForm-" + songId);

    // Set the 'next' URL in the form
    form.querySelector('input[name="next"]').value = nextUrl;

    modal.style.display = "block";
}

function submitAddToPlaylistForm(songId, playlistId) {
    var form = document.getElementById("addToPlaylistForm-" + songId);
    var playlistInput = form.querySelector('input[name="playlist_id"]');

    // Set the playlist ID in the hidden input
    playlistInput.value = playlistId;

    // Submit the form
    form.submit();
}

function closeAddToPlaylistModal(songId) {
    var modal = document.getElementById("addToPlaylistModal-" + songId);
    modal.style.display = "none";
}


// Function to show the "Create Playlist" modal
function showCreatePlaylistModal() {
    var modal = document.getElementById("createPlaylistModal");
    modal.style.display = "block";
}

// Attach event listener to the "Create Playlist" button
var createPlaylistBtn = document.getElementById("createPlaylistBtn");
if (createPlaylistBtn) {
    createPlaylistBtn.onclick = showCreatePlaylistModal;
}