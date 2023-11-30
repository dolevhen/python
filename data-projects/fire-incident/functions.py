from conn_class import NYCData
import requests
import json
import pandas as pd
import sqlalchemy
import logging
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_data(data_url, chunk_size=None, query_params=None, limit=None):
    try:
        nyc_data = NYCData(data_url)
        count = nyc_data._get_count() if limit is None else limit
        nyc_data._validate_count(count)

        if chunk_size is None:
            chunk_size = NYCData.DEFAULT_CHUNK_SIZE

        data_list = []
        total_rows_fetched = 0

        for offset in range(0, count, chunk_size):
            chunk_size = min(chunk_size, count - total_rows_fetched)

            chunk_query = {
                '$limit': chunk_size,
                '$offset': offset
            }

            if query_params:
                chunk_query.update(query_params)

            chunk_data = _fetch_data(data_url, chunk_query)
            total_rows_fetched += len(chunk_data)
            data_list.extend(chunk_data)

            logger.info(f"Processed {total_rows_fetched} out of {count} rows so far.")

        logger.info(f"Finished fetching. Total rows fetched: {len(data_list)}.")
        return data_list

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise ValueError from e


def _fetch_data(data_url, query_params):
    response = requests.get(data_url, params=query_params)
    response.raise_for_status()
    return json.loads(response.text)


def fill_null_cols(df, col1, col2, col3=None):
    df.loc[df[col1].isnull(), col1] = df[col2]
    df.loc[df[col2].isnull(), col2] = df[col1]

    if col3:
        df.loc[df[col1].isnull(), col1] = df[col3]
        df.loc[df[col2].isnull(), col2] = df[col3]

    return df


def map_yes_no_to_binary(df: pd.DataFrame, column_name: str) -> pd.DataFrame:

    if column_name not in df.columns:
        logger.error(f"The specified column '{column_name}' does not exist in the DataFrame.")
        raise ValueError(f"The specified column '{column_name}' does not exist in the DataFrame.")

    unique_values = df[column_name].unique()
    if set(unique_values) - {'Y', 'N'}:
        logger.warning(
            f"The column '{column_name}' contains values other than 'Y' and 'N'. Unexpected values will not be converted.")

    df[column_name] = df[column_name].map({'Y': 1, 'N': 0}, na_action='ignore')

    logger.info(f"Column '{column_name}' successfully mapped from 'Y' and 'N' to 1 and 0.")
    return df


def move_column_to_first(df, column_name):
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")

    cols = [column_name] + [col for col in df if col != column_name]
    return df[cols]


def create_engine_with_retry(conn_string, max_retries=3):
    for attempt in range(max_retries):
        try:
            engine = sqlalchemy.create_engine(conn_string)
            return engine
        except sqlalchemy.exc.SQLAlchemyError as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt == max_retries - 1:
                raise
            else:
                continue


def write_df_to_postgres(df, conn_string, table_name, dtype, if_exists='replace', chunk_size=None, max_retries=3):
    try:
        engine = create_engine_with_retry(conn_string, max_retries)
        total_rows = len(df)
        rows_written_so_far = 0
        initial_if_exists = if_exists

        num_chunks = math.ceil(total_rows / chunk_size) if chunk_size else 1

        logger.info(f"Starting to write {total_rows} rows to {table_name} table in {num_chunks} chunks.")

        for i in range(num_chunks):
            start_index = i * chunk_size
            end_index = min(start_index + chunk_size, total_rows) if chunk_size else total_rows
            chunk = df.iloc[start_index:end_index]

            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists=initial_if_exists,
                index=False,
                chunksize=chunk_size,
                dtype=dtype
            )
            rows_written_so_far += len(chunk)
            logger.info(f"Wrote chunk {i + 1} to {table_name} table with {rows_written_so_far}/{total_rows} rows.")
            initial_if_exists = 'append'

        logger.info(f"Finished writing to {table_name} table. Total rows written: {rows_written_so_far}")

    except Exception as e:
        logger.error(f"Error writing data to PostgreSQL: {e}")
        raise

