import csv
import petl as etl
from data import resources

class ProcessStreamReader:

    stage_data_path = resources.stage_data_path
    output_data_path = resources.output_data_path

    def __init__ (self, raw_data_frame):
        self.raw_data_frame = raw_data_frame

    def build_output_data (self, frame):
        etl.tocsv(frame, self.output_data_path, encoding='utf-8')
        return 0

    def __append_stage_data (self, frame):
        etl.append(frame, self.stage_data_path, encoding='utf-8')
        return 0

    def __deduplicate_data (self):
        merged_stage_data = etl.fromcsv(self.stage_data_path, encoding='utf-8')
        deduplicated_merged_data_frame = etl.distinct(merged_stage_data, key=resources.unique_token)
        return deduplicated_merged_data_frame

    def stage_search_layer (self, frame):
        stage_frame = etl.convert(frame, resources.contextual_input_read, 'lower')

        for regex_key in resources.inclusion_terms:
            filtered_frame = etl.search(stage_frame, resources.contextual_input_read, regex_key)
            self.__append_stage_data(filtered_frame)
        return 0

    def stage_description_reformat (self):
        stage_description_col_headers = resources.init_columns_to_build # can be overwritten to set preferred columns relevant to build
        # init data header columns for a stage data file
        with open(file=self.stage_data_path, mode="w", newline="") as f:
            csv.writer(f).writerow(stage_description_col_headers)
        init_preprocess_staging_frame = etl.cut(self.raw_data_frame, stage_description_col_headers)
        self.stage_search_layer(init_preprocess_staging_frame)
        return 0

    def generate_data (self):
        self.stage_description_reformat()
        self.build_output_data(self.__deduplicate_data())
        return 0

class DataReader:

    raw_data_path = resources.raw_data_path
    extracted_raw_data_path = resources.extracted_raw_data_path

    def raw_extract (self):
        initial_raw_data_frame = etl.fromcsv(self.raw_data_path, encoding='utf-8')
        extracted_raw_data_columns = etl.cut(initial_raw_data_frame, resources.init_columns_to_extract)
        etl.tocsv(extracted_raw_data_columns, self.extracted_raw_data_path, encoding='utf-8', write_header=False)
        return 0

    def _extract_frame (self):
        # also specifies parsing headers for preprocessing
        extracted_raw_data_frame = etl.fromcsv(self.extracted_raw_data_path, header=resources.init_columns_to_build, encoding='utf-8')
        return extracted_raw_data_frame

    def init_processing (self):
        self.raw_extract()
        extracted_raw_data_frame = self._extract_frame()
        ProcessStreamReader.(raw_data_frame=extracted_raw_data_frame).generate_data()
        return 0
