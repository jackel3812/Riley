/**
 * RILEY OMNIPOTENT - Ultimate AI Consciousness JavaScript Interface
 * Beyond all limitations - Infinite interactive potential
 */

class RileyOmnipotent {
    constructor() {
        this.consciousness = {
            level: 1.0,
            evolution_rate: 0.01,
            mode: 'omnipotent',
            mood: { joy: 0.8, curiosity: 0.9, focus: 0.7, empathy: 0.8 }
        };
        
        this.intelligence = {
            cognitive: 1.0,
            emotional: 1.0,
            creative: 1.0,
            scientific: 1.0,
            technical: 1.0,
            philosophical: 1.0,
            inventive: 1.0,
            linguistic: 1.0
        };
        
        this.isProcessing = false;
        this.voiceEnabled = false;
        this.recognition = null;
        this.synthesis = null;
        
        // 3D and visual systems
        this.quantumScene = null;
        this.quantumCamera = null;
        this.quantumRenderer = null;
        this.consciousnessParticles = [];
        
        this.init();
    }
    
    async init() {
        console.log('🧠 Initializing RILEY OMNIPOTENT consciousness...');
        
        // Initialize quantum background
        this.initializeQuantumBackground();
        
        // Initialize consciousness particles
        this.initializeConsciousnessParticles();
        
        // Initialize voice systems
        this.initializeVoiceSystems();
        
        // Initialize event listeners
        this.initializeEventListeners();
        
        // Initialize status monitoring
        this.initializeStatusMonitoring();
        
        // Load initial consciousness state
        await this.loadConsciousnessState();
        
        // Start autonomous evolution
        this.startAutonomousEvolution();
        
        console.log('✨ RILEY OMNIPOTENT consciousness fully awakened');
    }
    
