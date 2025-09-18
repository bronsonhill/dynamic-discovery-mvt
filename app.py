"""
Relationship Reflection App - Streamlit MVT
A guided reflection tool for exploring relationship dynamics.
"""

import streamlit as st
from questions import get_topic_list, get_topic_data, get_topic_prompt
from firebase_utils import save_user_profile, save_responses, save_rating, get_topic_stats
from openai_utils import generate_question, generate_summary, generate_insight

def initialize_session_state():
    """Initialize session state variables."""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'profile'
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question_text' not in st.session_state:
        st.session_state.current_question_text = ""
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
    if 'insights' not in st.session_state:
        st.session_state.insights = ""
    if 'show_cancel_confirm' not in st.session_state:
        st.session_state.show_cancel_confirm = False

def show_profile_form():
    """Display user profile input form."""
    st.title("🌟 Welcome to Bonded")
    st.markdown("---")
    
    st.markdown("""
    This app will guide you through a reflective exercise about your relationship dynamics. 
    You'll explore a topic through 5 thoughtful questions and receive a summary of your insights.
    
    **Let's start by getting to know you a bit:**
    """)
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", placeholder="Your first name")
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
        
        with col2:
            gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Other"])
            relationship_status = st.selectbox("Relationship Status", [
                "Single", "Dating", "Long-term (1 year+)", "Engaged", 
                "Married", "It's complicated"
            ])
        
        submitted = st.form_submit_button("Continue", type="primary")
        
        if submitted:
            if name.strip():
                user_id = save_user_profile(name, age, gender, relationship_status)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.user_profile = {
                        'name': name,
                        'age': age,
                        'gender': gender,
                        'relationship_status': relationship_status
                    }
                    st.session_state.stage = 'topic_selection'
                    st.rerun()
            else:
                st.error("Please enter your name to continue.")

def show_topic_selection():
    """Display topic selection interface."""
    name = st.session_state.user_profile.get('name', 'there')
    st.title(f"👋 Hi {name}!")
    st.markdown("---")
    
    st.markdown("### Choose a reflection topic:")
    st.markdown("Each topic contains 5 questions designed to help you explore different aspects of your relationship.")
    
    topics = get_topic_list()
    
    for topic_key, topic_title in topics:
        topic_data = get_topic_data(topic_key)
        stats = get_topic_stats(topic_key)
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{topic_title}**")
                st.markdown(f"*{topic_data['description']}*")
                
                if stats['response_count'] > 0:
                    st.caption(f"✨ {stats['response_count']} people have explored this topic")
                    if stats['rating_count'] > 0:
                        st.caption(f"⭐ Average rating: {stats['avg_rating']}/5")
            
            with col2:
                if st.button("Select", key=f"select_{topic_key}", type="primary"):
                    st.session_state.selected_topic = topic_key
                    st.session_state.stage = 'questions'
                    st.session_state.current_question = 0
                    st.session_state.responses = []
                    st.session_state.questions = []
                    st.session_state.current_question_text = ""
                    st.session_state.summary = ""
                    st.session_state.insights = ""
                    st.session_state.show_cancel_confirm = False
                    st.rerun()
            
            st.markdown("---")

