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
import logging

load_dotenv()

router = APIRouter()

logging.basicConfig(level=logging.INFO)

def partition_pdf_function(file_path):

    raw_pdf_elements = partition_pdf(filename=file_path, strategy="hi_res",
                        languages=['jpn','eng'],
                        extract_images_in_pdf=True,
                        extract_image_block_types=["Image","Table"],
                        extract_image_block_to_payload=False,
                        extract_image_block_output_dir="./images",
                        chunking_strategy="by_title",
                        max_characters=4000,
                        new_after_n_chars=3800,
                        combine_text_under_n_chars=2000,)
    return raw_pdf_elements
'''
    raw_pdf_elements = partition_pdf(
        filename=file_path,
        languages=['jpn','eng'],
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        image_output_dir_path=file_path + "/images",
    )
'''

def partition_xlsx_function(file_path):
    
    raw_xlsx_elements = partition_xlsx(
        filename=file_path,
        include_metadata=True,
        include_header=True,
        find_subtable=True
    )

    return raw_xlsx_elements

def partition_docs_function(file_path):
    logging.info('START: partition_docs_function')
    raw_docs_elements = partition_doc(
        filename=file_path,
        include_page_breaks=True,
    )
    logging.info('END: partition_docs_function')
    return raw_docs_elements

def categorize_elements(elements):
    logging.info('START: categorize_elemets')
    categorized_elements = {'tables': [], 'texts': []}

    for element in elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements['tables'].append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements['texts'].append(str(element))

    logging.info('END: categorize_elemets')
    return categorized_elements

      
def data_load_main(file_path: str):
    logging.info('START: dataLoadMain')

    elements = None
    
    extension = os.path.splitext(file_path)[1].lower()

    if extension in os.getenv("ALLOWED_CONTENTS_EXTENSION"):
        logging.info('analyzing file types...')
        if extension in ['.pdf']:
            logging.info('file type is pdf. Then executing partition_pdf_function')
            elements = partition_pdf_function(file_path)
        elif extension in ['.xls','.xlsx']:
            logging.info('file type is xlsx. Then executing partition_xlsx_function')
            elements = partition_xlsx_function(file_path)
        elif extension in ['.doc','.docx']:
            logging.info('file type is docx. Then executing partition_docs_function')
            elements = partition_docs_function(file_path)
    else:
        logging.warning('Unsupported file type.')

    if elements is not None:
        categorized_elements = categorize_elements(elements)
    else:
        logging.warning('No elements to categorize, returning empty categorization.')
        categorized_elements = {'tables': [], 'texts': []}

    logging.info('END: dataLoadMain')
    return categorized_elements