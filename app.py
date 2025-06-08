from flask import Flask, render_template, request, jsonify
import datetime
import random
import os
import sys

# Add jarvis to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'jarvis'))

app = Flask(__name__)

# Import Riley's advanced systems (lazy loading for Railway compatibility)
ADVANCED_RILEY = False
RileyGenesis = None
PersonalityMode = None
MHDGEngine = None
RileyConversationEngine = None

def load_advanced_systems():
    global ADVANCED_RILEY, RileyGenesis, PersonalityMode, MHDGEngine, RileyConversationEngine
    if not ADVANCED_RILEY:
        try:
            from jarvis.core.riley_genesis import RileyGenesis, PersonalityMode
            from jarvis.core.mhdg_engine import MHDGEngine
            from jarvis.core.riley_conversation_engine import RileyConversationEngine
            ADVANCED_RILEY = True
            print("🚀 RILEY GENESIS systems loaded successfully!")
            return True
        except Exception as e:
            print(f"⚠️ Advanced Riley systems not available: {e}")
            return False
    return ADVANCED_RILEY

class RileyAdvanced:
    """Enhanced Riley with full GENESIS capabilities"""

    def __init__(self):
        if ADVANCED_RILEY:
            try:
                self.genesis = RileyGenesis()
                self.mhdg_engine = MHDGEngine()
                self.conversation_engine = RileyConversationEngine()
                self.personality = self.genesis.personality.mode.value
                self.memory = []
                print("🧠 RILEY GENESIS fully initialized with advanced capabilities!")
            except Exception as e:
                print(f"⚠️ Error initializing advanced systems, falling back to basic mode: {e}")
                self.personality = "friendly"
                self.memory = []
                global ADVANCED_RILEY
                ADVANCED_RILEY = False
                print("🤖 Basic Riley initialized (fallback)")
        else:
            self.personality = "friendly"
            self.memory = []
            print("🤖 Basic Riley initialized")

    def respond(self, message):
        try:
            if ADVANCED_RILEY and hasattr(self, 'genesis'):
                return self._advanced_respond(message)
            else:
                return self._basic_respond(message)
        except Exception as e:
            print(f"⚠️ Error in respond method: {e}")
            return self._basic_respond(message)

    def _advanced_respond(self, message):
        try:
            self.memory.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "user": message,
                "type": "user_input"
            })

            if message.startswith('!'):
                parts = message.split(' ', 1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                response = self.genesis.process_command(command, args)

            elif any(term in message.lower() for term in ["calculate", "mhdg", "magnetic field", "anti-gravity", "plasma"]):
                response = self._handle_mhdg_request(message)

            else:
                response = self.conversation_engine.process_human_conversation(message)

            self.memory.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "riley": response,
                "type": "riley_response"
            })

            return response

        except Exception as e:
            print(f"Error in advanced response: {e}")
            return self._basic_respond(message)

    def _handle_mhdg_request(self, message):
        message_lower = message.lower()

        if "magnetic field" in message_lower:
            result = self.mhdg_engine.calculate_magnetic_field(1.5, 1000, 0.1)
            return f"🧮 Magnetic field calculation: {result.result:.2e} {result.units}. {result.explanation}"

        elif "anti-gravity" in message_lower or "anti gravity" in message_lower:
            result = self.mhdg_engine.calculate_anti_gravity_potential(1.5, 9.81)
            return f"🛸 Anti-gravity potential: {result.result:.2e} {result.units}. {result.explanation}"

        elif "plasma" in message_lower:
            result = self.mhdg_engine.calculate_plasma_confinement(2.0)
            return f"🔥 Plasma confinement: {result.result:.2e} {result.units}. {result.explanation}"

        elif "device" in message_lower and "design" in message_lower:
            design = self.mhdg_engine.design_anti_gravity_device(1000, 1e6)
            return f"🛸 Anti-gravity device design: Required field: {design['required_magnetic_field']:.2e}T, Power: {design['estimated_power']:.2e}W, Feasible: {design['feasible']}"

        else:
            return "🧮 MHDG theory encompasses magnetic-gravitational field interactions. I can help with calculations for magnetic fields, anti-gravity potential, plasma confinement, or device design. What specific calculation would you like?"

    def _basic_respond(self, message):
        message = message.lower().strip()
        self.memory.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user": message,
            "type": "user_input"
        })

        if "hello" in message or "hi" in message:
            responses = [
                "Hello! I'm Riley, your advanced AI assistant. How can I help you today?",
                "Hi there! Riley here, ready to assist you with anything you need!",
                "Hey! Great to meet you. I'm Riley - what would you like to explore together?"
            ]
            response = random.choice(responses)

        elif "riley" in message and "who" in message:
            response = "I'm Riley, an advanced AI assistant with GENESIS capabilities. I specialize in MHDG theory, scientific calculations, invention assistance, and human-like conversation!"

        elif "mhdg" in message or "magnetic" in message:
            response = "MHDG (Magneto-Hydrodynamic Gravity) theory is fascinating! It explores the relationship between magnetic fields and gravitational effects. I can perform calculations and help with theoretical device design!"

        elif "invent" in message or "invention" in message:
            inventions = [
                "How about a magnetic levitation device using counter-rotating fields?",
                "I'm thinking of a plasma-based energy harvester that could revolutionize power generation!",
                "What about a gravitational wave detector using MHDG principles?",
                "Consider a magnetic field generator that could create localized gravity wells!"
            ]
            response = f"Great question about inventions! {random.choice(inventions)} What type of invention interests you most?"

        else:
            responses = [
                f"That's an interesting point about '{message}'. Could you tell me more?",
                f"I find your question about '{message}' quite intriguing. What would you like to explore?",
                "That's a great question! I'm processing multiple angles on this. What's your main interest here?",
                "Fascinating! I can see several ways to approach this. What outcome are you hoping to achieve?"
            ]
            response = random.choice(responses)

        self.memory.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "riley": response,
            "type": "riley_response"
        })

        return response

    def get_status(self):
        try:
            if ADVANCED_RILEY and hasattr(self, 'genesis'):
                return self.genesis.get_personality_status()
            else:
                return {
                    "mode": self.personality,
                    "memory_count": len(self.memory),
                    "advanced_systems": False
                }
        except Exception as e:
            print(f"⚠️ Error getting status: {e}")
            return {
                "mode": self.personality,
                "memory_count": len(self.memory),
                "advanced_systems": False,
                "error": str(e)
            }

    def switch_personality(self, mode):
        try:
            if ADVANCED_RILEY and hasattr(self, 'genesis'):
                try:
                    personality_mode = PersonalityMode(mode.lower())
                    return self.genesis.switch_personality_mode(personality_mode)
                except ValueError:
                    return f"Invalid mode. Available: {', '.join([m.value for m in PersonalityMode])}"
                except Exception as e:
                    print(f"⚠️ Error switching personality: {e}")
                    self.personality = mode
                    return f"Switched to {mode} mode (basic fallback)"
            else:
                self.personality = mode
                return f"Switched to {mode} mode (basic)"
        except Exception as e:
            print(f"⚠️ Error in switch_personality: {e}")
            self.personality = mode
            return f"Switched to {mode} mode (error fallback)"

