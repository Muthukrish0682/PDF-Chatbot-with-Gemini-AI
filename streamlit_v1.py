import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Streamlit page configuration
st.set_page_config(page_title="Chat with PDF", layout="centered")
st.title("PDF Chatbot with Gemini AI")

# Gemini API Key Input
GEMINI_API_KEY = st.text_input("Enter your Gemini API Key:", type="password")

if not GEMINI_API_KEY:
    st.warning("Please enter your Gemini API Key to proceed.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

    # PDF File Uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        try:
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Question Input
            question = st.text_input("Ask a question about the PDF content:")

            if question:
                # Optimized Prompt
                prompt = f"""You are an expert at extracting information from technical specification sheets.
                The following text is from a specification sheet for the Barrett™ Whirlpool and Bathtub.
                Your goal is to answer the user's question accurately and concisely using ONLY the information provided in the document.
                If the answer is not explicitly in the document, state that you cannot answer the question.

                Document Text:
                {text}

                User Question: {question}

                Answer:
                """

                # Generate Response
                response = model.generate_content(prompt)
                st.subheader("Answer:")
                st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