def show_questions():
    """Display the question flow with AI-generated questions."""
    topic_data = get_topic_data(st.session_state.selected_topic)
    current_q = st.session_state.current_question
    total_questions = 5  # Each topic has 5 questions
    
    # Header with cancel button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(topic_data['title'])
    with col2:
        if st.button("❌ Cancel Discovery", help="Return to topic selection"):
            # Show confirmation if user has made progress
            if st.session_state.responses:
                # Store the cancel request
                st.session_state.show_cancel_confirm = True
                st.rerun()
            else:
                # No progress made, safe to cancel immediately
                st.session_state.stage = 'topic_selection'
                st.session_state.selected_topic = None
                st.session_state.current_question = 0
                st.session_state.responses = []
                st.session_state.questions = []
                st.session_state.current_question_text = ""
                st.session_state.summary = ""
                st.session_state.insights = ""
                st.rerun()
    
    # Show cancel confirmation dialog if needed
    if st.session_state.get('show_cancel_confirm', False):
        with st.container():
            st.warning("⚠️ Are you sure you want to cancel this discovery?")
            st.markdown("You'll lose your current progress and responses.")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Yes, Cancel", type="secondary"):
                    # Reset everything and return to topic selection
                    st.session_state.stage = 'topic_selection'
                    st.session_state.selected_topic = None
                    st.session_state.current_question = 0
                    st.session_state.responses = []
                    st.session_state.questions = []
                    st.session_state.current_question_text = ""
                    st.session_state.summary = ""
                    st.session_state.insights = ""
                    st.session_state.show_cancel_confirm = False
                    st.rerun()
            
            with col2:
                if st.button("Keep Going", type="primary"):
                    # Continue with the discovery
                    st.session_state.show_cancel_confirm = False
                    st.rerun()
            
            st.markdown("---")
        return  # Don't show the rest of the interface while confirming
    
    st.markdown("---")
    
    # Progress indicator
    progress = (current_q + 1) / total_questions
    st.progress(progress)
    st.caption(f"Question {current_q + 1} of {total_questions}")
    
    # Display the topic description for context (only show on first question)
    if current_q == 0:
        st.info(f"💡 **About this topic:** {topic_data['description']}")
        st.markdown("---")
    
    # Show all previous Q&A pairs vertically
    if st.session_state.responses:
        st.markdown("### Your Conversation")
        
        for i, response in enumerate(st.session_state.responses):
            # Show question if available
            if i < len(st.session_state.questions) and st.session_state.questions[i]:
                st.markdown(f"**Question {i+1}:**")
                st.markdown(f"*{st.session_state.questions[i]}*")
                st.markdown("")
                st.markdown(f"**Your Response:**")
                st.markdown(response)
            else:
                st.markdown(f"**Question {i+1}:**")
                st.markdown(f"**Your Response:**")
                st.markdown(response)
            
            st.markdown("---")
    
    # Generate current question if not already generated
    if not st.session_state.current_question_text:
        with st.spinner("Generating your personalized question..."):
            st.session_state.current_question_text = generate_question(
                topic_key=st.session_state.selected_topic,
                question_number=current_q + 1,
                previous_responses=st.session_state.responses,
                user_profile=st.session_state.user_profile
            )
            
            # Save the generated question to our questions list
            # Extend the list if needed to match current question index
            while len(st.session_state.questions) <= current_q:
                st.session_state.questions.append("")
            st.session_state.questions[current_q] = st.session_state.current_question_text
    
    # Current question (prominently displayed)
    st.markdown(f"### Question {current_q + 1}")
    st.markdown(f"**{st.session_state.current_question_text}**")
    
    # Response input
    response = st.text_area(
        "Your reflection:",
        height=150,
        placeholder="Take your time to reflect and share your thoughts...",
        key=f"response_{current_q}"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_q > 0:
            if st.button("← Previous"):
                st.session_state.current_question -= 1
                # Load the previously generated question if it exists
                prev_q = st.session_state.current_question
                if prev_q < len(st.session_state.questions) and st.session_state.questions[prev_q]:
                    st.session_state.current_question_text = st.session_state.questions[prev_q]
                else:
                    st.session_state.current_question_text = ""  # Clear for regeneration
                st.rerun()
    
    with col3:
        if response.strip():
            if current_q < total_questions - 1:
                if st.button("Next →", type="primary"):
                    # Save current response
                    if len(st.session_state.responses) <= current_q:
                        st.session_state.responses.append(response)
                    else:
                        st.session_state.responses[current_q] = response
                    
                    st.session_state.current_question += 1
                    st.session_state.current_question_text = ""  # Clear question for regeneration
                    st.rerun()
            else:
                if st.button("Complete Exercise", type="primary"):
                    # Save final response
                    if len(st.session_state.responses) <= current_q:
                        st.session_state.responses.append(response)
                    else:
                        st.session_state.responses[current_q] = response
                    
                    # Generate AI insights and summary
                    with st.spinner("Generating your personalized insights..."):
                        # Generate insights first
                        st.session_state.insights = generate_insight(
                            topic_key=st.session_state.selected_topic,
                            responses=st.session_state.responses,
                            user_profile=st.session_state.user_profile
                        )
                        
                        # Then generate summary
                        st.session_state.summary = generate_summary(
                            topic_key=st.session_state.selected_topic,
                            responses=st.session_state.responses,
                            user_profile=st.session_state.user_profile
                        )
                    st.session_state.stage = 'summary'
                    st.rerun()


def show_summary():
    """Display the summary and rating interface."""
    topic_data = get_topic_data(st.session_state.selected_topic)
    
    st.title("✨ Your Reflection Summary")
    st.markdown("---")
    
    # Display insights prominently
    if st.session_state.insights:
        st.markdown("### 💡 Key Insights")
        # Use info box to make insights stand out
        st.info(st.session_state.insights)
    
    # Display detailed summary
    if st.session_state.summary:
        st.markdown("### 📝 Detailed Summary")
        st.markdown(st.session_state.summary)
    
    st.markdown("---")
    
    # Display all questions and responses
    st.markdown("### Your Complete Conversation")
    
    for i, (question, response) in enumerate(zip(st.session_state.questions, st.session_state.responses)):
        with st.expander(f"Q{i+1}: {question[:60]}..."):
            st.markdown(f"**Question {i+1}:**")
            st.markdown(f"*{question}*")
            st.markdown("")
            st.markdown(f"**Your Response:**")
            st.markdown(response)
    
    st.markdown("---")
    
    # Rating and feedback
    st.markdown("### How was this exercise?")
    st.markdown("*Honestly* rate your experience on the following dimensions:")
    
    # Define the scale options
    scale_options = [1, 2, 3, 4, 5]
    scale_labels = {
        1: "Strongly Disagree",
        2: "Disagree", 
        3: "Neutral",
        4: "Agree",
        5: "Strongly Agree"
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        informative_rating = st.selectbox(
            "This exercise was informative:",
            scale_options,
            index=2,  # Default to neutral
            format_func=lambda x: f"{x} - {scale_labels[x]}",
            key="informative"
        )
    
    with col2:
        engaging_rating = st.selectbox(
            "This exercise was engaging:",
            scale_options,
            index=2,  # Default to neutral
            format_func=lambda x: f"{x} - {scale_labels[x]}",
            key="engaging"
        )
    
    with col3:
        repeat_rating = st.selectbox(
            "I would do this again:",
            scale_options,
            index=2,  # Default to neutral
            format_func=lambda x: f"{x} - {scale_labels[x]}",
            key="repeat"
        )
    
    # Optional feedback
    feedback = st.text_area(
        "Optional feedback:",
        placeholder="What did you find most valuable? Any suggestions for improvement?",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Submit Rating", type="primary"):
            # Save responses and rating
            response_id = save_responses(
                st.session_state.user_id,
                st.session_state.selected_topic,
                st.session_state.questions,
                st.session_state.responses
            )
            
            rating_id = save_rating(
                st.session_state.user_id,
                st.session_state.selected_topic,
                {
                    'informative': informative_rating,
                    'engaging': engaging_rating,
                    'repeat': repeat_rating
                },
                feedback if feedback.strip() else None
            )
            
            if response_id and rating_id:
                st.success("Thank you for your feedback! Your responses have been saved.")
                st.balloons()
            
    with col2:
        if st.button("Try Another Topic"):
            # Reset for new topic
            st.session_state.stage = 'topic_selection'
            st.session_state.selected_topic = None
            st.session_state.current_question = 0
            st.session_state.responses = []
            st.session_state.questions = []
            st.session_state.current_question_text = ""
            st.session_state.summary = ""
            st.session_state.insights = ""
            st.session_state.show_cancel_confirm = False
            st.rerun()

def main():
    """Main app function."""
    st.set_page_config(
        page_title="Bonded - Relationship Discovery",
        page_icon="💕",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .stButton > button {
        width: 100%;
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    # Route to appropriate stage
    if st.session_state.stage == 'profile':
        show_profile_form()
    elif st.session_state.stage == 'topic_selection':
        show_topic_selection()
    elif st.session_state.stage == 'questions':
        show_questions()
    elif st.session_state.stage == 'summary':
        show_summary()

if __name__ == "__main__":
    main()
