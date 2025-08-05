import csv
import os
import re
import threading
import time
import json
import numpy as np
from datetime import datetime
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

class NLPEnhancedChatbot:
    def __init__(self, csv_file_path=None):
        self.qa_pairs = []
        self.original_qa_count = 0  # Track original count for learning statistics
        self.context_data = ""
        self.model = None
        self.tokenizer = None
        self.model_type = "Loading..."
        self.model_loading = True
        
        # ML/RL components
        self.conversation_history = []
        self.feedback_scores = {}
        self.response_quality = {}
        self.learning_rate = 0.1
        self.vectorizer = None
        self.qa_vectors = None
        
        # Advanced NLP components
        self.sentence_transformer = None
        self.nlp_processor = None
        self.intent_classifier = None
        self.context_embeddings = None
        self.domain_knowledge = {}
        
        # Load Q&A data if available
        if csv_file_path and os.path.exists(csv_file_path):
            self.load_qa_data(csv_file_path)
        
        # Initialize NLP components
        self.initialize_nlp_components()
        
        # Start model loading in background thread
        self.model_loading_thread = threading.Thread(target=self.initialize_model, daemon=True)
        self.model_loading_thread.start()
        
    def initialize_nlp_components(self):
        """Initialize advanced NLP components for semantic understanding"""
        try:
            print("Initializing advanced NLP components...")
            
            # Initialize sentence transformer for semantic embeddings
            self.initialize_sentence_transformer()
            
            # Initialize intent classification
            self.initialize_intent_classifier()
            
            # Build domain knowledge from Q&A pairs
            self.build_domain_knowledge()
            
            # Create semantic embeddings for existing data
            if self.qa_pairs:
                self.create_semantic_embeddings()
            
            print("✓ Advanced NLP components initialized successfully")
            
        except Exception as e:
            print(f"Error initializing NLP components: {e}")
            # Fallback to basic TF-IDF
            self.initialize_fallback_ml()
    
    def initialize_sentence_transformer(self):
        """Initialize sentence transformer for semantic understanding"""
        try:
            from sentence_transformers import SentenceTransformer
            
            # Use a lightweight but effective model
            model_name = 'all-MiniLM-L6-v2'
            print(f"Loading sentence transformer: {model_name}")
            self.sentence_transformer = SentenceTransformer(model_name)
            print("✓ Sentence transformer loaded successfully")
            
        except ImportError:
            print("⚠ sentence-transformers not available, using fallback")
            self.sentence_transformer = None
        except Exception as e:
            print(f"Error loading sentence transformer: {e}")
            self.sentence_transformer = None
    
    def initialize_intent_classifier(self):
        """Initialize intent classification for understanding user queries"""
        try:
            # Define common healthcare intents
            self.intent_patterns = {
                'appointment': ['appointment', 'book', 'schedule', 'visit', 'consultation', 'see doctor'],
                'pricing': ['price', 'cost', 'how much', 'expensive', 'fee', 'charge', 'bill'],
                'hospital_info': ['hours', 'visiting', 'location', 'address', 'directions', 'parking'],
                'emergency': ['emergency', 'urgent', 'ambulance', '911', 'critical', 'accident'],
                'departments': ['department', 'specialist', 'doctor', 'cardiology', 'neurology', 'oncology'],
                'insurance': ['insurance', 'cover', 'nhif', 'payment', 'billing', 'claim'],
                'medical_records': ['records', 'results', 'report', 'test', 'x-ray', 'lab'],
                'symptoms': ['pain', 'fever', 'headache', 'chest', 'stomach', 'symptoms'],
                'pharmacy': ['medicine', 'prescription', 'drug', 'pharmacy', 'medication'],
                'general': ['hello', 'hi', 'greetings', 'thank you', 'bye', 'goodbye', 'help']
            }
            
            print("✓ Intent classification patterns loaded")
            
        except Exception as e:
            print(f"Error initializing intent classifier: {e}")
    
    def build_domain_knowledge(self):
        """Build domain knowledge from Q&A pairs and medical data"""
        try:
            # Extract key concepts and entities from medical Q&A data
            self.domain_knowledge = {
                'departments': set(),
                'procedures': set(),
                'hospitals': set(),
                'symptoms': set(),
                'treatments': set(),
                'insurance_types': set()
            }
            
            for qa in self.qa_pairs:
                text = (qa['question'] + ' ' + qa['answer']).lower()
                
                # Extract product-related terms
                if any(term in text for term in ['car', 'phone', 'laptop', 'house', 'land']):
                    words = text.split()
                    for word in words:
                        if len(word) > 3 and word.isalpha():
                            self.domain_knowledge['products'].add(word)
                
                # Extract payment methods
                if any(term in text for term in ['pay', 'payment', 'money', 'cash']):
                    self.domain_knowledge['payment_methods'].update(['mobile money', 'cash', 'card', 'bank transfer'])
            
            print(f"✓ Domain knowledge built: {len(self.domain_knowledge['products'])} product terms")
            
        except Exception as e:
            print(f"Error building domain knowledge: {e}")
    
    def create_semantic_embeddings(self):
        """Create semantic embeddings for all Q&A pairs"""
        try:
            if not self.sentence_transformer:
                return
                
            # Create embeddings for questions and answers
            questions = [qa['question'] for qa in self.qa_pairs]
            answers = [qa['answer'] for qa in self.qa_pairs]
            
            print("Creating semantic embeddings...")
            self.question_embeddings = self.sentence_transformer.encode(questions)
            self.answer_embeddings = self.sentence_transformer.encode(answers)
            
            print(f"✓ Created embeddings for {len(questions)} Q&A pairs")
            
        except Exception as e:
            print(f"Error creating semantic embeddings: {e}")
    
    def initialize_fallback_ml(self):
        """Fallback ML initialization if advanced NLP fails"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            print("Initializing fallback ML components...")
            
            # Initialize TF-IDF vectorizer for semantic matching
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Load conversation history if exists
            self.load_conversation_history()
            
            # Load feedback scores if exists
            self.load_feedback_scores()
            
            print("ML components initialized successfully")
            
        except ImportError:
            print("WARNING: scikit-learn not available. Using basic matching.")
            self.vectorizer = None
            
    def load_conversation_history(self):
        """Load previous conversation history for learning"""
        try:
            if os.path.exists('conversation_history.json'):
                with open('conversation_history.json', 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
                print(f"Loaded {len(self.conversation_history)} previous conversations")
        except Exception as e:
            print(f"Could not load conversation history: {e}")
            
    def save_conversation_history(self):
        """Save conversation history for future learning"""
        try:
            # Keep only last 1000 conversations to prevent file from growing too large
            recent_history = self.conversation_history[-1000:] if len(self.conversation_history) > 1000 else self.conversation_history
            
            with open('conversation_history.json', 'w', encoding='utf-8') as f:
                json.dump(recent_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Could not save conversation history: {e}")
            
    def load_feedback_scores(self):
        """Load user feedback scores for reinforcement learning"""
        try:
            if os.path.exists('feedback_scores.json'):
                with open('feedback_scores.json', 'r', encoding='utf-8') as f:
                    self.feedback_scores = json.load(f)
                print(f"Loaded feedback for {len(self.feedback_scores)} response patterns")
        except Exception as e:
            print(f"Could not load feedback scores: {e}")
            
    def save_feedback_scores(self):
        """Save feedback scores for reinforcement learning"""
        try:
            with open('feedback_scores.json', 'w', encoding='utf-8') as f:
                json.dump(self.feedback_scores, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Could not save feedback scores: {e}")
    
    def load_qa_data(self, file_path):
        """Load questions and answers from CSV file and create ML vectors"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Handle both old format (Question/Answer) and new format (question/answer)
                    question = row.get("question", row.get("Question", "")).strip().strip('"')
                    answer = row.get("answer", row.get("Answer", "")).strip().strip('"')
                    category = row.get("category", "general")
                    hospital = row.get("hospital", "both")
                    
                    self.qa_pairs.append({
                        "question": question, 
                        "answer": answer,
                        "category": category,
                        "hospital": hospital
                    })
                    # Add to context for the model
                    self.context_data += f"Q: {question}\nA: {answer}\n\n"
            
            print(f"Loaded {len(self.qa_pairs)} medical Q&A pairs from hospital dataset")
            
            # Set original count for learning statistics
            self.original_qa_count = len(self.qa_pairs)
            
            # Create TF-IDF vectors for ML-enhanced matching
            self.create_qa_vectors()
            
        except Exception as e:
            print(f"Error loading Q&A data: {e}")
            
    def create_qa_vectors(self):
        """Create TF-IDF vectors for all Q&A pairs for semantic matching"""
        try:
            if self.vectorizer and self.qa_pairs:
                questions = [qa["question"] for qa in self.qa_pairs]
                self.qa_vectors = self.vectorizer.fit_transform(questions)
                print("Created TF-IDF vectors for semantic matching")
        except Exception as e:
            print(f"Could not create vectors: {e}")
            
    def get_nlp_enhanced_answer(self, user_input):
        """Use advanced NLP for semantic understanding and dynamic answer generation"""
        
        # Step 1: Intent Classification
        intent = self.classify_intent(user_input)
        
        # Step 2: Semantic Understanding with Sentence Transformers
        if self.sentence_transformer and hasattr(self, 'question_embeddings'):
            semantic_answer = self.get_semantic_answer(user_input, intent)
            if semantic_answer:
                return semantic_answer
        
        # Step 3: Dynamic Answer Generation
        dynamic_answer = self.generate_dynamic_answer(user_input, intent)
        if dynamic_answer:
            return dynamic_answer
        
        # Fallback to ML approach
        return self.get_ml_context_answer(user_input)
    
    def classify_intent(self, user_input):
        """Classify the intent of the user input"""
        user_input_lower = user_input.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in user_input_lower:
                    score += 1
            intent_scores[intent] = score
        
        # Return the intent with highest score, or 'general' if no clear intent
        if max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'general'
    
    def get_semantic_answer(self, user_input, intent):
        """Get answer using semantic similarity with sentence transformers"""
        try:
            if not self.sentence_transformer or not hasattr(self, 'question_embeddings'):
                return None
            
            # Encode the user input
            user_embedding = self.sentence_transformer.encode([user_input])
            
            # Calculate semantic similarity with questions
            similarities = np.dot(user_embedding, self.question_embeddings.T).flatten()
            
            # Find best matches
            best_indices = np.argsort(similarities)[::-1][:3]
            best_scores = similarities[best_indices]
            
            # Check if best match is semantically similar (threshold of 0.3)
            if best_scores[0] > 0.3:
                best_match = self.qa_pairs[best_indices[0]]
                
                # Generate contextual response based on intent
                enhanced_answer = self.enhance_answer_with_intent(
                    best_match['answer'], intent, user_input
                )
                
                return {
                    'answer': enhanced_answer,
                    'confidence': float(best_scores[0]),
                    'source': 'semantic_nlp',
                    'intent': intent,
                    'method': 'sentence_transformer'
                }
            
            return None
            
        except Exception as e:
            print(f"Error in semantic answer generation: {e}")
            return None
    
    def enhance_answer_with_intent(self, base_answer, intent, user_input):
        """Enhance the answer based on detected intent and context"""
        
        # Intent-specific enhancements
        if intent == 'pricing':
            if 'varies' in base_answer.lower() or 'depend' in base_answer.lower():
                return f"{base_answer} For specific pricing information, please contact our sales team or check the latest listings on our platform."
        
        elif intent == 'availability':
            return f"{base_answer} Please check our current inventory or contact us for real-time availability."
        
        elif intent == 'comparison':
            return f"{base_answer} Would you like me to help you compare specific features or models?"
        
        elif intent == 'support':
            return f"{base_answer} If you need additional assistance, please don't hesitate to contact our customer support team."
        
        elif intent == 'payment':
            return f"{base_answer} We accept multiple payment methods for your convenience."
        
        return base_answer
    
    def generate_dynamic_answer(self, user_input, intent):
        """Generate dynamic answers based on intent and medical domain knowledge"""
        
        # Extract key entities from user input
        entities = self.extract_entities(user_input)
        
        # Generate intent-specific responses
        if intent == 'appointment':
            return self.generate_appointment_response(entities, user_input)
        
        elif intent == 'pricing':
            return self.generate_pricing_response(entities, user_input)
        
        elif intent == 'hospital_info':
            return self.generate_hospital_info_response(entities, user_input)
        
        elif intent == 'emergency':
            return self.generate_emergency_response(entities, user_input)
        
        elif intent == 'departments':
            return self.generate_departments_response(entities, user_input)
        
        elif intent == 'insurance':
            return self.generate_insurance_response(user_input)
        
        elif intent == 'medical_records':
            return self.generate_medical_records_response(user_input)
        
        elif intent == 'symptoms':
            return self.generate_symptoms_response(entities, user_input)
        
        elif intent == 'pharmacy':
            return self.generate_pharmacy_response(user_input)
        
        elif intent == 'general':
            return self.generate_general_response(user_input)
        
        return None
    
    def extract_entities(self, user_input):
        """Extract relevant medical entities from user input"""
        entities = {
            'departments': [],
            'symptoms': [],
            'hospitals': [],
            'numbers': [],
            'dates': []
        }
        
        words = user_input.lower().split()
        
        # Extract potential product names
        for word in words:
            if word in self.domain_knowledge.get('products', set()):
                entities['products'].append(word)
        
        # Extract numbers (for pricing, quantities, etc.)
        import re
        numbers = re.findall(r'\d+', user_input)
        entities['numbers'] = numbers
        
        return entities
    
    def generate_pricing_response(self, entities, user_input):
        """Generate dynamic medical pricing responses"""
        return {
            'answer': "Medical service pricing varies by procedure and hospital. General ranges: CT scan 8,000-25,000 KSh, Normal delivery 25,000-120,000 KSh, C-section 60,000-200,000 KSh. Insurance coverage available. Contact billing for specific procedures.",
            'confidence': 0.7,
            'source': 'dynamic_generation',
            'intent': 'pricing',
            'method': 'template_based'
        }
    
    def generate_general_response(self, user_input):
        """Generate general responses for unclear intents"""
        greetings = ['hello', 'hi', 'hey', 'greetings']
        gratitude = ['thank', 'thanks', 'appreciate']
        farewell = ['bye', 'goodbye', 'farewell', 'see you']
        
        user_lower = user_input.lower()
        
        if any(greeting in user_lower for greeting in greetings):
            return {
                'answer': "Hello! Welcome to Hospital AI Agent. I'm here to help you with medical information about Nairobi Hospital and Kenyatta National Hospital. How can I assist you today?",
                'confidence': 0.9,
                'source': 'dynamic_generation',
                'intent': 'general',
                'method': 'template_based'
            }
        
        elif any(thanks in user_lower for thanks in gratitude):
            return {
                'answer': "You're very welcome! I'm glad I could help with your medical information needs. If you have other health-related questions, please don't hesitate to ask.",
                'confidence': 0.9,
                'source': 'dynamic_generation',
                'intent': 'general',
                'method': 'template_based'
            }
        
        elif any(bye in user_lower for bye in farewell):
            return {
                'answer': "Thank you for using our Hospital AI Agent! Stay healthy and feel free to contact us anytime for medical information assistance.",
                'confidence': 0.9,
                'source': 'dynamic_generation',
                'intent': 'general',
                'method': 'template_based'
            }
        
        # Default general response
        return {
            'answer': "I'm here to help with medical information about Nairobi Hospital and Kenyatta National Hospital. You can ask about appointments, services, pricing, departments, or emergency contacts.",
            'confidence': 0.6,
            'source': 'dynamic_generation',
            'intent': 'general',
            'method': 'template_based'
        }
        
    def generate_appointment_response(self, entities, user_input):
        """Generate appointment booking responses"""
        return {
            'answer': "To book an appointment: Nairobi Hospital: +254-20-2845000 or online portal. Kenyatta National Hospital: +254-20-2726300. For specialists, please book 2-3 days in advance. Emergency services available 24/7.",
            'confidence': 0.8,
            'source': 'dynamic_generation',
            'intent': 'appointment',
            'method': 'template_based'
        }
    
    def generate_emergency_response(self, entities, user_input):
        """Generate emergency contact responses"""
        return {
            'answer': "EMERGENCY CONTACTS: Nairobi Hospital: +254-20-2845000 | Kenyatta National: +254-20-2726300 | Both hospitals operate 24/7 emergency services. For life-threatening situations, call immediately.",
            'confidence': 0.9,
            'source': 'dynamic_generation',
            'intent': 'emergency',
            'method': 'template_based'
        }
    
    def generate_hospital_info_response(self, entities, user_input):
        """Generate hospital information responses"""
        return {
            'answer': "Hospital Information: Visiting hours vary by department. General wards: 2PM-4PM & 6PM-8PM daily. ICU: 3PM-4PM only. Both hospitals have 24/7 emergency services, pharmacies, and parking facilities.",
            'confidence': 0.8,
            'source': 'dynamic_generation',
            'intent': 'hospital_info',
            'method': 'template_based'
        }
    
    def generate_departments_response(self, entities, user_input):
        """Generate department information responses"""
        return {
            'answer': "Available departments: Cardiology, Neurology, Oncology, Pediatrics, Orthopedics, Radiology, Emergency Medicine, Maternity, Surgery, Internal Medicine, Psychiatry, Dermatology, and more. Specialist appointments available.",
            'confidence': 0.8,
            'source': 'dynamic_generation',
            'intent': 'departments',
            'method': 'template_based'
        }
    
    def generate_insurance_response(self, user_input):
        """Generate insurance information responses"""
        return {
            'answer': "Insurance accepted: NHIF, AAR, CIC, Jubilee, Resolution, Madison, APA. Both hospitals offer direct billing for approved insurance. Please check with billing department for specific coverage details.",
            'confidence': 0.8,
            'source': 'dynamic_generation',
            'intent': 'insurance',
            'method': 'template_based'
        }
    
    def generate_medical_records_response(self, user_input):
        """Generate medical records information responses"""
        return {
            'answer': "Medical Records: Nairobi Hospital - online portal or Medical Records dept. Kenyatta National - apply at Records office with ID. Digital records available for recent patients. Lab results available online.",
            'confidence': 0.8,
            'source': 'dynamic_generation',
            'intent': 'medical_records',
            'method': 'template_based'
        }
    
    def generate_symptoms_response(self, entities, user_input):
        """Generate symptom-related responses"""
        return {
            'answer': "For medical symptoms, please consult with a healthcare professional. Both hospitals offer emergency services 24/7. For non-emergency consultations, book an appointment with the appropriate specialist department.",
            'confidence': 0.7,
            'source': 'dynamic_generation',
            'intent': 'symptoms',
            'method': 'template_based'
        }
    
    def generate_pharmacy_response(self, user_input):
        """Generate pharmacy information responses"""
        return {
            'answer': "Pharmacy services: Both hospitals have 24/7 pharmacies with prescription medications and over-the-counter drugs. Nairobi Hospital offers home delivery service. Bring valid prescription for medications.",
            'confidence': 0.8,
            'source': 'dynamic_generation',
            'intent': 'pharmacy',
            'method': 'template_based'
        }
        
        return None
    
    def get_ml_context_answer(self, user_input):
        """Fallback ML method for enhanced context matching"""
        if not self.qa_pairs or not self.vectorizer or self.qa_vectors is None:
            return self.get_basic_context_answer(user_input)
            
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Vectorize user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate cosine similarity with all Q&A pairs
            similarities = cosine_similarity(user_vector, self.qa_vectors).flatten()
            
            # Find best matches
            best_indices = np.argsort(similarities)[::-1][:3]  # Top 3 matches
            best_scores = similarities[best_indices]
            
            # Check if best match is good enough (threshold of 0.1)
            if best_scores[0] > 0.1:
                best_match = self.qa_pairs[best_indices[0]]
                
                # Apply reinforcement learning adjustment
                pattern_key = f"{user_input.lower()[:50]}||{best_match['answer'][:50]}"
                feedback_multiplier = self.feedback_scores.get(pattern_key, 1.0)
                adjusted_score = best_scores[0] * feedback_multiplier
                
                # Store response quality for learning
                self.response_quality[pattern_key] = {
                    'base_score': float(best_scores[0]),
                    'feedback_multiplier': feedback_multiplier,
                    'final_score': adjusted_score,
                    'timestamp': datetime.now().isoformat()
                }
                
                return {
                    'answer': best_match['answer'],
                    'confidence': min(adjusted_score * 2, 1.0),  # Scale to 0-1
                    'source': 'ml_context',
                    'method': 'tfidf_cosine_similarity'
                }
                
        except ImportError:
            return self.get_basic_context_answer(user_input)
        except Exception as e:
            print(f"ML matching error: {e}")
            return self.get_basic_context_answer(user_input)
            
        return None
        
    def get_basic_context_answer(self, user_input):
        """Fallback basic context matching"""
        if not self.qa_pairs:
            return None
            
        user_input_lower = user_input.lower()
        
        # Simple keyword matching for context-based answers
        best_match = None
        best_score = 0
        
        for qa in self.qa_pairs:
            question_lower = qa["question"].lower()
            answer_lower = qa["answer"].lower()
            
            # Check for keyword overlap
            user_words = set(re.findall(r'\w+', user_input_lower))
            question_words = set(re.findall(r'\w+', question_lower))
            answer_words = set(re.findall(r'\w+', answer_lower))
            
            # Calculate relevance score
            question_overlap = len(user_words.intersection(question_words))
            answer_overlap = len(user_words.intersection(answer_words))
            total_score = question_overlap * 2 + answer_overlap  # Weight question matches more
            
            if total_score > best_score and total_score > 1:
                best_score = total_score
                best_match = qa
                
        if best_match:
            confidence = min(best_score / 10.0, 1.0)  # Normalize to 0-1
            return {
                'answer': best_match['answer'],
                'confidence': confidence,
                'source': 'basic_context',
                'method': 'keyword_matching'
            }
        
        return None
    
    def initialize_model(self):
        """Initialize the pretrained conversational model in background"""
        try:
            print("Loading AI model in background...")
            self.model_type = "Loading DialoGPT..."
            
            # Try to import and load transformers
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            import torch
            
            # Use Microsoft DialoGPT for conversational AI (free and lightweight)
            model_name = "microsoft/DialoGPT-medium"
            
            print(f"Downloading/Loading {model_name}...")
            
            # Initialize tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print(f"Model loaded successfully: {model_name}")
            
            # Initialize conversation history
            self.chat_history_ids = None
            self.model_type = "DialoGPT"
            self.model_loading = False
            
        except ImportError:
            print("WARNING: Transformers not available. Using context-only mode.")
            self.model = None
            self.tokenizer = None
            self.model_type = "Context-Only"
            self.model_loading = False
            
        except Exception as e:
            print(f"WARNING: Error loading DialoGPT model: {e}")
            print("Falling back to context-only mode...")
            self.model = None
            self.tokenizer = None
            self.model_type = "Context-Only (Fallback)"
            self.model_loading = False
            
    def record_conversation(self, user_input, response, confidence, source):
        """Record conversation for reinforcement learning"""
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'confidence': confidence,
            'source': source
        }
        self.conversation_history.append(conversation)
        
        # Save periodically (every 10 conversations)
        if len(self.conversation_history) % 10 == 0:
            self.save_conversation_history()
            
    def apply_user_feedback(self, user_input, response, feedback_score):
        """Apply user feedback for reinforcement learning"""
        pattern_key = f"{user_input.lower()[:50]}||{response[:50]}"
        
        # Update feedback score using exponential moving average
        current_score = self.feedback_scores.get(pattern_key, 1.0)
        new_score = current_score * (1 - self.learning_rate) + feedback_score * self.learning_rate
        
        self.feedback_scores[pattern_key] = new_score
        
        # Save feedback scores
        self.save_feedback_scores()
        
        print(f"Applied feedback: {feedback_score} -> Pattern score: {new_score:.3f}")
        
    def learn_from_patterns(self):
        """Analyze conversation patterns for adaptive learning"""
        if len(self.conversation_history) < 10:
            return
            
        try:
            # Analyze successful conversation patterns
            successful_conversations = [
                conv for conv in self.conversation_history[-100:] 
                if conv.get('confidence', 0) > 0.7
            ]
            
            # Extract common patterns from successful conversations
            if successful_conversations:
                print(f"Learning from {len(successful_conversations)} successful conversations")
                
                # Update Q&A pairs based on successful patterns
                self.update_qa_from_patterns(successful_conversations)
                
        except Exception as e:
            print(f"Error in pattern learning: {e}")
            
    def update_qa_from_patterns(self, successful_conversations):
        """Update Q&A pairs based on successful conversation patterns"""
        try:
            # Group similar questions and responses
            pattern_groups = {}
            
            for conv in successful_conversations:
                user_input = conv['user_input'].lower()
                response = conv['response']
                
                # Create a simplified pattern key
                key_words = [word for word in re.findall(r'\w+', user_input) if len(word) > 3]
                pattern_key = ' '.join(sorted(key_words[:5]))  # Top 5 keywords
                
                if pattern_key not in pattern_groups:
                    pattern_groups[pattern_key] = []
                pattern_groups[pattern_key].append((user_input, response))
            
            # Add new Q&A pairs from patterns with multiple successful instances
            new_qa_count = 0
            for pattern_key, conversations in pattern_groups.items():
                if len(conversations) >= 3:  # At least 3 successful instances
                    # Use the most common response
                    responses = [conv[1] for conv in conversations]
                    most_common_response = max(set(responses), key=responses.count)
                    
                    # Create a representative question
                    representative_question = conversations[0][0]  # Use first question as template
                    
                    # Check if this pattern doesn't already exist
                    existing = any(
                        qa['question'].lower() == representative_question.lower() 
                        for qa in self.qa_pairs
                    )
                    
                    if not existing:
                        self.qa_pairs.append({
                            'question': representative_question,
                            'answer': most_common_response
                        })
                        new_qa_count += 1
            
            if new_qa_count > 0:
                print(f"Learned {new_qa_count} new Q&A patterns")
                # Recreate vectors with new Q&A pairs
                self.create_qa_vectors()
                
        except Exception as e:
            print(f"Error updating Q&A from patterns: {e}")
    
    def get_context_answer(self, user_input):
        """NLP-Enhanced answer finding with semantic understanding and dynamic generation"""
        
        # Primary: Advanced NLP with semantic understanding
        nlp_answer = self.get_nlp_enhanced_answer(user_input)
        if nlp_answer and isinstance(nlp_answer, dict):
            return nlp_answer.get('answer', nlp_answer)
        elif nlp_answer:
            return nlp_answer
            
        # Secondary: ML-based approach if NLP fails  
        ml_answer = self.get_ml_context_answer(user_input)
        if ml_answer and isinstance(ml_answer, dict):
            return ml_answer.get('answer', ml_answer)
        elif ml_answer:
            return ml_answer
            
        # Final fallback: Basic keyword matching
        return self.get_basic_context_answer(user_input)
    
    def get_basic_context_answer(self, user_input):
        """Basic keyword matching fallback method"""
        if not self.qa_pairs:
            return None
            
        user_input_lower = user_input.lower()
        
        # Simple keyword matching for context-based answers
        best_match = None
        best_score = 0
        
        for qa in self.qa_pairs:
            question_lower = qa["question"].lower()
            answer_lower = qa["answer"].lower()
            
            # Check for keyword overlap
            user_words = set(re.findall(r'\w+', user_input_lower))
            question_words = set(re.findall(r'\w+', question_lower))
            answer_words = set(re.findall(r'\w+', answer_lower))
            
            # Calculate relevance score
            question_overlap = len(user_words.intersection(question_words))
            answer_overlap = len(user_words.intersection(answer_words))
            total_score = question_overlap * 2 + answer_overlap  # Weight question matches more
            
            if total_score > best_score and total_score >= 2:  # At least 2 points
                best_score = total_score
                best_match = qa["answer"]
        
        return best_match
    
    def generate_response_with_dialogpt(self, user_input):
        """Generate response using DialoGPT"""
        if not self.model or not self.tokenizer:
            return None
            
        try:
            import torch
            
            # Encode the user input
            new_user_input_ids = self.tokenizer.encode(
                user_input + self.tokenizer.eos_token, 
                return_tensors='pt'
            )
            
            # Append to chat history
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            else:
                bot_input_ids = new_user_input_ids
            
            # Limit context length to prevent memory issues
            if bot_input_ids.shape[-1] > 1000:
                bot_input_ids = bot_input_ids[:, -1000:]
            
            # Generate response
            with torch.no_grad():
                self.chat_history_ids = self.model.generate(
                    bot_input_ids,
                    max_length=bot_input_ids.shape[-1] + 100,
                    num_beams=3,
                    early_stopping=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7
                )
            
            # Decode the response
            response = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
                skip_special_tokens=True
            )
            
            return response.strip() if response.strip() else None
            
        except Exception as e:
            print(f"Error generating DialoGPT response: {e}")
            return None
    
    def get_response(self, user_input):
        """Get response for user input using available methods"""
        try:
            # First, try to get answer from context data
            context_answer = self.get_context_answer(user_input)
            if context_answer:
                return {
                    "response": context_answer,
                    "confidence": 0.9,
                    "source": "context_data"
                }
            
            # Try to generate response using DialoGPT if available
            if self.model and self.tokenizer:
                ai_response = self.generate_response_with_dialogpt(user_input)
                if ai_response and len(ai_response.strip()) > 0:
                    # Add marketplace context to responses
                    if len(ai_response) < 20 or any(word in ai_response.lower() for word in ["i don't", "not sure", "unclear"]):
                        ai_response = f"As a Jiji marketplace assistant, {ai_response}. I can help you with questions about buying, selling, payments, delivery, and marketplace policies."
                    
                    return {
                        "response": ai_response,
                        "confidence": 0.7,
                        "source": "dialogpt_model"
                    }
            
            # Generate smart fallback based on keywords
            smart_response = self.generate_smart_fallback(user_input)
            return {
                "response": smart_response,
                "confidence": 0.5,
                "source": "smart_fallback"
            }
            
        except Exception as e:
            print(f"Error in get_response: {e}")
            return {
                "response": "I apologize, but I'm experiencing some technical difficulties. Please try rephrasing your question or ask about our marketplace services.",
                "confidence": 0.1,
                "source": "error"
            }
    
    def generate_smart_fallback(self, user_input):
        """Generate contextual fallback responses based on keywords"""
        user_input_lower = user_input.lower()
        
        # Payment related keywords
        if any(word in user_input_lower for word in ["payment", "pay", "money", "mpesa", "card", "bank"]):
            return "We accept various payment methods including M-Pesa, credit/debit cards, bank transfers, and cash on delivery. For specific payment options, please check our payment page."
        
        # Delivery related keywords
        elif any(word in user_input_lower for word in ["delivery", "shipping", "deliver", "ship", "track", "order"]):
            return "Delivery typically takes 1-3 business days within Nairobi and 3-7 days for other locations. You can track your order using the tracking number sent via SMS."
        
        # Return/refund related keywords
        elif any(word in user_input_lower for word in ["return", "refund", "exchange", "replace", "back"]):
            return "We offer a 7-day return policy for most items. Items must be in original condition. Returns are processed within 5-7 business days."
        
        # Seller related keywords
        elif any(word in user_input_lower for word in ["seller", "vendor", "shop", "store", "business"]):
            return "All our sellers are verified through our comprehensive verification process. You can view seller ratings and reviews before making a purchase."
        
        # Price related keywords
        elif any(word in user_input_lower for word in ["price", "cost", "cheap", "expensive", "discount", "offer"]):
            return "Prices on Jiji are competitive and set by individual sellers. You can negotiate prices directly with sellers and look for special offers and discounts."
        
        # General greeting
        elif any(word in user_input_lower for word in ["hello", "hi", "hey", "good", "morning", "afternoon", "evening"]):
            return "Hello! Welcome to Jiji, East Africa's largest marketplace. I'm here to help you with questions about buying, selling, payments, delivery, and more. How can I assist you today?"
        
        # Question about what is Jiji
        elif any(word in user_input_lower for word in ["what", "jiji", "about", "platform", "marketplace"]):
            return "Jiji is East Africa's largest online marketplace where you can buy and sell almost anything - from cars and phones to houses and jobs. We connect millions of buyers and sellers across Kenya, Uganda, Tanzania, and Ghana."
        
        # Default fallback
        else:
            return "I'm here to help you with the Jiji marketplace! I can assist with questions about buying, selling, payments, delivery, returns, seller information, and more. What specific information do you need?"

