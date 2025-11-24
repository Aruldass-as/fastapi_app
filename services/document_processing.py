# services/document_processing.py
import PyPDF2
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def split_into_sections(text):
    """
    Simple split by headings. Adjust regex if needed.
    """
    import re
    # Split by lines that start with capital letter + colon or numbering
    sections = re.split(r'\n(\d+\..+?|[A-Z][^\n]+)\n', text)
    # Filter empty strings
    sections = [s.strip() for s in sections if s.strip()]
    return sections

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

def generate_graph(sections):
    """
    Create nodes for each section, edges connecting sequentially
    """
    nodes = [{"id": f"node{i}", "label": sec[:50]} for i, sec in enumerate(sections)]
    edges = [{"source": f"node{i}", "target": f"node{i+1}"} for i in range(len(nodes)-1)]
    return {"nodes": nodes, "edges": edges}

def process_document(file_path):
    text = extract_text_from_pdf(file_path)
    sections = split_into_sections(text)
    summary = generate_summary(text)
    graph = generate_graph(sections)
    return summary, graph
