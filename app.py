from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Creating Google GenAI Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vector_index = Chroma.from_texts([], embeddings).as_retriever()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_pdf():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdf_files')
        existing_text = ""
        if pdf_files:
            # Process each PDF file
            for pdf in pdf_files:
                pdf_reader = PdfReader(pdf)
                pdf_text = ""

                for page in pdf_reader.pages:
                    pdf_text += page.extract_text()

                # Append new PDF text to existing text
                existing_text += pdf_text

            # Split the combined text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
            text_chunks = text_splitter.split_text(existing_text)

            global vector_index
            vector_index = Chroma.from_texts(text_chunks, embeddings).as_retriever()

            return "Processing complete. You can now ask questions."

    return "Error processing PDFs."

@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.form['question']

    if user_question:
        # Retrieving the context based on the user query
        docs = vector_index.get_relevant_documents(user_question)

        # prompt_template = """
        # Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        # provided context just say, "answer is not available in the context", don't provide the wrong answer. If the query is regarding related documents then generate a response.\n\n
        # Context:\n {context}?\n
        # Question: \n{question}\n
        #
        # Answer:
        # """
        prompt_template = """
                You are a chatbot. 
                Answer the question as detailed as possible using the provided context. 
                Make sure the response is properly framed.
                If no data is available but if accurate result can be generated then give a response 
                else say Answer not available in Context.\n\n
                Context:\n {context}?\n
                Question: \n{question}\n

                Answer:
                """

        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

        return response["output_text"]

    return "Invalid question."

if __name__ == '__main__':
    app.run(debug=True)
