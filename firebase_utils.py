"""
Firebase Firestore utilities for the Relationship Reflection App.
"""

import uuid
from datetime import datetime
from config import get_db
import streamlit as st

def save_user_profile(name, age, gender, relationship_status):
    """Save user profile to Firestore and return user_id."""
    try:
        db = get_db()
        user_id = str(uuid.uuid4())
        
        user_data = {
            'user_id': user_id,
            'name': name,
            'age': age,
            'gender': gender,
            'relationship_status': relationship_status,
            'created_at': datetime.now()
        }
        
        db.collection('streamlitUsers').document(user_id).set(user_data)
        return user_id
    except Exception as e:
        st.error(f"Error saving user profile: {str(e)}")
        return None

def save_responses(user_id, topic, questions, responses):
    """Save user questions and responses to Firestore."""
    try:
        db = get_db()
        response_id = str(uuid.uuid4())
        
        # Create question-response pairs for better structure
        qa_pairs = []
        for i, (question, response) in enumerate(zip(questions, responses)):
            qa_pairs.append({
                'question_number': i + 1,
                'question': question,
                'response': response
            })
        
        response_data = {
            'response_id': response_id,
            'user_id': user_id,
            'topic': topic,
            'qa_pairs': qa_pairs,
            'questions': questions,  # Keep for backward compatibility
            'responses': responses,  # Keep for backward compatibility
            'completed_at': datetime.now()
        }
        
        db.collection('streamlitResponses').document(response_id).set(response_data)
        return response_id
    except Exception as e:
        st.error(f"Error saving responses: {str(e)}")
        return None

def save_rating(user_id, topic, ratings, feedback=None):
    """Save user ratings and feedback to Firestore."""
    try:
        db = get_db()
        rating_id = str(uuid.uuid4())
        
        rating_data = {
            'rating_id': rating_id,
            'user_id': user_id,
            'topic': topic,
            'ratings': ratings,  # Dictionary with informative, engaging, repeat scores
            'informative_rating': ratings.get('informative', 3),
            'engaging_rating': ratings.get('engaging', 3), 
            'repeat_rating': ratings.get('repeat', 3),
            'overall_rating': round((ratings.get('informative', 3) + ratings.get('engaging', 3) + ratings.get('repeat', 3)) / 3, 1),  # Average for backward compatibility
            'feedback': feedback,
            'created_at': datetime.now()
        }
        
        db.collection('streamlitRatings').document(rating_id).set(rating_data)
        return rating_id
    except Exception as e:
        st.error(f"Error saving rating: {str(e)}")
        return None

def get_user_responses(user_id):
    """Get all responses for a specific user."""
    try:
        db = get_db()
        responses = db.collection('streamlitResponses').where('user_id', '==', user_id).get()
        return [doc.to_dict() for doc in responses]
    except Exception as e:
        st.error(f"Error retrieving user responses: {str(e)}")
        return []

def get_topic_stats(topic):
    """Get basic statistics for a topic (number of completions, average rating)."""
    try:
        db = get_db()
        
        # Count responses for this topic
        responses = db.collection('streamlitResponses').where('topic', '==', topic).get()
        response_count = len(responses)
        
        # Get average rating for this topic (use overall_rating for backward compatibility)
        ratings = db.collection('ratings').where('topic', '==', topic).get()
        rating_values = []
        for doc in ratings:
            data = doc.to_dict()
            # Try new overall_rating field first, fall back to old rating field
            rating = data.get('overall_rating', data.get('rating', 0))
            if rating > 0:
                rating_values.append(rating)
        
        avg_rating = sum(rating_values) / len(rating_values) if rating_values else 0
        
        return {
            'response_count': response_count,
            'avg_rating': round(avg_rating, 1),
            'rating_count': len(rating_values)
        }
    except Exception as e:
        st.error(f"Error getting topic stats: {str(e)}")
        return {'response_count': 0, 'avg_rating': 0, 'rating_count': 0}
