import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import PyPDF2

key = "b2910e5e03fe4418997fbe2685763a90"
endpoint = "https://ai102servicesbylg.cognitiveservices.azure.com/"

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""  # Extract text from each page
        return text

# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Text summarization example
def text_summarization_example(client, text_from_pdf, file_name):

    try:
        # Skip if the extracted text is empty or just whitespace
        if not text_from_pdf.strip():
            print(f"Skipped {file_name} because it has no valid text.")
            return

        # Define the documents for summarization
        documents = [text_from_pdf]

        # Summarize the document using the Azure AI Text Analytics client
        poller = client.begin_extract_summary(documents=documents)
        results = poller.result()

        # Process and display the summaries
        for result in results:
            if not result.is_error:
                print(f"Summary of {file_name}:")
                for sentence in result.sentences:
                    print("\t", sentence.text)
            else:
                print(f"Error in {file_name}: {result.error}")

    except Exception as err:
        print(f"Encountered exception while processing {file_name}. {err}")

# Function to process all PDF files in a folder
def process_pdfs_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, file_name)
            print(f"Processing: {file_name}")
            text_from_pdf = extract_text_from_pdf(pdf_file_path)
            text_summarization_example(client, text_from_pdf, file_name)

# Path to your folder containing PDF files
folder_path = r"C:\Users\lesalgad\Desktop\PDF_Folder"

# Process all PDFs in the folder
process_pdfs_in_folder(folder_path)
