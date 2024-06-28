# GenAICapstone
This is a LLM-PDF-Reader application to provide summaries of uploaded PDFs.

# PDF Reader Tool 1.0

## Overview

This tool is a desktop application for reading summaries of uploaded PDFs using OpenAI's GPT models.

## Features

- **Upload PDF**: Upload a PDF file to extract text and images.
- **Summarize Content**: Generate a concise summary of the PDF content using OpenAI's GPT models.
- **Extract Images**: Extract and save images from the PDF.
- **Save Summaries**: Save the generated summaries as text files.

## Requirements

- Python 3.x
- The following Python libraries:
  - `tkinter`
  - `fitz` (PyMuPDF)
  - `openai`
  - `Pillow`

## Usage

Use the **File** menu to:

- **Open PDF**: Select a PDF to upload. Processing might take a while.

- **Save Summary**: Saves the summary as a text file.

Use the Options menu to:

- **Clear Text area**: Clear the current text area.

- **Delete Summary**: Deletes the currently selected summary


## Additional Info

Remember to set the OpenAI API Key in the utils.py file.

All summaries are automatically saved upon exiting the application (in the summaries.json file).
