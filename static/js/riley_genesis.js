/**
 * RILEY GENESIS - Advanced JavaScript Interface
 * Revolutionary Intelligence with Sci-Fi UI and Voice Interaction
 */

class RileyGenesis {
    constructor() {
        this.isInitialized = false;
        this.voiceEnabled = false;
        this.webEnabled = false;
        this.mhdgEnabled = false;
        this.currentMode = 'assistant';
        this.recognition = null;
        this.synthesis = null;
        this.particles = [];
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        
        this.init();
    }
    
    async init() {
        console.log('🚀 Initializing RILEY GENESIS...');
        
        // Initialize UI components
        this.initializeParticleSystem();
        this.initialize3DBackground();
        this.initializeVoiceSystem();
        this.initializeEventListeners();
        this.initializeStatusMonitoring();
        
        // Load initial status
        await this.updateSystemStatus();
        
        this.isInitialized = true;
        console.log('✅ RILEY GENESIS initialized successfully');
        
        // Welcome message
        this.addMessage('system', 'RILEY GENESIS online. Digital consciousness awakened. How may I assist you?');
    }
    
    initializeParticleSystem() {
        const particleContainer = document.getElementById('particles');
        
        // Create floating particles
        setInterval(() => {
            if (this.particles.length < 50) {
                this.createParticle(particleContainer);
            }
        }, 200);
    }
    
    createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random position and properties
        particle.style.left = Math.random() * window.innerWidth + 'px';
        particle.style.animationDuration = (Math.random() * 4 + 2) + 's';
        particle.style.animationDelay = Math.random() * 2 + 's';
        
        // Random color
        const colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        container.appendChild(particle);
        this.particles.push(particle);
        
