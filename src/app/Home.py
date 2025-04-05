import streamlit as st

st.set_page_config(page_title="Prof Reviewer - Home", page_icon="📝", layout="wide")

st.title("Welcome to Prof Reviewer")

# Main content in columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## About This App
    Prof Reviewer is a specialized tool for analyzing student answers in Cambridge Certificate of Proficiency in English writing exams.
    
    The app uses advanced AI to extract text from handwritten essays, then provides detailed analysis and feedback based on official Cambridge assessment criteria.
    
    ### Key Features
    - **OCR Text Extraction**: Convert handwritten essays to text
    - **Comprehensive Assessment**: Analysis across four key criteria:
        - Content
        - Communicative Achievement
        - Organisation
        - Language
    - **Detailed Feedback**: Specific improvement suggestions with examples
    - **Visual Score Reports**: Easy-to-understand visualizations
    - **Export Options**: Save and share analysis results
    """)

    # Call to action
    st.markdown("### Ready to start?")
    st.markdown(
        "Click the **Analysis** page in the sidebar to analyze a student essay."
    )

with col2:
    # Image or icon that represents the app
    st.image(
        "https://img.icons8.com/color/240/000000/test-partial-passed.png", width=150
    )

    # Quick navigation cards
    st.markdown("### Quick Navigation")

    # Analysis card
    with st.container():
        st.markdown("#### 📊 Analysis")
        st.markdown("Upload images and analyze student essays")
        if st.button("Go to Analysis", key="goto_analysis"):
            st.switch_page("pages/01_Analysis.py")

    st.markdown("---")

    # History card
    with st.container():
        st.markdown("#### 📚 History")
        st.markdown("View past analyses and results")
        if st.button("View History", key="goto_history"):
            st.switch_page("pages/02_History.py")

# How to use section
st.markdown("---")
st.markdown("## How to Use")

# Create step by step guide with columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 1. Upload")
    st.markdown("Upload images of student handwritten essays")
    st.image("https://img.icons8.com/color/96/000000/upload--v1.png", width=64)

with col2:
    st.markdown("### 2. Describe")
    st.markdown("Enter the task description or prompt")
    st.image("https://img.icons8.com/color/96/000000/task.png", width=64)

with col3:
    st.markdown("### 3. Analyze")
    st.markdown("Run the analysis to assess the essay")
    st.image("https://img.icons8.com/color/96/000000/analyze.png", width=64)

with col4:
    st.markdown("### 4. Review")
    st.markdown("Get detailed feedback and scores")
    st.image("https://img.icons8.com/color/96/000000/report-card.png", width=64)

# Benefits section
st.markdown("---")
st.markdown("## Benefits")

benefit_col1, benefit_col2 = st.columns(2)

with benefit_col1:
    st.markdown("""
    ### For Teachers
    - Save time on grading and feedback
    - Provide consistent, detailed analysis
    - Track student progress over time
    - Focus on teaching rather than assessment
    """)

with benefit_col2:
    st.markdown("""
    ### For Students
    - Receive detailed, objective feedback
    - Identify specific areas for improvement
    - Understand assessment criteria better
    - Track progress toward proficiency
    """)

# Footer
st.markdown("---")
st.markdown("### Technical Information")
st.markdown("""
- Built with Streamlit and OpenAI's GPT-4o model
- OCR capabilities for handwritten text extraction
- Assessment based on Cambridge English Proficiency criteria
""")

# Attribution for icons
st.markdown("---")
st.caption("Icons by Icons8")
