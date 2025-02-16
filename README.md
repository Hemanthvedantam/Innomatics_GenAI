# GenAI Code Reviewer for Innomatic

Welcome to the **GenAI Code Reviewer**, a Streamlit-based application powered by OpenAI's APIs. This project aims to provide intelligent and automated code review functionality, offering valuable insights, suggestions, and feedback for developers.

---

## Features

- **AI-Powered Code Review**: Automatically review code for best practices, bugs, and improvements using OpenAI's language models.
- **Streamlit Interface**: User-friendly, interactive interface for uploading code files or pasting code snippets.
- **Customizable Feedback**: Supports configurable feedback levels (e.g., beginner, intermediate, expert).
- **Language-Agnostic**: Capable of reviewing code in multiple programming languages.
- **Real-Time Suggestions**: Provides instant feedback on coding standards, security vulnerabilities, and optimizations.

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: OpenAI API (GPT-4 or GPT-3.5-turbo)
- **Deployment**: Streamlit Cloud or any cloud service provider
- **Languages Supported**: Python, JavaScript, Java, C++, and more

---

## Installation

Follow the steps below to set up the project locally:

### Prerequisites

- Python 3.9 or above
- OpenAI API key
- Streamlit installed (`pip install streamlit`)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/genai-code-reviewer.git
   cd genai-code-reviewer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. Access the application at `http://localhost:8501`.

---

## Usage

1. Launch the application.
2. Upload a code file or paste code directly into the text area.
3. Select the desired review parameters (e.g., language, depth of feedback).
4. Click **Review Code** to get AI-generated insights and suggestions.
5. Export the review summary if needed.

---

## Contribution Guidelines

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Acknowledgements

- **Innomatic** for providing the opportunity to build this project.
- **OpenAI** for the robust APIs.
- **Streamlit** for the interactive interface framework.

---
