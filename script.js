// Session state management
let isLoggedIn = false;
let username = '';

// Toggle Profile Modal
function toggleProfile() {
    const modal = document.getElementById('profileModal');
    modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
    
    // Toggle main content visibility
    const mainContent = document.getElementById('mainContentArea');
    mainContent.style.display = modal.style.display === 'block' ? 'none' : 'block';
}

// Toggle between Login and Signup forms
function toggleForms() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    loginForm.style.display = loginForm.style.display === 'none' ? 'block' : 'none';
    signupForm.style.display = signupForm.style.display === 'none' ? 'block' : 'none';
}

// Handle Login
function handleLogin() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    // Add your login logic here
    console.log('Login:', username, password);
    
    // Simulate successful login
    isLoggedIn = true;
    toggleProfile();
}

// Handle Signup
function handleSignup() {
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        alert("Passwords don't match!");
        return;
    }
    
    // Add your signup logic here
    console.log('Signup:', username, password);
    toggleForms();
}

// Handle Search
function handleSearch() {
    const searchInput = document.getElementById('searchInput').value;
    if (searchInput.trim()) {
        const resultsDiv = document.getElementById('searchResults');
        resultsDiv.innerHTML = `<p>Searching for: ${searchInput}</p>`;
        // Add your search logic here
    }
}

// Voice Search Functions
let recognition;

function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';

        recognition.onresult = function(event) {
            const result = event.results[0][0].transcript;
            document.getElementById('recognizedText').innerHTML = `
                <p>Recognized Text:</p>
                <p>${result}</p>
                <button onclick="useRecognizedText('${result}')">Use this text</button>
            `;
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            document.getElementById('voiceStatus').textContent = 'Error: ' + event.error;
        };
    } else {
        alert('Speech recognition is not supported in this browser.');
    }
}

function startVoiceSearch() {
    const modal = document.getElementById('voiceModal');
    modal.style.display = 'block';
    document.getElementById('recognizedText').innerHTML = '';
    initializeSpeechRecognition();
}

function startRecording() {
    if (recognition) {
        recognition.start();
        document.getElementById('startVoiceBtn').style.display = 'none';
        document.getElementById('stopVoiceBtn').style.display = 'inline-block';
        document.getElementById('voiceStatus').textContent = '🎙️ Listening...';
    }
}

function stopRecording() {
    if (recognition) {
        recognition.stop();
        document.getElementById('startVoiceBtn').style.display = 'inline-block';
        document.getElementById('stopVoiceBtn').style.display = 'none';
        document.getElementById('voiceStatus').textContent = '🎙️ Click Start to speak your query...';
    }
}

function closeVoiceModal() {
    const modal = document.getElementById('voiceModal');
    modal.style.display = 'none';
    if (recognition) {
        recognition.stop();
    }
}

function useRecognizedText(text) {
    document.getElementById('searchInput').value = text;
    closeVoiceModal();
}

// Handle sidebar clicks
function handleSidebarClick(section) {
    console.log('Navigating to:', section);
    // Add your navigation logic here
}

// Close modals when clicking outside
window.onclick = function(event) {
    const profileModal = document.getElementById('profileModal');
    const voiceModal = document.getElementById('voiceModal');
    if (event.target === profileModal || event.target === voiceModal) {
        profileModal.style.display = 'none';
        voiceModal.style.display = 'none';
        document.getElementById('mainContentArea').style.display = 'block';
    }
}