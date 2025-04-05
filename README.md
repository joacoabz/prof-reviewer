# Prof Reviewer

A specialized tool for analyzing student answers in Cambridge Certificate of Proficiency in English (CPE) writing exams.

![Prof Reviewer](https://img.icons8.com/color/240/000000/test-partial-passed.png)

## Overview

Prof Reviewer uses advanced AI to extract text from handwritten essays, then provides detailed analysis and feedback based on official Cambridge assessment criteria. The application helps teachers save time while providing consistent, detailed feedback to students.

## Features

- **OCR Text Extraction**: Convert handwritten essays to text using Computer Vision.
- **Comprehensive Assessment**: Analysis across four key criteria:
  - Content
  - Communicative Achievement
  - Organisation
  - Language
- **Detailed Feedback**: Specific improvement suggestions with examples, text references, and issue identification
- **Visual Score Reports**: Easy-to-understand visualizations including radar charts and bar graphs
- **Export Options**: Generate professional PDF reports with charts and annotations
- **Analysis History**: Track multiple essay assessments over time


## Getting Started

### Prerequisites

- Python 3.9+
- pip or uv package manager
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/prof-reviewer.git
cd prof-reviewer
```

**On Linux/Mac:**
```bash
chmod +x start.sh  # Make the script executable (first time only)
./start.sh
```

**On Windows:**
```
start.bat
```

These scripts will:
1. Create a virtual environment
2. Activate the virtual environment
3. Install all dependencies
4. Create necessary directories
5. Start the Streamlit application

Alternatively, you can manually run the application:

```bash
streamlit run src/app/Home.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
prof-reviewer/
├── .env                # Environment variables (create from .env.example)
├── .env.example        # Example environment variables
├── .streamlit/         # Streamlit configuration
├── logs/               # Analysis logs
│   └── history/        # Saved analysis results
├── prompts/            # Assessment prompts for AI
├── src/
│   ├── app/            # Streamlit application
│   │   ├── Home.py     # Main page
│   │   └── pages/      # Additional pages
│   ├── ocr/            # OCR functionality
│   ├── openai/         # OpenAI integration
│   └── pipeline/       # Assessment pipeline
└── utils/              # Utility functions
```