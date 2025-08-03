import csv
import random
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Initialize stopwords
stop_words = set(stopwords.words('english'))

class JijiChatbot:
    def __init__(self, csv_file_path):
        self.qa_pairs = []
        self.questions = []
        self.answers = []
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.question_vectors = None
        self.load_qa_data(csv_file_path)
        self.train_model()
    
    def load_qa_data(self, file_path):
        """Load questions and answers from CSV file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    question = row["Question"].strip().strip('"')
                    answer = row["Answer"].strip().strip('"')
                    self.qa_pairs.append({"question": question, "answer": answer})
                    self.questions.append(question)
                    self.answers.append(answer)
            print(f"Loaded {len(self.qa_pairs)} Q&A pairs")
        except Exception as e:
            print(f"Error loading Q&A data: {e}")
    
    def preprocess_text(self, text):
        """Preprocess text for better matching"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def train_model(self):
        """Train the TF-IDF model on questions"""
        if self.questions and len(self.questions) > 0:
            try:
                preprocessed_questions = [self.preprocess_text(q) for q in self.questions]
                # Filter out empty strings
                preprocessed_questions = [q for q in preprocessed_questions if q.strip()]
                
                if preprocessed_questions:
                    self.question_vectors = self.vectorizer.fit_transform(preprocessed_questions)
                    print(f"Model trained successfully with {len(preprocessed_questions)} questions")
                else:
                    print("Warning: No valid questions found for training")
            except Exception as e:
                print(f"Error training model: {e}")
                self.question_vectors = None
        else:
            print("Warning: No questions available for training")
    
    def find_best_match(self, user_input, threshold=0.3):
        """Find the best matching question using cosine similarity"""
        if self.question_vectors is None or len(self.questions) == 0:
            return None
        
        # Preprocess user input
        processed_input = self.preprocess_text(user_input)
        
        try:
            # Transform user input to vector
            user_vector = self.vectorizer.transform([processed_input])
            
            # Calculate cosine similarities
            similarities = cosine_similarity(user_vector, self.question_vectors).flatten()
            
            # Find the best match
            best_match_index = np.argmax(similarities)
            best_similarity = similarities[best_match_index]
            
            if best_similarity > threshold:
                return {
                    "question": self.questions[best_match_index],
                    "answer": self.answers[best_match_index],
                    "confidence": float(best_similarity)
                }
        
        except Exception as e:
            print(f"Error in find_best_match: {e}")
            return None
        
        return None
    
    def get_response(self, user_input):
        """Get response for user input"""
        # First try to find exact or close matches
        best_match = self.find_best_match(user_input)
        
        if best_match:
            return {
                "response": best_match["answer"],
                "confidence": best_match["confidence"],
                "matched_question": best_match["question"]
            }
        
        # If no good match, provide a helpful default response
        return {
            "response": "I'm sorry, I don't have a specific answer for that question. Could you please rephrase or ask about pricing, delivery, payment options, returns, or seller information?",
            "confidence": 0.0,
            "matched_question": None
        }

# Initialize chatbot
chatbot = JijiChatbot("common_questions.csv")

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
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "qa_pairs_loaded": len(chatbot.qa_pairs)
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "total_questions": len(chatbot.questions),
        "total_answers": len(chatbot.answers),
        "model_trained": chatbot.question_vectors is not None
    })

if __name__ == "__main__":
    print("Starting Jiji Chatbot Backend...")
    print(f"Loaded {len(chatbot.qa_pairs)} question-answer pairs")
    app.run(debug=True, host='0.0.0.0', port=5000)
