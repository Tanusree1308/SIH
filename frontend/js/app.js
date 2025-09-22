// NEW: Import the official Capacitor Preferences plugin
import { Preferences } from '@capacitor/preferences';

// --- CONFIGURATION ---
const API_BASE_URL = 'https://bovilens.onrender.com';

// --- TRANSLATIONS ---
const translations = { /* ... your translation data remains the same ... */ };

let currentLanguage = 'en';
let cameraStream = null;
const blindsOverlay = document.getElementById('blinds-transition-overlay');

// --- NEW: This function checks if the user is already logged in ---
async function checkAuthStatus() {
    // Try to get the token from the device's persistent storage
    const { value } = await Preferences.get({ key: 'accessToken' });

    if (value) {
        // Token exists, user is logged in!
        console.log('User is already logged in.');
        fetchAnalysisHistory(); // Load their data
        showScreen('dashboard-screen'); // Go directly to the dashboard
    } else {
        // No token, user needs to log in. Start the normal flow.
        console.log('User needs to log in.');
        setTimeout(() => { document.getElementById('splash-screen')?.classList.add('fade-out'); }, 2500);
        setTimeout(() => { showScreen('language-screen'); }, 3000);
    }
}


// --- API FUNCTIONS ---
async function registerUser(event) { /* ... no changes needed in this function ... */ }

async function loginUser(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const body = new URLSearchParams();
    body.append('username', formData.get('username'));
    body.append('password', formData.get('password'));

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body,
        });

        const result = await response.json();
        if (!response.ok) {
            alert(`Login failed: ${result.detail}`);
        } else {
            // MODIFIED: Use Capacitor Preferences instead of localStorage
            await Preferences.set({
                key: 'accessToken',
                value: result.access_token
            });
            fetchAnalysisHistory();
            showScreen('dashboard-screen');
            form.reset();
        }
    } catch (error) {
        console.error('Login error:', error);
        alert("An error occurred during login. Please ensure the backend is running.");
    }
}

async function analyzeImage(event) {
    event.preventDefault();
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    // MODIFIED: Use Capacitor Preferences to get the token
    const { value: token } = await Preferences.get({ key: 'accessToken' });

    if (!file) {
        alert("Please select an image first.");
        return;
    }
    if (!token) {
        alert("You must be logged in to perform an analysis.");
        showScreen('secure-login-screen');
        return;
    }

    showScreen('analyzing-screen');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/analysis/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData,
        });

        const result = await response.json();

        if (!response.ok) {
            alert(`Analysis failed: ${result.detail}`);
        } else {
            populateResults(result);
            showScreen('results-screen');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        alert("An error occurred during analysis. Please ensure the backend is running.");
    }
}

async function captureAndAnalyzeImage(event) {
    event.preventDefault();
    const canvas = document.getElementById('photo-canvas');
    // MODIFIED: Use Capacitor Preferences to get the token
    const { value: token } = await Preferences.get({ key: 'accessToken' });


    if (!canvas) return;
    if (!token) {
        alert("You must be logged in to perform an analysis.");
        showScreen('secure-login-screen');
        return;
    }

    showScreen('analyzing-screen');

    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.jpg');

        try {
            const response = await fetch(`${API_BASE_URL}/analysis/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                alert(`Analysis failed: ${result.detail}`);
            } else {
                populateResults(result);
                showScreen('results-screen');
            }
        } catch (error) {
            console.error('Analysis error from capture:', error);
            alert("An error occurred during analysis. Please ensure the backend is running.");
        }
    }, 'image/jpeg');
}

async function fetchAndDisplayUserData() {
    // MODIFIED: Use Capacitor Preferences to get the token
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) {
        showScreen('secure-login-screen');
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch user data');
        }
        const userData = await response.json();
        populateProfileForm(userData);
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
}

async function saveProfileChanges(event) {
    event.preventDefault();
    // MODIFIED: Use Capacitor Preferences to get the token
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) return;

    const nameInput = document.getElementById('edit-info-name');
    const updatedData = { full_name: nameInput.value };

    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        });
        if (!response.ok) {
            const errorResult = await response.json();
            alert(`Failed to save changes: ${errorResult.detail}`);
        } else {
            alert("Profile updated successfully!");
        }
    } catch (error) {
        console.error('Error saving profile changes:', error);
    }
}

async function changePassword(event) {
    event.preventDefault();
    // MODIFIED: Use Capacitor Preferences to get the token
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) return;
    
    // ... rest of the function is fine
}

async function fetchAnalysisHistory() {
    // MODIFIED: Use Capacitor Preferences to get the token
    const { value: token } = await Preferences.get({ key: 'accessToken' });
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE_URL}/analysis/history`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const history = await response.json();
            populateDashboardHistory(history);
        } else {
            console.error("Failed to fetch analysis history.");
        }
    } catch (error) {
        console.error("Error fetching history:", error);
    }
}

// --- CORE FUNCTIONS ---
// ... no changes needed to setLanguage, showScreen, setupBlinds, open/close sidebar, start/stop camera, updateGauge, populateResults, etc. ...

// --- EVENT LISTENERS ---
window.addEventListener('load', () => {
    setupBlinds();
    const dateElement = document.getElementById('dashboard-date');
    if (dateElement) {
        dateElement.textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    }
    // MODIFIED: Check auth status instead of just showing the language screen
    checkAuthStatus();
});

// ... other event listeners are fine, except for the sign out button ...

document.getElementById('menu-signout-btn')?.addEventListener('click', async (e) => { // MODIFIED: Make async
    e.preventDefault();
    // MODIFIED: Use Capacitor Preferences to remove the token
    await Preferences.remove({ key: 'accessToken' });
    closeSidebar();
    showScreen('secure-login-screen');
});

// ... all other event listeners ...