import streamlit as st
import tempfile
import os
from PIL import Image
from pathlib import Path

from src.pipeline.main_pipe import Pipeline

st.set_page_config(page_title="Prof Reviewer - Analysis", page_icon="🔍", layout="wide")

st.title("Student Answer Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Upload student solution image(s)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Upload one or more images of the student's handwritten answer",
    )

    task_prompt = st.text_area(
        "Task Description/Prompt",
        height=150,
        placeholder="Enter the task description or writing prompt given to the student...",
        help="Enter the exact task that was assigned to the student",
    )

    st.markdown("---")

    if uploaded_files and task_prompt:
        if st.button("Analyze", type="primary"):
            with st.spinner("Analyzing student answer..."):
                # Create temporary files to process the images
                temp_image_paths = []

                for uploaded_file in uploaded_files:
                    # Create a temporary file
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".jpg"
                    ) as temp_file:
                        # Write the uploaded file to the temporary file
                        temp_file.write(uploaded_file.getvalue())
                        temp_image_paths.append(temp_file.name)

                # Display the images
                st.subheader("Uploaded Student Answer")

                # Display images with better quality control
                if len(temp_image_paths) == 1:
                    # Single image - display in center with controlled width
                    img = Image.open(temp_image_paths[0])
                    max_width = 500  # Smaller max width
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize(
                            (max_width, new_height)
                        )  # Default resampling is OK
                    st.image(img, use_container_width=False)
                else:
                    # Multiple images - use grid with smaller thumbnails
                    num_cols = min(len(temp_image_paths), 3)
                    image_cols = st.columns(num_cols)
                    for i, img_path in enumerate(temp_image_paths):
                        img = Image.open(img_path)
                        # Smaller thumbnail size for multiple images
                        max_width = 300
                        if img.width > max_width:
                            ratio = max_width / img.width
                            new_height = int(img.height * ratio)
                            img = img.resize(
                                (max_width, new_height)
                            )  # Default resampling is OK
                        image_cols[i % num_cols].image(img, use_container_width=False)

                # Here we would call the OCR and analysis pipeline
                st.info("Running assessment pipeline...")

                try:
                    # Convert string paths to Path objects
                    path_objects = [Path(path) for path in temp_image_paths]

                    # Create and run the assessment pipeline
                    if Pipeline is not None:
                        pipeline = Pipeline(task=task_prompt)
                        general_comment, criterion_scores = pipeline.run(
                            image_paths=path_objects
                        )
                        pipeline_result = True
                    else:
                        raise ImportError("Pipeline module could not be imported")
                except Exception as e:
                    st.error(f"Error running assessment pipeline: {str(e)}")
                    # Use placeholder data in case of error
                    general_comment = "Placeholder general comment. The real application will provide detailed feedback."
                    criterion_scores = {
                        "Content": (
                            3,
                            "Content meets the requirements but could be more detailed.",
                        ),
                        "Communicative Achievement": (
                            4,
                            "Strong communicative skills shown.",
                        ),
                        "Organisation": (
                            3,
                            "Well structured but transitions could be improved.",
                        ),
                        "Language": (4, "Good range of vocabulary with minor errors."),
                    }
                    pipeline_result = False

                # Clean up temporary files
                for temp_path in temp_image_paths:
                    os.unlink(temp_path)

                # Show results in the UI
                st.subheader("Analysis Results")

                # Display the general comment
                st.markdown("### General Feedback")
                st.write(general_comment)

                # Display criterion scores in col2
                with col2:
                    st.subheader("Score Breakdown")

                    # Create a table for the scores
                    score_data = {"Criterion": [], "Score": [], "Justification": []}
                    for criterion, (score, justification) in criterion_scores.items():
                        score_data["Criterion"].append(criterion)
                        score_data["Score"].append(score)
                        score_data["Justification"].append(justification)

                    # Display scores
                    for criterion, (score, justification) in criterion_scores.items():
                        with st.expander(f"{criterion}: {score}/5"):
                            st.write(justification)

                    # Calculate and display overall score
                    total_score = sum(score for score, _ in criterion_scores.values())
                    max_possible = 5 * len(criterion_scores)
                    overall_percent = (total_score / max_possible) * 100

                    st.metric(
                        "Overall Score",
                        f"{total_score}/{max_possible} ({overall_percent:.0f}%)",
                    )

                    # Add CEFR level interpretation
                    if overall_percent >= 90:
                        cefr_level = "C2 (Proficiency)"
                    elif overall_percent >= 75:
                        cefr_level = "C1 (Advanced)"
                    elif overall_percent >= 60:
                        cefr_level = "B2 (Upper Intermediate)"
                    elif overall_percent >= 40:
                        cefr_level = "B1 (Intermediate)"
                    else:
                        cefr_level = "A2 (Elementary) or below"

                    st.info(f"CEFR Level Equivalent: {cefr_level}")

                # If pipeline didn't succeed, show disclaimer
                if not pipeline_result:
                    st.warning(
                        "Note: Using placeholder data. Actual results will use the real pipeline once integrated."
                    )
    else:
        with col2:
            st.info(
                "Please upload student solution image(s) and provide the task description to start analysis."
            )
            st.markdown("""
            ### How the Analysis Works
            1. OCR extracts text from the student's handwritten answer
            2. The extracted text is compared against the task requirements
            3. AI analyzes the response for accuracy, language use, and content
            4. Detailed feedback is generated to help both teachers and students
            """)
