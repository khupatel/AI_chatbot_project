# Document Parsing
from PyPDF2 import PdfReader
from flask import Flask, request, render_template
from docx import Document

# Open the PDF file
file_path = "C:/Users/7849l/Desktop/test.docx"
extracted_texts = {}

# Extract text from each page
# iterating through each page and extracting the text
# printing the text on each page
# extracted text is stored by page

def extract_text_from_pdf(file_path):

    if file_path.endswith(".pdf"):
        pdf_reader = PdfReader(file_path)
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            extracted_texts[page_num + 1] = page_text
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        page_num = 1
        for paragraph in doc.paragraphs:
            if paragraph.text:
                extracted_texts[page_num] = paragraph.text.strip().lower()
            page_num += 1

    return extracted_texts

# Load and preprocess the documents
extracted_texts = extract_text_from_pdf(file_path)

# Handling the Query
# Retrieve the user's question
# stripping white spaces and converting to lowercase
def handle_query(query):
    results = search_documents(query, extracted_texts)

    print(f"Search results: {results}")
    return results

# searching the document
# catches the first time the word is used in the document
def search_documents(query, texts, snippet_length=30):
    results = []

    for page_num, text in texts.items():
        text = text.lower()
        if query in text:
            # find the index where the query was found
            start_index = text.index(query)

            # creating a snippet
            # calculate the start and end indices for the snippet
            start_snippet = max(start_index - snippet_length, 0)
            end_snippet = start_index + len(query) + snippet_length

            # extract the snippet from the original text
            snippet = text[start_snippet:end_snippet].strip()

            results.append((page_num, snippet))
    return results

# Flask app integration
app = Flask(__name__)

# GET request: Default request type when a page is loaded/refreshed; displays the search form without any results
# POST request: Triggered when user submits a query via the form; tells Flask to process the form data and display the results

@app.route("/", methods=["GET", "POST"])
def index():
    query = None
    results = []

    # if request is a POST (form was submitted)
    if request.method == "POST":
        query = request.form["query"].strip().lower()
        results = handle_query(query)

    return render_template("index.html", query=query, results=results)

# running the flask app locally
if __name__ == "__main__":
    app.run(port=81, debug=True)
