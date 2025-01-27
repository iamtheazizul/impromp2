document.addEventListener('DOMContentLoaded', function() {
    const videoId = document.getElementById('videoId').value; // Ensure this is correctly set in your HTML

    // Function to get CSRF token, useful for any POST requests you might add later
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to fetch transcription
    function fetchTranscription(videoId) {
        const transcriptSection = document.querySelector('.transcript-section');
        transcriptSection.innerHTML = `<h3>Transcription</h3><p>Fetching transcription...</p>`;

        fetch(`/video/${videoId}/`) // Ensure this URL matches your Django URL pattern for the transcription view
        .then(response => response.json())
        .then(data => {
            const transcriptionText = data.transcription;
            transcriptSection.innerHTML = `<h3>Transcription</h3><p>${transcriptionText}</p>`;
            
            // Call the function to analyze transcription after displaying it
            analyzeTranscription(videoId, transcriptionText);
        })
        .catch(error => {
            console.error('Error fetching transcription:', error);
            transcriptSection.innerHTML += `<p>Error fetching transcription.</p>`;
        });
    }

    // Function to fetch analysis
    function analyzeTranscription(videoId, transcriptionText) {
        // Assuming you have an element to display the analysis results
        const analysisSection = document.querySelector('.analysis-section');
        analysisSection.innerHTML = `<h3>Analysis</h3><p>Fetching analysis...</p>`;

        // Prepare the data for POST request
        const formData = new FormData();
        formData.append('transcription_text', transcriptionText);
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken')); // Include CSRF token

        fetch(`/analyze-transcription/${videoId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Important for Django to recognize AJAX request
                // Other headers if necessary
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            analysisSection.innerHTML = `<h3>Analysis</h3><p>${data.analysis_result}</p>`;
            renderVideo("D:\impromptle\media\videos\model.mp4"); // Use video URL here
        })
        .catch(error => {
        });
    }

    // Initiate the transcription fetch operation
    fetchTranscription(videoId);
});


function renderVideo(videoUrl) {
    const videoContainer = document.getElementById('videoContainer');
    const videoElement = document.createElement('video');
    videoElement.src = videoUrl;
    videoElement.controls = true;
    videoContainer.appendChild(videoElement);
}
