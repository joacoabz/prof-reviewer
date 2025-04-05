import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path

# Page configuration
st.set_page_config(page_title="Prof Reviewer - History", page_icon="📚", layout="wide")

st.title("Analysis History")

# Create a directory for storing history if it doesn't exist
HISTORY_DIR = Path("logs/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


# Function to load history entries
def load_history_entries():
    entries = []

    if HISTORY_DIR.exists():
        for file_path in HISTORY_DIR.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Add the filename as ID and extract timestamp from filename
                data["id"] = file_path.stem
                timestamp = file_path.stem.split("_")[0]
                data["timestamp"] = datetime.fromtimestamp(int(timestamp))

                entries.append(data)
            except Exception as e:
                st.error(f"Error loading history entry {file_path}: {str(e)}")

    # Sort entries by timestamp (newest first)
    entries.sort(key=lambda x: x["timestamp"], reverse=True)
    return entries


# Load history entries
history_entries = load_history_entries()

# Display empty state if no history
if not history_entries:
    st.info("No analysis history found. Complete an analysis to see it here.")

    # Show demo entry option
    if st.button("Create Demo History Entry"):
        # Create a demo entry
        demo_entry = {
            "timestamp": datetime.now(),
            "task_description": "Write an essay discussing the impact of technology on education.",
            "general_comment": "The essay presents a well-structured argument with good examples, though some language improvements could be made.",
            "criterion_scores": {
                "content": [
                    4,
                    "The content is relevant and addresses all parts of the task.",
                ],
                "communicative-achievement": [
                    3,
                    "The register is appropriate for an academic essay.",
                ],
                "organisation": [
                    4,
                    "The text is well-organized with clear paragraphs.",
                ],
                "language": [3, "Good range of vocabulary with some errors."],
            },
            "detailed_analysis": [
                {
                    "category": "Content",
                    "text_reference": "Technology has changed education forever and this is a good thing.",
                    "issue": "Overly simplistic claim without nuance or supporting evidence.",
                    "suggestions": [
                        "Add specific examples of how technology has changed education",
                        "Acknowledge both positive and negative impacts",
                        "Use more precise language instead of vague statements like 'good thing'",
                    ],
                },
                {
                    "category": "Language",
                    "text_reference": "Students can access informations from anywhere at anytime.",
                    "issue": "Grammatical error with plural form of 'information'.",
                    "suggestions": [
                        "Change 'informations' to 'information' as it is an uncountable noun",
                        "Revise similar uncountable nouns throughout the essay",
                        "Consider using more precise terms like 'educational resources' or 'learning materials'",
                    ],
                },
                {
                    "category": "Organisation",
                    "text_reference": "Another point to consider is the cost savings. Also, technology enables interactive learning.",
                    "issue": "Abrupt transition between ideas without proper connection.",
                    "suggestions": [
                        "Add a transitional phrase to connect these ideas",
                        "Consider reorganizing these points under appropriate subheadings",
                        "Expand on each point in separate paragraphs for better flow",
                    ],
                },
                {
                    "category": "Communicative Achievement",
                    "text_reference": "It's super cool how tech helps kids learn stuff faster.",
                    "issue": "Informal register inappropriate for an academic essay.",
                    "suggestions": [
                        "Replace informal expressions like 'super cool' with academic language",
                        "Use more precise terminology like 'accelerates learning outcomes'",
                        "Maintain a consistent academic tone throughout the essay",
                    ],
                },
            ],
            "extracted_text": "The Impact of Technology on Education\n\nTechnology has changed education forever and this is a good thing. In the modern classroom, digital tools have transformed how students learn and teachers teach.\n\nFirstly, accessibility has improved. Students can access informations from anywhere at anytime. This flexibility allows for personalized learning experiences that cater to individual needs and schedules.\n\nSecondly, interactive learning has become more common. Through simulations, educational games, and multimedia presentations, complex concepts become easier to understand. This engagement helps with knowledge retention.\n\nAnother point to consider is the cost savings. Also, technology enables interactive learning. Digital textbooks and open educational resources reduce financial barriers.\n\nHowever, there are challenges. The digital divide means not all students have equal access to technology. Additionally, some students become distracted by social media and other non-educational content.\n\nIt's super cool how tech helps kids learn stuff faster. Research shows that properly implemented educational technology can improve learning outcomes significantly.\n\nIn conclusion, while we must address the challenges, the positive impact of technology on education outweighs the negatives, creating more inclusive, engaging, and effective learning environments.",
            "total_score": 14,
            "max_score": 20,
        }

        # Save demo entry
        timestamp = int(datetime.now().timestamp())
        file_path = HISTORY_DIR / f"{timestamp}_demo.json"
        with open(file_path, "w") as f:
            json.dump(demo_entry, f)

        st.success("Demo entry created! Refresh the page to see it.")
        st.rerun()
else:
    # Display history entries in a table
    st.write(f"Found {len(history_entries)} past analyses")

    # Create columns for the table header
    col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 1])
    with col1:
        st.write("**Date**")
    with col2:
        st.write("**Task**")
    with col3:
        st.write("**Score**")
    with col4:
        st.write("**CEFR Level**")
    with col5:
        st.write("**Actions**")

    # Display each history entry
    for entry in history_entries:
        col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 1])

        with col1:
            st.write(entry["timestamp"].strftime("%Y-%m-%d %H:%M"))

        with col2:
            # Truncate task description if it's too long
            task = entry.get("task_description", "No task")
            if len(task) > 100:
                task = task[:97] + "..."
            st.write(task)

        with col3:
            # Display score as fraction and percentage
            total_score = entry.get("total_score", 0)
            max_score = entry.get("max_score", 20)
            score_percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            st.write(f"{total_score}/{max_score} ({score_percentage:.1f}%)")

        with col4:
            # Determine CEFR level based on percentage
            if score_percentage >= 90:
                cefr_level = "C2 (Proficiency)"
            elif score_percentage >= 75:
                cefr_level = "C1 (Advanced)"
            elif score_percentage >= 60:
                cefr_level = "B2 (Upper Int.)"
            elif score_percentage >= 40:
                cefr_level = "B1 (Intermediate)"
            else:
                cefr_level = "A2 or below"
            st.write(cefr_level)

        with col5:
            # View button
            if st.button("View", key=f"view_{entry['id']}"):
                st.session_state.selected_entry = entry

        # Display a separator line
        st.markdown("---")

    # Display selected entry details if there is one
    if "selected_entry" in st.session_state:
        entry = st.session_state.selected_entry

        st.header("Analysis Details")

        # Close button for details view
        if st.button("Close Details"):
            del st.session_state.selected_entry
            st.rerun()

        # Display task
        st.subheader("Task")
        st.write(entry.get("task_description", "No task description available"))

        # Display general comment
        st.subheader("General Comment")
        st.info(entry.get("general_comment", "No general comment available"))

        # Display criterion scores
        st.subheader("Criterion Scores")

        criterion_scores = entry.get("criterion_scores", {})
        for criterion, (score, justification) in criterion_scores.items():
            with st.expander(f"{criterion.title()} - Score: {score}/5"):
                st.write(justification)

        # Display detailed analysis if available
        if detailed_analysis := entry.get("detailed_analysis"):
            st.subheader("Detailed Analysis")

            # Group analysis by category
            analysis_by_category = {}
            for item in detailed_analysis:
                category = item.get("category", "Other")
                if category not in analysis_by_category:
                    analysis_by_category[category] = []
                analysis_by_category[category].append(item)

            # Display analysis grouped by category
            for category, items in analysis_by_category.items():
                with st.expander(f"{category} Issues ({len(items)})"):
                    for i, item in enumerate(items):
                        st.markdown(f"### Issue {i + 1}")

                        # Text reference with highlighting
                        st.markdown("**Text Reference:**")
                        st.markdown(
                            f"<div style='background-color: #ffeeee; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>\"{item.get('text_reference', 'No text reference')}\"</div>",
                            unsafe_allow_html=True,
                        )

                        # Issue description
                        st.markdown("**Issue:**")
                        st.markdown(
                            f"<div style='padding: 10px; border-left: 3px solid #ff6666; margin-bottom: 10px;'>{item.get('issue', 'No issue description')}</div>",
                            unsafe_allow_html=True,
                        )

                        # Suggestions
                        st.markdown("**Suggestions:**")
                        suggestions = item.get("suggestions", [])
                        for j, suggestion in enumerate(suggestions):
                            st.markdown(
                                f"<div style='padding: 5px 10px; margin-bottom: 5px; background-color: #e6f7ff; border-radius: 3px;'>{j + 1}. {suggestion}</div>",
                                unsafe_allow_html=True,
                            )

                        # Add separator between issues
                        if i < len(items) - 1:
                            st.markdown("---")

        # Action buttons
        col1, col2 = st.columns(2)

        with col1:
            st.button("Export to PDF", key=f"export_{entry['id']}")

        with col2:
            if st.button("Delete", key=f"delete_{entry['id']}"):
                # Delete the entry file
                try:
                    file_path = HISTORY_DIR / f"{entry['id']}.json"
                    if file_path.exists():
                        os.remove(file_path)
                        st.success("Entry deleted successfully")

                        # Remove from session state and refresh
                        del st.session_state.selected_entry
                        st.rerun()
                except Exception as e:
                    st.error(f"Error deleting entry: {str(e)}")
