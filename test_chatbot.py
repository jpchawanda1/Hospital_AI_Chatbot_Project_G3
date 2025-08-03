import requests
import json
import time
from chatbot_backend import JijiChatbot

def test_chatbot_locally():
    """Test the chatbot using the local class"""
    print("Testing Chatbot Locally...")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = JijiChatbot("common_questions.csv")
    
    # Test questions
    test_questions = [
        "What is the price of this item?",
        "How can I pay?",
        "Can I return my purchase?",
        "How long is delivery?",
        "Is the seller trustworthy?",
        "Do you accept M-Pesa?",
        "Can I negotiate the price?",
        "What if item is damaged?",
        "How do I track my order?",
        "Can I cancel my order?",
        "Random question that shouldn't match anything specific"
    ]
    
    for question in test_questions:
        response = chatbot.get_response(question)
        print(f"Q: {question}")
        print(f"A: {response['response']}")
        print(f"Confidence: {response['confidence']:.3f}")
        print("-" * 30)

def test_chatbot_api():
    """Test the chatbot via API"""
    print("\nTesting Chatbot API...")
    print("=" * 50)
    
    api_url = "http://localhost:5000/chat"
    
    test_questions = [
        "What payment methods do you accept?",
        "How long does shipping take?",
        "Can I return items?",
        "What if my item is damaged?",
        "How do I contact customer service?"
    ]
    
    for question in test_questions:
        try:
            response = requests.post(api_url, 
                                   json={"message": question},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"Q: {question}")
                print(f"A: {data['response']}")
                print(f"Confidence: {data.get('confidence', 'N/A')}")
            else:
                print(f"Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to API. Make sure the backend is running.")
            break
        except Exception as e:
            print(f"Error: {e}")
            
        print("-" * 30)
        time.sleep(1)  # Small delay between requests

def performance_metrics():
    """Calculate performance metrics"""
    print("\nPerformance Metrics...")
    print("=" * 50)
    
    chatbot = JijiChatbot("common_questions.csv")
    
    # Test with a sample of questions from the dataset
    total_questions = len(chatbot.questions)
    sample_size = min(100, total_questions)  # Test with up to 100 questions
    
    high_confidence = 0
    medium_confidence = 0
    low_confidence = 0
    
    for i in range(0, sample_size, 10):  # Test every 10th question
        question = chatbot.questions[i]
        response = chatbot.get_response(question)
        confidence = response['confidence']
        
        if confidence > 0.8:
            high_confidence += 1
        elif confidence > 0.5:
            medium_confidence += 1
        else:
            low_confidence += 1
    
    tested = sample_size // 10
    print(f"Total questions in dataset: {total_questions}")
    print(f"Questions tested: {tested}")
    print(f"High confidence responses (>0.8): {high_confidence} ({high_confidence/tested*100:.1f}%)")
    print(f"Medium confidence responses (0.5-0.8): {medium_confidence} ({medium_confidence/tested*100:.1f}%)")
    print(f"Low confidence responses (<0.5): {low_confidence} ({low_confidence/tested*100:.1f}%)")

if __name__ == "__main__":
    # Test locally first
    test_chatbot_locally()
    
    # Test performance metrics
    performance_metrics()
    
    # Test API (only if backend is running)
    print("\nTo test the API, make sure to run 'python chatbot_backend.py' first")
    
    # Uncomment the following line to test API
    # test_chatbot_api()
