"""
OpenAI utilities for generating dynamic conversation questions.
"""

import openai
import streamlit as st
from questions import get_topic_prompt

def initialize_openai():
    """Initialize OpenAI client with API key from Streamlit secrets."""
    try:
        # Try to get API key from Streamlit secrets first
        api_key = st.secrets.get("openai", {}).get("api_key")
        if not api_key:
            st.error("OpenAI API key not found in Streamlit secrets. Please add it to .streamlit/secrets.toml")
            st.stop()
        
        client = openai.OpenAI(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Error initializing OpenAI: {str(e)}")
        st.stop()

def generate_question(topic_key, question_number, previous_responses=None, user_profile=None):
    """
    Generate a dynamic question using OpenAI based on the topic and previous responses.
    
    Args:
        topic_key: The key of the selected topic
        question_number: Current question number (1-5)
        previous_responses: List of previous user responses
        user_profile: User profile information for personalization
    
    Returns:
        Generated question as a string
    """
    try:
        client = initialize_openai()
        
        # Get the base prompt for this topic
        base_prompt = get_topic_prompt(topic_key)
        
        # Build the conversation context
        messages = [
            {
                "role": "system",
                "content": base_prompt
            }
        ]
        
        # Add user profile context if available
        if user_profile:
            profile_context = f"""
            User Profile:
            - Name: {user_profile.get('name', 'User')}
            - Age: {user_profile.get('age', 'Unknown')}
            - Relationship Status: {user_profile.get('relationship_status', 'Unknown')}
            
            Please personalize the questions based on this information when appropriate. Address the user by name when appropriate, and thank them for sharing when appropriate.
            """
            messages.append({
                "role": "system",
                "content": profile_context
            })
        
        # Add previous responses for context
        if previous_responses:
            for i, response in enumerate(previous_responses):
                messages.extend([
                    {
                        "role": "assistant",
                        "content": f"Question {i+1}: [Previous question was asked here]"
                    },
                    {
                        "role": "user",
                        "content": response
                    }
                ])
        
        # Request the next question
        if question_number == 1:
            request_message = "Please ask the first question to start this reflection exercise."
        else:
            request_message = f"Based on the user's previous responses, please ask question {question_number} that builds naturally on what they've shared so far."
        
        messages.append({
            "role": "user",
            "content": request_message
        })
        
        # Generate the question
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            max_completion_tokens=300,
            reasoning_effort="minimal"
        )

        print(response)
        
        question = response.choices[0].message.content.strip()
        
        # Clean up the question (remove any "Question X:" prefixes)
        if question.startswith(f"Question {question_number}:"):
            question = question[len(f"Question {question_number}:"):].strip()
        
        return question
        
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        # Fallback to a generic question
        return f"Tell me more about your thoughts on this topic. What comes to mind?"

def generate_insight(topic_key, responses, user_profile=None):
    """
    Generate personalized insights using OpenAI based on all responses.
    
    Args:
        topic_key: The key of the selected topic
        responses: List of all user responses
        user_profile: User profile information
    
    Returns:
        Generated insight as a string
    """
    try:
        client = initialize_openai()
        
        # Get the base prompt for context
        base_prompt = get_topic_prompt(topic_key)
        
        # Build the insight request
        messages = [
            {
                "role": "system",
                "content": f"""
                {base_prompt}
                
                Based on the user's responses, generate 2-3 key insights that:
                1. Reveal patterns or themes in their responses
                2. Offer gentle, supportive observations about their relationship dynamics
                3. Highlight strengths and areas for growth
                4. Are specific to what they shared, not generic advice
                5. Are warm, empathetic, and non-judgmental
                6. Help them see their situation with fresh perspective
                
                Format as 2-3 bullet points starting with "•"
                """
            }
        ]
        
        # Add user profile if available
        if user_profile:
            messages.append({
                "role": "system",
                "content": f"User is {user_profile.get('age', 'unknown')} years old and {user_profile.get('relationship_status', 'unknown')} relationship status."
            })
        
        # Add all responses
        responses_text = "\n\n".join([f"Response {i+1}: {response}" for i, response in enumerate(responses)])
        messages.append({
            "role": "user",
            "content": f"Here are my responses to the reflection questions:\n\n{responses_text}\n\nPlease provide key insights about my relationship patterns and dynamics."
        })
        
        # Generate the insights
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            max_completion_tokens=1000,
            reasoning_effort="low"
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        st.error(f"Error generating insights: {str(e)}")
        # Fallback to a simple insight
        return "• Your responses show thoughtful self-reflection about your relationship\n• You demonstrate awareness of both challenges and strengths in your dynamic\n• There are opportunities for deeper connection and understanding"

def generate_summary(topic_key, responses, user_profile=None):
    """
    Generate a personalized summary using OpenAI based on all responses.
    
    Args:
        topic_key: The key of the selected topic
        responses: List of all user responses
        user_profile: User profile information
    
    Returns:
        Generated summary as a string
    """
    try:
        client = initialize_openai()
        
        # Get the base prompt for context
        base_prompt = get_topic_prompt(topic_key)
        
        # Build the summary request
        messages = [
            {
                "role": "system",
                "content": f"""
                {base_prompt}
                
                Based on the user's responses, create a thoughtful summary that:
                1. Identifies key themes and patterns
                2. Offers gentle insights without being prescriptive
                3. Highlights what might really be at stake
                4. Is supportive and non-judgmental
                5. Is 2-3 paragraphs long
                """
            }
        ]
        
        # Add user profile if available
        if user_profile:
            messages.append({
                "role": "system",
                "content": f"User is {user_profile.get('age', 'unknown')} years old and {user_profile.get('relationship_status', 'unknown')} relationship status."
            })
        
        # Add all responses
        responses_text = "\n\n".join([f"Response {i+1}: {response}" for i, response in enumerate(responses)])
        messages.append({
            "role": "user",
            "content": f"Here are my responses to the reflection questions:\n\n{responses_text}\n\nPlease provide a thoughtful summary of my reflections."
        })
        
        # Generate the summary
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            max_completion_tokens=1000,
            reasoning_effort="low"
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        # Fallback to a simple summary
        return f"You've shared thoughtful reflections on this topic. Your responses show depth and self-awareness in your relationship journey."