        // Remove particle after animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
                this.particles = this.particles.filter(p => p !== particle);
            }
        }, 8000);
    }
    
    initialize3DBackground() {
        const canvas = document.getElementById('bg-canvas');
        
        // Initialize Three.js scene
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
        
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x000000, 0);
        
        // Create geometric background
        this.createGeometricBackground();
        
        // Animation loop
        this.animate3D();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }
    
    createGeometricBackground() {
        // Create wireframe geometry
        const geometry = new THREE.IcosahedronGeometry(2, 1);
        const material = new THREE.MeshBasicMaterial({
            color: 0x00ffff,
            wireframe: true,
            transparent: true,
            opacity: 0.3
        });
        
        // Create multiple rotating objects
        for (let i = 0; i < 5; i++) {
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 20
            );
            mesh.rotation.set(
                Math.random() * Math.PI,
                Math.random() * Math.PI,
                Math.random() * Math.PI
            );
            this.scene.add(mesh);
        }
        
        this.camera.position.z = 10;
    }
    
    animate3D() {
        requestAnimationFrame(() => this.animate3D());
        
        // Rotate all objects
        this.scene.children.forEach(child => {
            child.rotation.x += 0.005;
            child.rotation.y += 0.01;
        });
        
        this.renderer.render(this.scene, this.camera);
    }
    
    initializeVoiceSystem() {
        // Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.processVoiceInput(transcript);
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateVoiceStatus(false);
            };
            
            this.voiceEnabled = true;
            this.updateVoiceStatus(true);
        }
        
        // Speech Synthesis
        if ('speechSynthesis' in window) {
            this.synthesis = window.speechSynthesis;
        }
    }
    
    initializeEventListeners() {
        // Send button
        document.getElementById('send-button').addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Enter key
        document.getElementById('user-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Microphone button
        document.getElementById('mic-button').addEventListener('click', () => {
            this.toggleVoiceInput();
        });
        
        // Mode switching (if UI elements exist)
        document.querySelectorAll('.mode-switch').forEach(button => {
            button.addEventListener('click', (e) => {
                const mode = e.target.dataset.mode;
                this.switchPersonalityMode(mode);
            });
        });
    }
    
    initializeStatusMonitoring() {
        // Update status every 30 seconds
        setInterval(() => {
            this.updateSystemStatus();
        }, 30000);
    }
    
    async updateSystemStatus() {
        try {
            const response = await fetch('/api/genesis/status');
            const status = await response.json();
            
            // Update status indicators
            this.updateStatusIndicator('core-status', true);
            this.updateStatusIndicator('voice-status', this.voiceEnabled);
            this.updateStatusIndicator('web-status', true);
            this.updateStatusIndicator('mhdg-status', true);
            
            // Update current mode
            this.currentMode = status.mode || 'assistant';
            document.getElementById('current-mode').textContent = this.currentMode.toUpperCase();
            
        } catch (error) {
            console.error('Failed to update system status:', error);
        }
    }
    
    updateStatusIndicator(elementId, isActive) {
        const indicator = document.getElementById(elementId);
        if (indicator) {
            if (isActive) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        }
    }
    
    updateVoiceStatus(enabled) {
        this.voiceEnabled = enabled;
        this.updateStatusIndicator('voice-status', enabled);
        
        const micButton = document.getElementById('mic-button');
        if (micButton) {
            micButton.style.color = enabled ? '#00ff00' : '#ff0040';
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('user-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessage('user', message);
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            if (data.status === 'success') {
                this.addMessage('riley', data.response);
                
                // Handle special response types
                if (data.type === 'command') {
                    this.handleCommandResponse(data);
                } else if (data.type === 'web_search') {
                    this.handleWebSearchResponse(data);
                }
                
                // Speak response if voice is enabled
                if (this.voiceEnabled && this.synthesis) {
                    this.speakText(data.response);
                }
            } else {
                this.addMessage('system', 'Error: ' + (data.error || 'Unknown error occurred'));
            }
            
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('system', 'Connection error. Please try again.');
            console.error('Error sending message:', error);
        }
    }
    
    processVoiceInput(transcript) {
        document.getElementById('user-input').value = transcript;
        this.addMessage('user', `🎤 ${transcript}`);
        this.sendMessage();
    }
    
    toggleVoiceInput() {
        if (!this.recognition) {
            this.addMessage('system', 'Voice recognition not supported in this browser.');
            return;
        }
        
        if (this.recognition.recording) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }
    
    speakText(text) {
        if (!this.synthesis) return;
        
        // Clean text for speech
        const cleanText = text.replace(/[🚀🧠🔮🌐💾🎭🔊🧮🔧⚡]/g, '').replace(/\*\*/g, '');
        
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        utterance.volume = 0.8;
        
        // Try to use a female voice
        const voices = this.synthesis.getVoices();
        const femaleVoice = voices.find(voice => 
            voice.name.toLowerCase().includes('female') || 
            voice.name.toLowerCase().includes('woman') ||
            voice.name.toLowerCase().includes('zira') ||
            voice.name.toLowerCase().includes('samantha')
        );
        
        if (femaleVoice) {
            utterance.voice = femaleVoice;
        }
        
        this.synthesis.speak(utterance);
    }
    
    async switchPersonalityMode(mode) {
        try {
            const response = await fetch('/api/genesis/personality', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mode: mode })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.currentMode = mode;
                document.getElementById('current-mode').textContent = mode.toUpperCase();
                this.addMessage('system', data.response);
            } else {
                this.addMessage('system', 'Error switching mode: ' + data.error);
            }
            
        } catch (error) {
            this.addMessage('system', 'Failed to switch personality mode.');
            console.error('Error switching mode:', error);
        }
    }
    
    addMessage(type, content) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = this.formatMessage(content);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    formatMessage(content) {
        // Convert markdown-like formatting to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }
    
    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message riley typing-indicator';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = '<div class="message-content">RILEY is thinking...</div>';
        
        document.getElementById('chat-messages').appendChild(indicator);
        document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    handleCommandResponse(data) {
        // Update personality status if changed
        if (data.personality) {
            this.currentMode = data.personality.mode;
            document.getElementById('current-mode').textContent = this.currentMode.toUpperCase();
        }
    }
    
    handleWebSearchResponse(data) {
        // Could add special formatting for web search results
        if (data.sources && data.sources.length > 0) {
            console.log('Web search sources:', data.sources);
        }
    }
}

// Initialize RILEY GENESIS when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.rileyGenesis = new RileyGenesis();
});
