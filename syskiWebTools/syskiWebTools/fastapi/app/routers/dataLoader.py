from dotenv import load_dotenv
import os
from fastapi import APIRouter, File, UploadFile
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.xml import partition_xml
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc
from unstructured.partition.html import (
    partition_html,
    convert_and_partition_html    
)
from unstructured.partition.md import partition_md
from unstructured.partition.text import partition_text

load_dotenv()

router = APIRouter()

def partition_pdf_function(file: UploadFile =File(...)):

    raw_pdf_elements = partition_pdf(
        filename=file.filename,
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        image_output_dir_path=os.getenv("IMAGE_OUTPUT_DIR"),
    )
    return raw_pdf_elements

def partition_xlsx_function(file: UploadFile =File(...)):
    
    raw_xlsx_elements = partition_xlsx(
        filename=file.filename
    )

    return raw_xlsx_elements

def partition_docs_function(file: UploadFile =File(...)):

    raw_docs_elements = partition_doc(
        filename=file.filename,
        include_page_breaks=True,
    )

    return raw_docs_elements

def categorize_elements(elements):

    categorized_elements = {'tables': [], 'texts': []}

    for element in elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements['tables'].append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements['texts'].append(str(element))
    
    return categorized_elements
    
def dataLoadMain(file: UploadFile =File(...)):

    allowed_mime_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]

    content_type = file.content_type

    if content_type in allowed_mime_types:
        if content_type == "application/pdf":
            elements = partition_pdf_function(file)
        elif content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            elements = partition_xlsx_function(file)
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            elements = partition_docs_function(file)
    
    categorized_elements = categorize_elements(elements)

    return categorized_elements