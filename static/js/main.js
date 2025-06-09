// J.A.R.V.I.S. AI Assistant - Main JavaScript
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');
    const feedbackModal = document.getElementById('feedback-modal');
    const closeModal = document.querySelector('.close-modal');
    const positiveFeedback = document.getElementById('positive-feedback');
    const negativeFeedback = document.getElementById('negative-feedback');
    const submitFeedback = document.getElementById('submit-feedback');
    const feedbackText = document.getElementById('feedback-text');
    const feedbackModalTitle = document.getElementById('feedback-modal-title');
    const savePreferences = document.getElementById('save-preferences');
    
    // Stats elements
    const commandsCount = document.getElementById('commands-count');
    const patternsCount = document.getElementById('patterns-count');
    const satisfactionRate = document.getElementById('satisfaction-rate');
    const suggestionsList = document.getElementById('suggestions-list');
    
    // Preference elements
    const voiceType = document.getElementById('voice-type');
    const interfaceTheme = document.getElementById('interface-theme');
    const responseDetail = document.getElementById('response-detail');
    
    // State
    let isPositiveFeedback = true;
    let recognitionActive = false;
    let speechRecognition = null;
    
    // Initialize speech recognition if available
    if ('webkitSpeechRecognition' in window) {
        speechRecognition = new webkitSpeechRecognition();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = false;
        speechRecognition.lang = 'en-US';
        
        speechRecognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };
        
        speechRecognition.onend = () => {
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            micButton.classList.remove('active');
            recognitionActive = false;
        };
        
        speechRecognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            micButton.classList.remove('active');
            recognitionActive = false;
            addSystemMessage('I couldn\'t hear you clearly. Please try again or type your message.');
        };
    } else {
        micButton.style.display = 'none';
    }
    
    // Load learning stats and suggestions
    loadLearningStats();
    loadSuggestions();
    loadPreferences();
    
    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    micButton.addEventListener('click', toggleSpeechRecognition);
    
    positiveFeedback.addEventListener('click', () => {
        isPositiveFeedback = true;
        feedbackModalTitle.textContent = 'Positive Feedback';
        feedbackText.placeholder = 'What did you find helpful about J.A.R.V.I.S.?';
        feedbackModal.style.display = 'block';
    });
    
    negativeFeedback.addEventListener('click', () => {
        isPositiveFeedback = false;
        feedbackModalTitle.textContent = 'Improvement Suggestions';
        feedbackText.placeholder = 'How can J.A.R.V.I.S. be improved?';
        feedbackModal.style.display = 'block';
    });
    
    closeModal.addEventListener('click', () => {
        feedbackModal.style.display = 'none';
        feedbackText.value = '';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === feedbackModal) {
            feedbackModal.style.display = 'none';
            feedbackText.value = '';
        }
    });
    
    submitFeedback.addEventListener('click', submitUserFeedback);
    
    savePreferences.addEventListener('click', saveUserPreferences);
    
    // Initialize with sample messages if the chat is empty
    if (chatMessages.children.length <= 1) {
        // Welcome message is already added in the HTML
        
        // Add a suggestion
        setTimeout(() => {
            addSystemMessage('Try asking me questions like "What time is it?" or "Tell me about Iron Man"');
        }, 1000);
    }
    
    // Functions
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (message === '') return;
        
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input
        userInput.value = '';
        
        // Send to backend API
        fetchJarvisResponse(message);
    }
    
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user';
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    function addSystemMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message system';
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        // Convert URLs to clickable links
        message = linkify(message);
        
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${message}</p>
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
        
        // Speech synthesis
        if ('speechSynthesis' in window) {
            const speech = new SpeechSynthesisUtterance(message.replace(/<[^>]*>?/gm, ''));
            speech.lang = 'en-US';
            window.speechSynthesis.speak(speech);
        }
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function fetchJarvisResponse(message) {
        // Add thinking indicator
        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'message system';
        loadingMessage.innerHTML = `
            <div class="message-content">
                <p><i class="fas fa-circle-notch fa-spin"></i> Processing...</p>
            </div>
        `;
        chatMessages.appendChild(loadingMessage);
        scrollToBottom();
        
        // Call the API
        fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            chatMessages.removeChild(loadingMessage);
            
            // Add response
            addSystemMessage(data.response);
            
            // Update stats
            loadLearningStats();
            loadSuggestions();
        })
        .catch(error => {
            // Remove loading indicator
            chatMessages.removeChild(loadingMessage);
            
            console.error('Error:', error);
            addSystemMessage('I encountered an error processing your request. Please try again.');
        });
    }
    
    function toggleSpeechRecognition() {
        if (!speechRecognition) return;
        
        if (recognitionActive) {
            speechRecognition.stop();
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            micButton.classList.remove('active');
            recognitionActive = false;
        } else {
            speechRecognition.start();
            micButton.innerHTML = '<i class="fas fa-microphone-alt"></i>';
            micButton.classList.add('active');
            recognitionActive = true;
            addSystemMessage('Listening...');
        }
    }
    
    function loadLearningStats() {
        fetch('/api/learning-stats')
            .then(response => response.json())
            .then(data => {
                commandsCount.textContent = data.total_commands || 0;
                
                // Calculate patterns count (this is just an estimate since we don't have direct access)
                const patternEstimate = Math.floor(data.total_commands * 0.8);
                patternsCount.textContent = patternEstimate;
                
                // Check if we have feedback data to calculate satisfaction
                if (data.user_satisfaction !== undefined) {
                    satisfactionRate.textContent = `${Math.round(data.user_satisfaction * 100)}%`;
                } else {
                    satisfactionRate.textContent = 'N/A';
                }
            })
            .catch(error => {
                console.error('Error loading learning stats:', error);
            });
    }
    
    function loadSuggestions() {
        fetch('/api/suggestions')
            .then(response => response.json())
            .then(data => {
                // Clear current suggestions
                suggestionsList.innerHTML = '';
                
                if (data && data.length > 0) {
                    data.forEach(suggestion => {
                        const li = document.createElement('li');
                        li.textContent = suggestion.message;
                        suggestionsList.appendChild(li);
                    });
                } else {
                    // No suggestions yet
                    const li = document.createElement('li');
                    li.textContent = 'No suggestions yet. Keep interacting with J.A.R.V.I.S.';
                    suggestionsList.appendChild(li);
                }
            })
            .catch(error => {
                console.error('Error loading suggestions:', error);
                suggestionsList.innerHTML = '<li>Unable to load suggestions at this time.</li>';
            });
    }
    
    function loadPreferences() {
        fetch('/api/preferences')
            .then(response => response.json())
            .then(data => {
                // Set UI preferences if available
                if (data.ui) {
                    if (data.ui.voice_type) {
                        voiceType.value = data.ui.voice_type.value;
                    }
                    
                    if (data.ui.theme) {
                        interfaceTheme.value = data.ui.theme.value;
                        applyTheme(data.ui.theme.value);
                    }
                    
                    if (data.ui.detail_level) {
                        responseDetail.value = data.ui.detail_level.value;
                    }
                }
            })
            .catch(error => {
                console.error('Error loading preferences:', error);
            });
    }
    
    function saveUserPreferences() {
        const preferences = {
            voice_type: voiceType.value,
            theme: interfaceTheme.value,
            detail_level: responseDetail.value
        };
        
        // Save each preference
        Object.entries(preferences).forEach(([name, value]) => {
            fetch('/api/preferences', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    category: 'ui',
                    name: name,
                    value: value
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(`Saved preference: ${name}`);
                    
                    // Apply theme if it was changed
                    if (name === 'theme') {
                        applyTheme(value);
                    }
                }
            })
            .catch(error => {
                console.error('Error saving preference:', error);
            });
        });
        
        // Notify user
        addSystemMessage('Your preferences have been saved.');
    }
    
    function submitUserFeedback() {
        const feedback = feedbackText.value.trim();
        
        if (feedback === '') {
            alert('Please enter some feedback.');
            return;
        }
        
        fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                feedback: feedback,
                is_positive: isPositiveFeedback
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addSystemMessage(`Thank you for your ${isPositiveFeedback ? 'positive feedback' : 'suggestions'}. I'll use this to improve.`);
                feedbackModal.style.display = 'none';
                feedbackText.value = '';
                
                // Refresh stats
                loadLearningStats();
            }
        })
        .catch(error => {
            console.error('Error submitting feedback:', error);
            alert('There was an error submitting your feedback. Please try again.');
        });
    }
    
    function applyTheme(theme) {
        const root = document.documentElement;
        
        switch (theme) {
            case 'light':
                root.style.setProperty('--bg-color', '#f5f5f5');
                root.style.setProperty('--panel-bg', '#ffffff');
                root.style.setProperty('--text-color', '#333333');
                root.style.setProperty('--text-secondary', '#666666');
                break;
                
            case 'blue':
                root.style.setProperty('--primary-color', '#1976d2');
                root.style.setProperty('--secondary-color', '#2196f3');
                root.style.setProperty('--bg-color', '#0a1929');
                root.style.setProperty('--panel-bg', '#10243e');
                root.style.setProperty('--accent-color', '#29b6f6');
                root.style.setProperty('--arc-reactor', '#40c4ff');
                break;
                
            default: // dark
                root.style.setProperty('--bg-color', '#1a1a1a');
                root.style.setProperty('--panel-bg', '#272727');
                root.style.setProperty('--text-color', '#f0f0f0');
                root.style.setProperty('--text-secondary', '#a0a0a0');
                break;
        }
    }
    
    // Helper functions
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function linkify(text) {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, url => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);
    }
});
