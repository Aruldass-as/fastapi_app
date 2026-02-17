# services/document_processing.py
import PyPDF2
from openai import OpenAI
import os
from dotenv import load_dotenv

from .graph_service import generate_concept_graph

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def generate_summary(text):
    """
    Use GPT to generate summary
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize this document:\n{text}"}],
        temperature=0.5
    )
    summary = response.choices[0].message.content
    return summary

def process_document(file_path):
    text = extract_text_from_pdf(file_path)
    summary = generate_summary(text)
    # Use GPT-based concept extraction for richer graph
    graph = generate_concept_graph(summary)
    return summary, graph