# Initialize chatbot - make CSV path optional since we're using pretrained model
csv_path = "data/hospital_comprehensive_data.csv"
if not os.path.exists(csv_path):
    print(f"Warning: CSV file not found at {csv_path}. Using pretrained model only.")
    csv_path = None

chatbot = NLPEnhancedChatbot(csv_path)

# Root route for basic info
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Jiji Chatbot Backend is running!",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)", 
            "stats": "/stats (GET)"
        },
        "qa_pairs_loaded": len(chatbot.qa_pairs)
    })

# API endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        response_data = chatbot.get_response(user_message)
        
        return jsonify({
            "response": response_data["response"],
            "confidence": response_data["confidence"],
            "source": response_data["source"],
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint with model loading status"""
    if chatbot.model_loading:
        model_status = f"Loading... ({chatbot.model_type})"
    elif hasattr(chatbot, 'model') and chatbot.model is not None:
        model_status = chatbot.model_type
    else:
        model_status = chatbot.model_type
    
    return jsonify({
        "status": "healthy",
        "qa_pairs_loaded": len(chatbot.qa_pairs),
        "model_type": model_status,
        "model_loading": chatbot.model_loading,
        "context_available": len(chatbot.context_data) > 0
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    model_info = "unknown"
    if hasattr(chatbot, 'model') and chatbot.model is not None:
        model_info = "microsoft/DialoGPT-medium"
    elif hasattr(chatbot, 'use_fallback') and chatbot.use_fallback:
        model_info = "gpt2 (fallback)"
    
    return jsonify({
        "total_qa_pairs": len(chatbot.qa_pairs),
        "context_length": len(chatbot.context_data),
        "model_type": model_info,
        "using_pretrained_model": True
    })

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for reinforcement learning"""
    try:
        data = request.get_json()
        user_input = data.get('user_input')
        response = data.get('response')
        feedback_score = data.get('feedback_score', 0)
        
        if not user_input or not response:
            return jsonify({"error": "Missing user_input or response"}), 400
            
        if not isinstance(feedback_score, (int, float)) or not -1 <= feedback_score <= 1:
            return jsonify({"error": "feedback_score must be between -1 and 1"}), 400
            
        # Apply user feedback for reinforcement learning
        chatbot.apply_user_feedback(user_input, response, feedback_score)
        
        return jsonify({
            "status": "success",
            "message": "Feedback recorded successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/learning_stats', methods=['GET'])
def get_learning_stats():
    """Get machine learning and reinforcement learning statistics"""
    try:
        # Get conversation history length
        history_length = len(chatbot.conversation_history)
        
        # Get feedback scores statistics
        feedback_scores = [conv.get('feedback_score', 0) for conv in chatbot.conversation_history if 'feedback_score' in conv]
        avg_feedback = sum(feedback_scores) / len(feedback_scores) if feedback_scores else 0
        
        # Get learned patterns count
        learned_patterns = len([conv for conv in chatbot.conversation_history if conv.get('feedback_score', 0) > 0.5])
        
        return jsonify({
            "total_conversations": history_length,
            "average_feedback_score": round(avg_feedback, 3),
            "learned_patterns": learned_patterns,
            "ml_enabled": hasattr(chatbot, 'vectorizer') and chatbot.vectorizer is not None,
            "rl_enabled": True,
            "qa_pairs_learned": len(chatbot.qa_pairs) - chatbot.original_qa_count if hasattr(chatbot, 'original_qa_count') else 0
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/trigger_learning', methods=['POST'])
def trigger_learning():
    """Manually trigger pattern learning from conversation history"""
    try:
        patterns_learned = chatbot.learn_from_patterns()
        return jsonify({
            "status": "success",
            "patterns_learned": patterns_learned,
            "message": f"Learning completed. {patterns_learned} new patterns identified."
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Jiji Chatbot Backend Server...")
    print(f"Loaded {len(chatbot.qa_pairs)} Q&A pairs as context")
    print("AI model loading in background...")
    print("Flask server starting immediately...")
    
    # Flask server starts immediately while model loads in background
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
