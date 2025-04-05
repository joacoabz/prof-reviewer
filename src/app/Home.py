import streamlit as st

st.set_page_config(page_title="Prof Reviewer - Home", page_icon="📝", layout="wide")

st.title("Welcome to Prof Reviewer")

st.markdown("""
## About This App
Prof Reviewer helps analyze student answers in Cambridge Certificate of Proficiency in English writing.
The app uses computer vision to extract text from handwritten essays, then provides detailed analysis and feedback.

## How to Use
1. Navigate to the **Analysis** page using the sidebar
2. Upload student solution image(s)
3. Enter the task description/prompt
4. Click 'Analyze' to get detailed feedback on the student's work

## Benefits
- Save time on grading and feedback
- Provide consistent, detailed analysis
- Identify strengths and areas of improvement
- Generate constructive feedback for students
""")

st.sidebar.success("Select a page above")
