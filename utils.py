# utils.py
import fitz
import openai
import json
import os

# Read OpenAI API key
openai.api_key = 'xxx'

# Load saved summaries from a JSON file
def load_summaries():
    if os.path.exists('summaries.json'):
        with open('summaries.json', 'r') as file:
            return json.load(file)
    return {}

# Save summaries to a JSON file
def save_summaries(summaries):
    with open('summaries.json', 'w') as file:
        json.dump(summaries, file)

# Extract text
def extract_text_from_pdf(pdf_path):
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Extract images
def extract_images_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    image_list = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        image_info = page.get_images(full=True)
        for img_index, img in enumerate(image_info):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            image_extension = base_image["ext"]
            image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_extension}"
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
            image_list.append(image_filename)
    return image_list

# Get summary and metadata from ChatGPT
def get_summary_and_metadata_from_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            #model="gpt-3.5-turbo",

            messages=[
                {"role": "system", "content": "You are an expert in summarizing scientific articles. Extract the most important bullet points, metadata, and keywords from the following scientific article text. Provide a concise summary with a clear title, line breaks, and stylized bullet points. Extract and list metadata such as author names, journal name, publication year, and main keywords. At the end, suggest relevant keywords for the article and provide a suggested reference formatted in Chicago style."},
                {"role": "user", "content": text}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.2,
        )
        return response.choices[0].message['content'].strip().split('\n')
    except Exception as e:
        print(f"Error getting summary from ChatGPT: {e}")
        return ["Error getting summary from ChatGPT."]