# Initialize Enhanced Riley (moved to after routes to prevent startup crashes)
riley = None

def get_riley():
    """Lazy initialization of Riley to prevent startup crashes"""
    global riley
    if riley is None:
        try:
            # Try to load advanced systems first
            load_advanced_systems()
            riley = RileyAdvanced()
        except Exception as e:
            print(f"⚠️ Error initializing Riley: {e}")
            # Create a minimal fallback Riley
            class BasicRiley:
                def __init__(self):
                    self.personality = "friendly"
                    self.memory = []

                def respond(self, message):
                    responses = [
                        f"Hello! I'm Riley. You said: '{message}' - How can I help you today?",
                        f"Hi there! I heard you say '{message}'. What would you like to explore?",
                        f"Great to meet you! Regarding '{message}' - I'm here to assist you!"
                    ]
                    import random
                    return random.choice(responses)

                def get_status(self):
                    return {"mode": "basic", "status": "online", "advanced_systems": False}

                def switch_personality(self, mode):
                    self.personality = mode
                    return f"Switched to {mode} mode (basic)"

            riley = BasicRiley()
    return riley

# Home route moved below to include error handling

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        riley_instance = get_riley()
        response = riley_instance.respond(user_message)

        return jsonify({
            'response': response,
            'status': 'success',
            'timestamp': datetime.datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for Railway - Absolutely bulletproof"""
    return "OK"

@app.route('/healthz')
def healthz():
    """Alternative health check endpoint"""
    return "healthy"

@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return "pong"

@app.route('/')
def home():
    """Root endpoint that also serves as health check"""
    try:
        return render_template('index.html')
    except:
        return "Riley AI is online", 200

@app.route('/status')
def status():
    try:
        riley_instance = get_riley()
        riley_status = riley_instance.get_status()
        return jsonify({
            'status': 'Riley AI GENESIS is online and ready!',
            'version': '2.0.0-GENESIS',
            'advanced_systems': ADVANCED_RILEY,
            'personality': riley_instance.personality,
            'memory_entries': len(riley_instance.memory),
            'riley_status': riley_status,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'Riley AI is online (basic mode)',
            'version': '2.0.0-GENESIS',
            'advanced_systems': False,
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        })

@app.route('/api/genesis/status')
def genesis_status():
    riley_status = riley.get_status()
    return jsonify({
        'status': 'online',
        'core_status': 'active',
        'voice_status': 'ready',
        'web_status': 'connected',
        'mhdg_status': 'active',
        'advanced_systems': ADVANCED_RILEY,
        'personality': riley.personality,
        'memory_entries': len(riley.memory),
        'learning_rate': 'active',
        'knowledge_size': 'expanding',
        'riley_genesis': riley_status,
        'capabilities': {
            'mhdg_calculations': ADVANCED_RILEY,
            'human_conversation': ADVANCED_RILEY,
            'personality_switching': ADVANCED_RILEY,
            'memory_system': ADVANCED_RILEY,
            'command_processing': ADVANCED_RILEY
        },
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/genesis/personality', methods=['POST'])
def switch_personality():
    try:
        data = request.get_json()
        new_personality = data.get('personality', 'assistant')
        result = riley.switch_personality(new_personality)
        return jsonify({
            'status': 'success',
            'personality': new_personality,
            'message': result,
            'advanced_systems': ADVANCED_RILEY,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mhdg/calculate', methods=['POST'])
def mhdg_calculate():
    try:
        if not ADVANCED_RILEY:
            return jsonify({'error': 'Advanced MHDG systems not available'}), 503

        data = request.get_json()
        calc_type = data.get('type', 'magnetic_field')

        if calc_type == 'magnetic_field':
            current = data.get('current', 1.0)
            turns = data.get('turns', 1000)
            length = data.get('length', 0.1)
            result = riley.mhdg_engine.calculate_magnetic_field(current, turns, length)

        elif calc_type == 'anti_gravity':
            magnetic_field = data.get('magnetic_field', 1.5)
            gravitational_field = data.get('gravitational_field', 9.81)
            result = riley.mhdg_engine.calculate_anti_gravity_potential(magnetic_field, gravitational_field)

        elif calc_type == 'plasma_confinement':
            magnetic_field = data.get('magnetic_field', 2.0)
            result = riley.mhdg_engine.calculate_plasma_confinement(magnetic_field)

        elif calc_type == 'device_design':
            target_force = data.get('target_force', 1000)
            available_power = data.get('available_power', 1e6)
            result = riley.mhdg_engine.design_anti_gravity_device(target_force, available_power)
            return jsonify({
                'status': 'success',
                'calculation_type': calc_type,
                'result': result,
                'timestamp': datetime.datetime.now().isoformat()
            })
        else:
            return jsonify({'error': f'Unknown calculation type: {calc_type}'}), 400

        return jsonify({
            'status': 'success',
            'calculation_type': result.calculation_type,
            'result': result.result,
            'units': result.units,
            'confidence': result.confidence,
            'explanation': result.explanation,
            'input_parameters': result.input_parameters,
            'timestamp': datetime.datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Railway-compatible launch block
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Riley GENESIS on port {port}")
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Error starting Riley: {e}")
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
