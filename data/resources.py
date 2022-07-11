import os
from dotenv import load_dotenv

load_dotenv()

raw_data_path = 'data/raw_data.csv'
extracted_raw_data_path = 'data/raw_extracted_data.csv'
stage_data_path = 'data/stage_data.csv'
output_data_path = 'data/output_data.csv'
init_columns_to_extract = os.getenv("INIT_COLUMNS_TO_EXTRACT") or [ 'some id', 'Pet 1', 'Pet 2', 'total', 'notes' ]
init_columns_to_build = os.getenv("INIT_COLUMNS_TO_BUILD") or ['ID', 'PET_1', 'PET_2', 'TOTAL_COUNT', 'NOTES' ] # TODO functionality limited to renaming
inclusion_terms = os.getenv("INCLUSION_TERMS") or ['.goldfish.', '.fishbowl.', '.bubbles.']
unique_token = os.getenv("UNIQUE_TOKEN") or 'ID'
contextual_input_read = os.getenv("CONTEXTUAL_INPUT_READ") or 'NOTES'
