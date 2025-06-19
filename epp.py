import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Course Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# Initialize database
def init_database():
    conn = sqlite3.connect('course_recommendation.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            school TEXT,
            strand TEXT,
            tvl_strand TEXT,
            science_interest INTEGER,
            arts_interest INTEGER,
            teaching_interest INTEGER,
            business_interest INTEGER,
            technology_interest INTEGER,
            design_interest INTEGER,
            sports_interest INTEGER,
            logical_ability INTEGER,
            creativity_ability INTEGER,
            communication_ability INTEGER,
            practical_ability INTEGER,
            teamwork_ability INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER,
            course_name TEXT,
            confidence_score REAL,
            explanation TEXT,
            FOREIGN KEY (assessment_id) REFERENCES assessments (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER,
            course_name TEXT,
            rating INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assessment_id) REFERENCES assessments (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Course data with descriptions
COURSES = {
    "Computer Science": {
        "description": "Study algorithms, programming, software development, and computational theory. Prepare for careers in software engineering, AI development, and tech innovation.",
        "image": "💻"
    },
    "Information Technology": {
        "description": "Focus on practical application of technology in business environments. Learn system administration, network management, and IT support.",
        "image": "🖥️"
    },
    "Data Science": {
        "description": "Combine statistics, programming, and domain expertise to extract insights from data. Work with big data, machine learning, and analytics.",
        "image": "📊"
    },
    "Engineering": {
        "description": "Apply mathematical and scientific principles to design and build solutions. Specializations include civil, electrical, mechanical, and more.",
        "image": "⚙️"
    },
    "Business Administration": {
        "description": "Learn management principles, finance, marketing, and operations. Prepare for leadership roles in various industries.",
        "image": "💼"
    },
    "Psychology": {
        "description": "Study human behavior, mental processes, and emotional well-being. Pursue careers in counseling, research, or organizational psychology.",
        "image": "🧠"
    },
    "Education": {
        "description": "Prepare to become an educator and shape future generations. Learn teaching methodologies, curriculum development, and educational psychology.",
        "image": "📚"
    },
    "Nursing": {
        "description": "Provide healthcare services and patient care. Learn medical procedures, patient assessment, and healthcare management.",
        "image": "🏥"
    },
    "Multimedia Arts": {
        "description": "Combine creativity with technology to create digital content. Learn graphic design, animation, video production, and digital marketing.",
        "image": "🎨"
    },
    "Hospitality Management": {
        "description": "Manage hotels, restaurants, and tourism businesses. Learn customer service, operations management, and hospitality industry practices.",
        "image": "🏨"
    }
}

# Simple recommendation algorithm
def get_recommendations(user_data):
    # Simple rule-based recommendation system
    recommendations = []
    
    # Extract user preferences
    interests = {
        'science': user_data['science_interest'],
        'arts': user_data['arts_interest'],
        'teaching': user_data['teaching_interest'],
        'business': user_data['business_interest'],
        'technology': user_data['technology_interest'],
        'design': user_data['design_interest'],
        'sports': user_data['sports_interest']
    }
    
    abilities = {
        'logical': user_data['logical_ability'],
        'creativity': user_data['creativity_ability'],
        'communication': user_data['communication_ability'],
        'practical': user_data['practical_ability'],
        'teamwork': user_data['teamwork_ability']
    }
    
    # Course matching logic
    course_scores = {}
    
    # Computer Science
    score = (interests['technology'] * 0.4 + interests['science'] * 0.3 + 
             abilities['logical'] * 0.3)
    course_scores['Computer Science'] = score
    
    # Information Technology
    score = (interests['technology'] * 0.5 + abilities['practical'] * 0.3 + 
             abilities['logical'] * 0.2)
    course_scores['Information Technology'] = score
    
    # Data Science
    score = (interests['science'] * 0.4 + interests['technology'] * 0.3 + 
             abilities['logical'] * 0.3)
    course_scores['Data Science'] = score
    
    # Engineering
    score = (interests['science'] * 0.4 + abilities['logical'] * 0.3 + 
             abilities['practical'] * 0.3)
    course_scores['Engineering'] = score
    
    # Business Administration
    score = (interests['business'] * 0.4 + abilities['communication'] * 0.3 + 
             abilities['teamwork'] * 0.3)
    course_scores['Business Administration'] = score
    
    # Psychology
    score = (interests['teaching'] * 0.3 + abilities['communication'] * 0.4 + 
             abilities['teamwork'] * 0.3)
    course_scores['Psychology'] = score
    
    # Education
    score = (interests['teaching'] * 0.5 + abilities['communication'] * 0.3 + 
             abilities['teamwork'] * 0.2)
    course_scores['Education'] = score
    
    # Nursing
    score = (interests['science'] * 0.3 + abilities['communication'] * 0.3 + 
             abilities['teamwork'] * 0.4)
    course_scores['Nursing'] = score
    
    # Multimedia Arts
    score = (interests['arts'] * 0.4 + interests['design'] * 0.4 + 
             abilities['creativity'] * 0.2)
    course_scores['Multimedia Arts'] = score
    
    # Hospitality Management
    score = (interests['business'] * 0.3 + abilities['communication'] * 0.4 + 
             abilities['teamwork'] * 0.3)
    course_scores['Hospitality Management'] = score
    
    # Sort courses by score and get top 3
    sorted_courses = sorted(course_scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_courses[:3]
    
    # Generate explanations
    for course, score in top_3:
        explanation = generate_explanation(course, interests, abilities)
        recommendations.append({
            'course': course,
            'score': score,
            'explanation': explanation
        })
    
    return recommendations

def generate_explanation(course, interests, abilities):
    explanations = {
        'Computer Science': f"Recommended because of your interest in technology ({interests['technology']}/5) and strong logical thinking abilities ({abilities['logical']}/5).",
        'Information Technology': f"Great fit due to your technology interest ({interests['technology']}/5) and practical skills ({abilities['practical']}/5).",
        'Data Science': f"Perfect match with your science interest ({interests['science']}/5) and logical abilities ({abilities['logical']}/5).",
        'Engineering': f"Suits your science interest ({interests['science']}/5) and practical problem-solving skills ({abilities['practical']}/5).",
        'Business Administration': f"Aligns with your business interest ({interests['business']}/5) and communication skills ({abilities['communication']}/5).",
        'Psychology': f"Matches your interest in helping others and strong communication abilities ({abilities['communication']}/5).",
        'Education': f"Perfect for your teaching interest ({interests['teaching']}/5) and communication skills ({abilities['communication']}/5).",
        'Nursing': f"Great choice given your interest in helping others and teamwork abilities ({abilities['teamwork']}/5).",
        'Multimedia Arts': f"Excellent match for your artistic interests ({interests['arts']}/5) and creativity ({abilities['creativity']}/5).",
        'Hospitality Management': f"Suits your business interest ({interests['business']}/5) and people skills ({abilities['communication']}/5)."
    }
    return explanations.get(course, "This course matches your profile based on your interests and abilities.")

# Database functions
def save_assessment(data):
    conn = sqlite3.connect('course_recommendation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO assessments (
            name, school, strand, tvl_strand, science_interest, arts_interest,
            teaching_interest, business_interest, technology_interest, design_interest,
            sports_interest, logical_ability, creativity_ability, communication_ability,
            practical_ability, teamwork_ability
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'], data['school'], data['strand'], data['tvl_strand'],
        data['science_interest'], data['arts_interest'], data['teaching_interest'],
        data['business_interest'], data['technology_interest'], data['design_interest'],
        data['sports_interest'], data['logical_ability'], data['creativity_ability'],
        data['communication_ability'], data['practical_ability'], data['teamwork_ability']
    ))
    
    assessment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return assessment_id

def save_recommendations(assessment_id, recommendations):
    conn = sqlite3.connect('course_recommendation.db')
    cursor = conn.cursor()
    
    for rec in recommendations:
        cursor.execute('''
            INSERT INTO recommendations (assessment_id, course_name, confidence_score, explanation)
            VALUES (?, ?, ?, ?)
        ''', (assessment_id, rec['course'], rec['score'], rec['explanation']))
    
    conn.commit()
    conn.close()

def save_feedback(assessment_id, course_name, rating):
    conn = sqlite3.connect('course_recommendation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO feedback (assessment_id, course_name, rating)
        VALUES (?, ?, ?)
    ''', (assessment_id, course_name, rating))
    
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = sqlite3.connect('course_recommendation.db')
    
    # Total courses available
    total_courses = len(COURSES)
    
    # Total assessments
    try:
        assessments_df = pd.read_sql_query("SELECT COUNT(*) as count FROM assessments", conn)
        total_assessments = assessments_df['count'].iloc[0]
    except:
        total_assessments = 0
    
    # Agreement rate (average rating)
    try:
        feedback_df = pd.read_sql_query("SELECT AVG(rating) as avg_rating FROM feedback", conn)
        avg_rating = feedback_df['avg_rating'].iloc[0]
        agreement_rate = (avg_rating / 5.0 * 100) if avg_rating else 0
    except:
        agreement_rate = 0
    
    # Most recommended courses
    try:
        popular_courses_df = pd.read_sql_query('''
            SELECT course_name, COUNT(*) as count 
            FROM recommendations 
            GROUP BY course_name 
            ORDER BY count DESC 
            LIMIT 3
        ''', conn)
        popular_courses = popular_courses_df.to_dict('records')
    except:
        popular_courses = []
    
    conn.close()
    
    return {
        'total_courses': total_courses,
        'total_assessments': total_assessments,
        'agreement_rate': agreement_rate,
        'popular_courses': popular_courses
    }

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'
if 'assessment_data' not in st.session_state:
    st.session_state.assessment_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'assessment_id' not in st.session_state:
    st.session_state.assessment_id = None

# Initialize database
init_database()

# Sidebar
st.sidebar.title("🎓 Course Recommendation System")

# Navigation buttons in sidebar
if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state.page = 'Dashboard'

if st.sidebar.button("📝 Assessment", use_container_width=True):
    st.session_state.page = 'Assessment'

# Add some spacing
st.sidebar.markdown("---")
st.sidebar.markdown("**About this System**")
st.sidebar.info("This AI-powered system helps Senior High School students choose suitable college courses based on their interests and abilities.")

# Dashboard Page
if st.session_state.page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Welcome to the Course Recommendation System Dashboard")
    
    # Get dashboard statistics
    stats = get_dashboard_stats()
    
    # Upper part - Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📚 Total Courses Available",
            value=stats['total_courses']
        )
    
    with col2:
        st.metric(
            label="✅ Assessments Completed",
            value=stats['total_assessments']
        )
    
    with col3:
        st.metric(
            label="👍 Agreement Rate",
            value=f"{stats['agreement_rate']:.1f}%"
        )
    
    st.divider()
    
    # Lower part - Most recommended courses
    st.subheader("🏆 Most Recommended Courses")
    
    if stats['popular_courses']:
        for i, course_data in enumerate(stats['popular_courses']):
            course_name = course_data['course_name']
            count = course_data['count']
            
            if course_name in COURSES:
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.markdown(f"<div style='font-size: 60px; text-align: center;'>{COURSES[course_name]['image']}</div>", 
                              unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"### {course_name}")
                    st.write(COURSES[course_name]['description'])
                    st.caption(f"Recommended {count} times")
                
                if i < len(stats['popular_courses']) - 1:
                    st.divider()
    else:
        st.info("No recommendations yet. Complete an assessment to see popular courses!")

# Assessment Page
elif st.session_state.page == "Assessment":
    st.title("📝 Course Assessment")
    st.write("Please answer the following questions to get personalized course recommendations.")
    
    with st.form("assessment_form"):
        # Personal Information
        st.subheader("📋 Personal Information")
        name = st.text_input("Name (Optional)")
        school = st.text_input("Current School/University")
        
        strand = st.selectbox(
            "Current SHS Strand",
            ["STEM", "ABM (Accountancy, Business, & Management)", 
             "HUMMS (Humanities & Social Sciences)", "GAS (General Academic Strand)", 
             "TVL (Technical-Vocational-Livelihood)"]
        )
        
        tvl_strand = st.selectbox(
            "TVL Strand (if applicable)",
            ["Not applicable", "ICT (Information and Communications Technology)",
             "HE (Home Economics)", "IA (Industrial Arts)", "AFA (Agri-Fishery Arts)"]
        )
        
        st.divider()
        
        # Interest Assessment
        st.subheader("🎯 Rate Your Interest (1=least interested, 5=most interested)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            science_interest = st.select_slider(
                "Science/Experiments", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Least' if x==1 else 'Most' if x==5 else 'Neutral' if x==3 else ''}"
            )
            
            arts_interest = st.select_slider(
                "Arts/Writing", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Least' if x==1 else 'Most' if x==5 else 'Neutral' if x==3 else ''}"
            )
            
            teaching_interest = st.select_slider(
                "Teaching/Tutoring", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Least' if x==1 else 'Most' if x==5 else 'Neutral' if x==3 else ''}"
            )
            
            business_interest = st.select_slider(
                "Business/Finance", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Least' if x==1 else 'Most' if x==5 else 'Neutral' if x==3 else ''}"
            )
        
        with col2:
            technology_interest = st.select_slider(
                "Technology/Coding", 
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: f"{x} - {'Least' if x==1 else 'Most' if x==5 else 'Neutral' if x==3 else ''}"
            )
            
            design_interest = st.select_slider(
                "Graphic Design/Digital Arts", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Least' if x==1 else 'Most' if x==5 else 'Neutral' if x==3 else ''}"
            )
            
            sports_interest = st.select_slider(
                "Physical Activity/Sports", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Least' if x==1 else 'Most' if x==5 else 'Neutral' if x==3 else ''}"
            )
        
        st.divider()
        
        # Ability Assessment
        st.subheader("💪 Rate Your Abilities (1=weak, 5=strong)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            logical_ability = st.select_slider(
                "Logical Thinking", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Weak' if x==1 else 'Strong' if x==5 else 'Average' if x==3 else ''}"
            )
            
            creativity_ability = st.select_slider(
                "Creativity", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Weak' if x==1 else 'Strong' if x==5 else 'Average' if x==3 else ''}"
            )
            
            communication_ability = st.select_slider(
                "Communication", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Weak' if x==1 else 'Strong' if x==5 else 'Average' if x==3 else ''}"
            )
        
        with col2:
            practical_ability = st.select_slider(
                "Practical Skills (hands-on tasks, using tools)", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Weak' if x==1 else 'Strong' if x==5 else 'Average' if x==3 else ''}"
            )
            
            teamwork_ability = st.select_slider(
                "Teamwork", 
                options=[1, 2, 3, 4, 5], 
                value=3,
                format_func=lambda x: f"{x} - {'Weak' if x==1 else 'Strong' if x==5 else 'Average' if x==3 else ''}"
            )
        
        st.divider()
        
        # Submit button
        submitted = st.form_submit_button("🎯 Get Recommendation", use_container_width=True, type="primary")
        
        if submitted:
            # Collect assessment data
            assessment_data = {
                'name': name if name else 'Anonymous',
                'school': school,
                'strand': strand,
                'tvl_strand': tvl_strand,
                'science_interest': science_interest,
                'arts_interest': arts_interest,
                'teaching_interest': teaching_interest,
                'business_interest': business_interest,
                'technology_interest': technology_interest,
                'design_interest': design_interest,
                'sports_interest': sports_interest,
                'logical_ability': logical_ability,
                'creativity_ability': creativity_ability,
                'communication_ability': communication_ability,
                'practical_ability': practical_ability,
                'teamwork_ability': teamwork_ability
            }
            
            # Save to database and get ID
            assessment_id = save_assessment(assessment_data)
            
            # Get recommendations
            recommendations = get_recommendations(assessment_data)
            
            # Save recommendations to database
            save_recommendations(assessment_id, recommendations)
            
            # Store in session state
            st.session_state.assessment_data = assessment_data
            st.session_state.recommendations = recommendations
            st.session_state.assessment_id = assessment_id
            st.session_state.page = 'Results'
            
            st.rerun()
    
    # Back to home button
    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.page = 'Dashboard'
        st.rerun()

# Results Page
elif st.session_state.page == "Results":
    if st.session_state.recommendations:
        st.title("🎯 Your Course Recommendations")
        st.write(f"Based on your assessment, here are the top 3 courses recommended for you:")
        
        for i, rec in enumerate(st.session_state.recommendations):
            course_name = rec['course']
            score = rec['score']
            explanation = rec['explanation']
            
            # Create a container for each recommendation
            with st.container():
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.markdown(f"<div style='font-size: 80px; text-align: center;'>{COURSES[course_name]['image']}</div>", 
                              unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"### {course_name}")
                    st.write(COURSES[course_name]['description'])
                    st.info(f"**Why this course?** {explanation}")
                    
                    # Confidence score
                    confidence_percent = min(95, max(60, score * 20))  # Scale to percentage
                    st.progress(confidence_percent / 100)
                    st.caption(f"Match confidence: {confidence_percent:.0f}%")
                
                # Feedback section
                st.write("**Did you like this recommendation?**")
                
                # Create unique key for each course rating
                rating_key = f"rating_{course_name}_{st.session_state.assessment_id}"
                
                col1, col2, col3, col4, col5 = st.columns(5)
                rating = None
                
                with col1:
                    if st.button("😞 1", key=f"{rating_key}_1"):
                        rating = 1
                with col2:
                    if st.button("🙁 2", key=f"{rating_key}_2"):
                        rating = 2
                with col3:
                    if st.button("😐 3", key=f"{rating_key}_3"):
                        rating = 3
                with col4:
                    if st.button("🙂 4", key=f"{rating_key}_4"):
                        rating = 4
                with col5:
                    if st.button("😊 5", key=f"{rating_key}_5"):
                        rating = 5
                
                if rating:
                    save_feedback(st.session_state.assessment_id, course_name, rating)
                    st.success(f"Thank you for rating {course_name}!")
                
                if i < len(st.session_state.recommendations) - 1:
                    st.divider()
        
        st.divider()
        
        # Back to home button
        if st.button("🏠 Back to Home", use_container_width=True, type="primary"):
            st.session_state.page = 'Dashboard'
            # Clear session data
            st.session_state.assessment_data = None
            st.session_state.recommendations = None
            st.session_state.assessment_id = None
            st.rerun()
    
    else:
        st.error("No recommendations found. Please take the assessment first.")
        if st.button("📝 Take Assessment"):
            st.session_state.page = 'Assessment'
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**Course Recommendation System** - Helping Senior High School students choose their ideal college course")