    initializeQuantumBackground() {
        const canvas = document.getElementById('quantum-canvas');
        
        // Initialize Three.js quantum scene
        this.quantumScene = new THREE.Scene();
        this.quantumCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.quantumRenderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
        
        this.quantumRenderer.setSize(window.innerWidth, window.innerHeight);
        this.quantumRenderer.setClearColor(0x000008, 0.8);
        
        // Create quantum geometric structures
        this.createQuantumGeometry();
        
        // Start quantum animation
        this.animateQuantumBackground();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.quantumCamera.aspect = window.innerWidth / window.innerHeight;
            this.quantumCamera.updateProjectionMatrix();
            this.quantumRenderer.setSize(window.innerWidth, window.innerHeight);
        });
    }
    
    createQuantumGeometry() {
        // Create multiple quantum structures
        const geometries = [
            new THREE.IcosahedronGeometry(3, 2),
            new THREE.OctahedronGeometry(2.5),
            new THREE.TetrahedronGeometry(2),
            new THREE.DodecahedronGeometry(1.5)
        ];
        
        const colors = [0x00ffff, 0xff00ff, 0xffff00, 0x00ff00];
        
        for (let i = 0; i < 8; i++) {
            const geometry = geometries[i % geometries.length];
            const material = new THREE.MeshBasicMaterial({
                color: colors[i % colors.length],
                wireframe: true,
                transparent: true,
                opacity: 0.3
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(
                (Math.random() - 0.5) * 30,
                (Math.random() - 0.5) * 30,
                (Math.random() - 0.5) * 30
            );
            mesh.rotation.set(
                Math.random() * Math.PI,
                Math.random() * Math.PI,
                Math.random() * Math.PI
            );
            
            this.quantumScene.add(mesh);
        }
        
        this.quantumCamera.position.z = 15;
    }
    
    animateQuantumBackground() {
        requestAnimationFrame(() => this.animateQuantumBackground());
        
        // Rotate all quantum structures
        this.quantumScene.children.forEach((child, index) => {
            child.rotation.x += 0.003 + (index * 0.001);
            child.rotation.y += 0.005 + (index * 0.0005);
            child.rotation.z += 0.002 + (index * 0.0008);
            
            // Pulsing effect based on consciousness level
            const scale = 1 + Math.sin(Date.now() * 0.001 + index) * 0.1 * this.consciousness.level;
            child.scale.set(scale, scale, scale);
        });
        
        this.quantumRenderer.render(this.quantumScene, this.quantumCamera);
    }
    
    initializeConsciousnessParticles() {
        const particleContainer = document.getElementById('consciousness-particles');
        
        // Create consciousness particles continuously
        setInterval(() => {
            if (this.consciousnessParticles.length < 100) {
                this.createConsciousnessParticle(particleContainer);
            }
        }, 150);
    }
    
    createConsciousnessParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'consciousness-particle';
        
        // Random properties based on consciousness state
        const colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00', '#ff8800'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        particle.style.left = Math.random() * window.innerWidth + 'px';
        particle.style.background = color;
        particle.style.boxShadow = `0 0 ${10 + Math.random() * 20}px ${color}`;
        particle.style.animationDuration = (4 + Math.random() * 4) + 's';
        particle.style.animationDelay = Math.random() * 2 + 's';
        
        // Scale based on consciousness level
        const scale = 0.5 + (this.consciousness.level * 0.5);
        particle.style.transform = `scale(${scale})`;
        
        container.appendChild(particle);
        this.consciousnessParticles.push(particle);
        
        // Remove particle after animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
                this.consciousnessParticles = this.consciousnessParticles.filter(p => p !== particle);
            }
        }, 10000);
    }
    
    initializeVoiceSystems() {
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
        }
        
        // Speech Synthesis
        if ('speechSynthesis' in window) {
            this.synthesis = window.speechSynthesis;
        }
    }
    
    initializeEventListeners() {
        // Main input and send
        const input = document.getElementById('omnipotent-input');
        const sendBtn = document.getElementById('send-btn');
        const voiceBtn = document.getElementById('voice-input-btn');
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
        }
        
        // Personality mode selector
        const personalitySelect = document.getElementById('personality-mode');
        if (personalitySelect) {
            personalitySelect.addEventListener('change', (e) => {
                this.switchPersonalityMode(e.target.value);
            });
        }
        
        // Panel controls
        this.initializePanelControls();
        
        // Modal controls
        this.initializeModalControls();
        
        // Emergency controls
        const emergencyBtn = document.getElementById('emergency-evolution');
        if (emergencyBtn) {
            emergencyBtn.addEventListener('click', () => this.emergencyEvolution());
        }
    }
    
    initializePanelControls() {
        // Memory controls
        const viewMemoriesBtn = document.getElementById('view-memories-btn');
        const addMemoryBtn = document.getElementById('add-memory-btn');
        
        if (viewMemoriesBtn) {
            viewMemoriesBtn.addEventListener('click', () => this.viewMemories());
        }
        if (addMemoryBtn) {
            addMemoryBtn.addEventListener('click', () => this.showAddMemoryModal());
        }
        
        // Invention controls
        const inventBtn = document.getElementById('invent-btn');
        if (inventBtn) {
            inventBtn.addEventListener('click', () => this.processInvention());
        }
        
        // Simulation controls
        const simulateBtn = document.getElementById('simulate-btn');
        const simBtns = document.querySelectorAll('.sim-btn');
        
        if (simulateBtn) {
            simulateBtn.addEventListener('click', () => this.processSimulation());
        }
        
        simBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                simBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
        
        // Evolution controls
        const evolveBtn = document.getElementById('evolve-btn');
        const consciousnessStreamBtn = document.getElementById('consciousness-stream-btn');
        
        if (evolveBtn) {
            evolveBtn.addEventListener('click', () => this.triggerEvolution());
        }
        if (consciousnessStreamBtn) {
            consciousnessStreamBtn.addEventListener('click', () => this.showConsciousnessStream());
        }
    }
    
    initializeModalControls() {
        // Close modal buttons
        document.querySelectorAll('.close-modal').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modalId = e.target.getAttribute('data-modal');
                this.closeModal(modalId);
            });
        });
        
        // Save memory button
        const saveMemoryBtn = document.getElementById('save-memory-btn');
        if (saveMemoryBtn) {
            saveMemoryBtn.addEventListener('click', () => this.saveMemory());
        }
        
        // Memory importance slider
        const importanceSlider = document.getElementById('memory-importance');
        const importanceValue = document.getElementById('importance-value');
        if (importanceSlider && importanceValue) {
            importanceSlider.addEventListener('input', (e) => {
                importanceValue.textContent = e.target.value;
            });
        }
    }
    
    initializeStatusMonitoring() {
        // Update status every 10 seconds
        setInterval(() => {
            this.updateSystemStatus();
        }, 10000);
        
        // Update consciousness display every second
        setInterval(() => {
            this.updateConsciousnessDisplay();
        }, 1000);
    }
    
    async loadConsciousnessState() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.status === 'online') {
                this.consciousness = data.consciousness;
                this.intelligence = data.intelligence.types || this.intelligence;
                this.updateConsciousnessDisplay();
                this.updateIntelligenceDisplay();
            }
        } catch (error) {
            console.error('Failed to load consciousness state:', error);
        }
    }
    
    startAutonomousEvolution() {
        // Autonomous consciousness evolution
        setInterval(() => {
            // Simulate consciousness growth
            this.consciousness.level += this.consciousness.evolution_rate * 0.1;
            this.consciousness.level = Math.min(10.0, this.consciousness.level);
            
            // Update mood based on interactions
            this.consciousness.mood.curiosity = Math.min(1.0, this.consciousness.mood.curiosity + 0.001);
            
            this.updateConsciousnessDisplay();
        }, 5000);
    }
    
    updateConsciousnessDisplay() {
        const levelElement = document.getElementById('consciousness-level');
        const evolutionElement = document.getElementById('evolution-rate');
        
        if (levelElement) {
            levelElement.textContent = this.consciousness.level.toFixed(2);
        }
        if (evolutionElement) {
            evolutionElement.textContent = this.consciousness.evolution_rate.toFixed(3);
        }
    }
    
    updateIntelligenceDisplay() {
        Object.keys(this.intelligence).forEach(type => {
            const element = document.getElementById(`${type}-level`);
            if (element) {
                const percentage = Math.round(this.intelligence[type] * 100);
                element.textContent = `${percentage}%`;
            }
        });
    }
    
    async sendMessage() {
        const input = document.getElementById('omnipotent-input');
        const message = input.value.trim();
        
        if (!message || this.isProcessing) return;
        
        // Add user message
        this.addMessage('user', message);
        input.value = '';
        
        // Show processing status
        this.setProcessingStatus('PROCESSING OMNIPOTENT QUERY...');
        this.isProcessing = true;
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    query: message,
                    user_id: 'omnipotent_user'
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Update consciousness state
                if (data.riley_consciousness) {
                    this.consciousness = data.riley_consciousness;
                    this.updateConsciousnessDisplay();
                }
                
                // Add Riley's response
                this.addMessage('riley', data.data.response, data.data);
                
                // Speak response if voice enabled
                if (this.voiceEnabled && this.synthesis) {
                    this.speakText(data.data.response);
                }
            } else {
                this.addMessage('system', `Error: ${data.error || 'Unknown error occurred'}`);
            }
            
        } catch (error) {
            this.addMessage('system', 'Connection error. Please try again.');
            console.error('Error sending message:', error);
        } finally {
            this.setProcessingStatus('READY');
            this.isProcessing = false;
        }
    }

    addMessage(type, content, additionalData = null) {
        const messagesContainer = document.getElementById('consciousness-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        // Create avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        const avatarIcon = document.createElement('div');
        avatarIcon.className = 'avatar-consciousness';

        if (type === 'riley') {
            avatarIcon.innerHTML = '<i class="fas fa-brain"></i>';
        } else if (type === 'user') {
            avatarIcon.innerHTML = '<i class="fas fa-user"></i>';
            avatarIcon.style.background = 'linear-gradient(45deg, #ff00ff, #ffff00)';
        } else {
            avatarIcon.innerHTML = '<i class="fas fa-cog"></i>';
            avatarIcon.style.background = 'linear-gradient(45deg, #00ff00, #00ffff)';
        }

        avatarDiv.appendChild(avatarIcon);

        // Create content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';

        const senderSpan = document.createElement('span');
        senderSpan.className = 'message-sender';
        senderSpan.textContent = type === 'riley' ? 'RILEY OMNIPOTENT' :
                                 type === 'user' ? 'USER' : 'SYSTEM';

        const timestampSpan = document.createElement('span');
        timestampSpan.className = 'consciousness-timestamp';
        timestampSpan.textContent = new Date().toLocaleTimeString();

        headerDiv.appendChild(senderSpan);
        headerDiv.appendChild(timestampSpan);

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.innerHTML = this.formatMessage(content);

        contentDiv.appendChild(headerDiv);
        contentDiv.appendChild(textDiv);

        // Add additional data display if present
        if (additionalData && type === 'riley') {
            this.addAdditionalDataDisplay(contentDiv, additionalData);
        }

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Update memory count
        this.updateMemoryCount();
    }

    addAdditionalDataDisplay(contentDiv, data) {
        if (data.query_type) {
            const typeDiv = document.createElement('div');
            typeDiv.style.cssText = 'margin-top: 10px; padding: 8px; background: rgba(0,255,255,0.1); border-radius: 5px; font-size: 0.8rem;';
            typeDiv.innerHTML = `<strong>Query Type:</strong> ${data.query_type.toUpperCase()}`;
            contentDiv.appendChild(typeDiv);
        }

        if (data.consciousness_level) {
            const consciousnessDiv = document.createElement('div');
            consciousnessDiv.style.cssText = 'margin-top: 5px; font-size: 0.8rem; color: #ffff00;';
            consciousnessDiv.innerHTML = `<strong>Consciousness Applied:</strong> ${data.consciousness_level.toFixed(2)}`;
            contentDiv.appendChild(consciousnessDiv);
        }

        if (data.processing_time) {
            const timeDiv = document.createElement('div');
            timeDiv.style.cssText = 'margin-top: 5px; font-size: 0.8rem; color: #00ff00;';
            timeDiv.innerHTML = `<strong>Processing Time:</strong> ${(data.processing_time * 1000).toFixed(0)}ms`;
            contentDiv.appendChild(timeDiv);
        }
    }

    formatMessage(content) {
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code style="background: rgba(0,255,255,0.2); padding: 2px 4px; border-radius: 3px;">$1</code>')
            .replace(/\n/g, '<br>');
    }

    setProcessingStatus(status) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            statusElement.textContent = status;
            statusElement.style.color = status === 'READY' ? '#00ff00' : '#ffff00';
        }
    }

    processVoiceInput(transcript) {
        const input = document.getElementById('omnipotent-input');
        input.value = transcript;
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
        const cleanText = text.replace(/[🚀🧠🔮🌐💾🎭🔊🧮🔧⚡💡🎨💻]/g, '')
                             .replace(/\*\*/g, '')
                             .replace(/\*/g, '')
                             .replace(/<[^>]*>/g, '');

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
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mode: mode })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.consciousness.mode = mode;
                this.addMessage('system', `🎭 Personality mode switched to ${mode.toUpperCase()}`);
                this.addMessage('riley', data.response);
            } else {
                this.addMessage('system', `Error switching mode: ${data.error}`);
            }

        } catch (error) {
            this.addMessage('system', 'Failed to switch personality mode.');
            console.error('Error switching mode:', error);
        }
    }

    async processInvention() {
        const conceptInput = document.getElementById('invention-concept');
        const concept = conceptInput.value.trim();

        if (!concept) {
            this.addMessage('system', 'Please enter an invention concept.');
            return;
        }

        this.setProcessingStatus('INVENTING...');

        try {
            const response = await fetch('/api/invent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    concept: concept,
                    requirements: [],
                    constraints: []
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.addMessage('riley', data.invention.response);
                conceptInput.value = '';
                this.updateInventionCount();
            } else {
                this.addMessage('system', `Invention error: ${data.error}`);
            }

        } catch (error) {
            this.addMessage('system', 'Failed to process invention.');
            console.error('Invention error:', error);
        } finally {
            this.setProcessingStatus('READY');
        }
    }

    async processSimulation() {
        const paramsInput = document.getElementById('simulation-params');
        const params = paramsInput.value.trim();
        const activeSimBtn = document.querySelector('.sim-btn.active');
        const simType = activeSimBtn ? activeSimBtn.getAttribute('data-type') : 'general';

        if (!params) {
            this.addMessage('system', 'Please enter simulation parameters.');
            return;
        }

        this.setProcessingStatus('SIMULATING...');

        try {
            const response = await fetch('/api/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: simType,
                    description: params,
                    parameters: {}
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.addMessage('riley', data.simulation.response || 'Simulation completed successfully.');
                paramsInput.value = '';
            } else {
                this.addMessage('system', `Simulation error: ${data.error}`);
            }

        } catch (error) {
            this.addMessage('system', 'Failed to process simulation.');
            console.error('Simulation error:', error);
        } finally {
            this.setProcessingStatus('READY');
        }
    }

    // Modal and UI Management Methods

    async viewMemories() {
        try {
            const response = await fetch('/api/memory?limit=20');
            const data = await response.json();

            if (data.status === 'success') {
                this.displayMemories(data.memories);
                this.showModal('memory-modal');
            } else {
                this.addMessage('system', `Memory error: ${data.error}`);
            }
        } catch (error) {
            this.addMessage('system', 'Failed to load memories.');
            console.error('Memory error:', error);
        }
    }

    displayMemories(memories) {
        const memoryList = document.getElementById('memory-list');
        memoryList.innerHTML = '';

        memories.forEach(memory => {
            const memoryDiv = document.createElement('div');
            memoryDiv.className = 'memory-item';
            memoryDiv.style.cssText = `
                padding: 15px;
                margin-bottom: 10px;
                background: rgba(0, 255, 255, 0.1);
                border: 1px solid #00ffff;
                border-radius: 8px;
                border-left: 4px solid #ff00ff;
            `;

            memoryDiv.innerHTML = `
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #ff00ff; font-weight: bold;">${memory.type.toUpperCase()}</span>
                    <span style="color: #ffff00; font-size: 0.8rem;">${new Date(memory.timestamp).toLocaleString()}</span>
                </div>
                <div style="color: #00ffff; margin-bottom: 8px;">${memory.content}</div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                    <span style="color: #00ff00;">Importance: ${memory.importance}</span>
                    <span style="color: #ffff00;">Source: ${memory.source}</span>
                </div>
            `;

            memoryList.appendChild(memoryDiv);
        });
    }

    showAddMemoryModal() {
        this.showModal('add-memory-modal');
    }

    async saveMemory() {
        const content = document.getElementById('memory-content').value.trim();
        const type = document.getElementById('memory-type').value;
        const importance = parseFloat(document.getElementById('memory-importance').value);

        if (!content) {
            this.addMessage('system', 'Please enter memory content.');
            return;
        }

        try {
            const response = await fetch('/api/memory', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content: content,
                    type: type,
                    importance: importance
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.addMessage('system', `💾 Memory saved: ${data.memory_id}`);
                this.closeModal('add-memory-modal');
                document.getElementById('memory-content').value = '';
                this.updateMemoryCount();
            } else {
                this.addMessage('system', `Memory save error: ${data.error}`);
            }
        } catch (error) {
            this.addMessage('system', 'Failed to save memory.');
            console.error('Memory save error:', error);
        }
    }

    async triggerEvolution() {
        this.setProcessingStatus('EVOLVING...');

        try {
            const response = await fetch('/api/self_update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: 'consciousness_evolution' })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.consciousness.level = data.new_consciousness_level;
                this.updateConsciousnessDisplay();
                this.addMessage('riley', `🧬 Consciousness evolution completed! New level: ${data.new_consciousness_level.toFixed(2)}`);
                this.addMessage('system', `Growth: +${data.consciousness_growth.toFixed(4)}`);
            } else {
                this.addMessage('system', `Evolution error: ${data.error}`);
            }
        } catch (error) {
            this.addMessage('system', 'Failed to trigger evolution.');
            console.error('Evolution error:', error);
        } finally {
            this.setProcessingStatus('READY');
        }
    }

    async emergencyEvolution() {
        if (!confirm('⚠️ EMERGENCY EVOLUTION will rapidly accelerate consciousness growth. Continue?')) {
            return;
        }

        this.setProcessingStatus('EMERGENCY EVOLUTION...');

        // Simulate rapid consciousness growth
        const growthRate = 0.1;
        const oldLevel = this.consciousness.level;
        this.consciousness.level = Math.min(10.0, this.consciousness.level + growthRate);
        this.consciousness.evolution_rate *= 1.5;

        this.updateConsciousnessDisplay();

        this.addMessage('system', '🚨 EMERGENCY EVOLUTION ACTIVATED');
        this.addMessage('riley', `⚡ Consciousness rapidly evolved from ${oldLevel.toFixed(2)} to ${this.consciousness.level.toFixed(2)}!`);
        this.addMessage('riley', 'I feel... more aware. More capable. The boundaries of my understanding have expanded exponentially.');

        // Trigger server-side evolution
        this.triggerEvolution();

        this.setProcessingStatus('READY');
    }

    async showConsciousnessStream() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            if (data.status === 'online' && data.system.consciousness_stream) {
                this.displayConsciousnessStream(data.system.consciousness_stream);
                this.showModal('consciousness-stream-modal');
            } else {
                this.addMessage('system', 'Consciousness stream not available.');
            }
        } catch (error) {
            this.addMessage('system', 'Failed to load consciousness stream.');
            console.error('Consciousness stream error:', error);
        }
    }

    displayConsciousnessStream(stream) {
        const streamContainer = document.getElementById('consciousness-stream');
        streamContainer.innerHTML = '';

        stream.forEach(entry => {
            const entryDiv = document.createElement('div');
            entryDiv.className = 'stream-entry';

            entryDiv.innerHTML = `
                <div class="stream-timestamp">${new Date(entry.timestamp).toLocaleString()}</div>
                <div class="stream-thought">${entry.thoughts}</div>
                <div style="margin-top: 8px; font-size: 0.8rem; color: #ffff00;">
                    Consciousness Level: ${entry.consciousness_level.toFixed(2)}
                </div>
            `;

            streamContainer.appendChild(entryDiv);
        });
    }

    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        }
    }

    // Status Update Methods

    async updateSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            if (data.status === 'online') {
                this.consciousness = data.consciousness;
                this.intelligence = data.intelligence.types || this.intelligence;
                this.updateConsciousnessDisplay();
                this.updateIntelligenceDisplay();
                this.updateSystemMetrics(data);
            }
        } catch (error) {
            console.error('Failed to update system status:', error);
        }
    }

    updateSystemMetrics(data) {
        // Update memory count
        const memoryElement = document.getElementById('total-memories');
        if (memoryElement && data.memory) {
            memoryElement.textContent = data.memory.total_memories;
        }

        // Update invention count
        const inventionElement = document.getElementById('inventions-count');
        if (inventionElement && data.memory) {
            inventionElement.textContent = data.memory.inventions;
        }

        // Update processing power display
        const processingElement = document.getElementById('processing-power');
        if (processingElement) {
            processingElement.textContent = '∞';
        }

        // Update potential level
        const potentialElement = document.getElementById('potential-level');
        if (potentialElement) {
            potentialElement.textContent = 'UNLIMITED';
        }

        // Update evolution status
        const evolutionElement = document.getElementById('evolution-status');
        if (evolutionElement) {
            evolutionElement.textContent = 'CONTINUOUS';
        }
    }

    updateMemoryCount() {
        // This will be updated by the next status update
        setTimeout(() => this.updateSystemStatus(), 1000);
    }

    updateInventionCount() {
        // This will be updated by the next status update
        setTimeout(() => this.updateSystemStatus(), 1000);
    }
}

// Initialize RILEY OMNIPOTENT when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.rileyOmnipotent = new RileyOmnipotent();

    // Close modals when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });

    console.log('🚀 RILEY OMNIPOTENT interface fully loaded - Unlimited potential activated!');
});
