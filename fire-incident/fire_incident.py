from functions import get_data, fill_null_cols, map_yes_no_to_binary, move_column_to_first, write_df_to_postgres
from cols_type import incident_mapping, alarm_box_mapping, response_time_mapping, resource_assignment_mapping, \
    geo_information_mapping
from conn_class import NYCData
import pandas as pd


conn_string = 'postgresql://@localhost:5432/firearcdb'
path = 'https://data.cityofnewyork.us/resource/8m42-w767.json'
nyc_data = NYCData(path)
data = get_data(data_url=path, chunk_size=200000, limit=None)
df = pd.DataFrame(data)


unique_rows_count_df = df.drop_duplicates()

fill_empty_datetime_upgrade_df = fill_null_cols(df=unique_rows_count_df,
                                                col1='first_assignment_datetime',
                                                col2='first_activation_datetime',
                                                col3='incident_close_datetime')

fill_empty_datetime_read_func = fill_null_cols(df=fill_empty_datetime_upgrade_df,
                                               col1='first_on_scene_datetime',
                                               col2='incident_close_datetime')

valid_dispatch_rspns_time_indc_bool_df = map_yes_no_to_binary(fill_empty_datetime_read_func,
                                                              'valid_dispatch_rspns_time_indc')
fill_empty_datetime_read_func_bool_df = map_yes_no_to_binary(valid_dispatch_rspns_time_indc_bool_df,
                                                             'valid_incident_rspns_time_indc')


df_incidents = fill_empty_datetime_read_func_bool_df[[
    "starfire_incident_id",
    "incident_datetime",
    "incident_borough",
    "incident_response_seconds_qy",
    "incident_travel_tm_seconds_qy",
    "incident_classification",
    "incident_classification_group",
    "incident_close_datetime"
    ]]

df_alarm_box = fill_empty_datetime_read_func_bool_df[[
    "starfire_incident_id",
    "incident_datetime",
    "alarm_box_borough",
    "alarm_box_number",
    "alarm_box_location",
    "alarm_source_description_tx",
    "alarm_level_index_description",
    "highest_alarm_level"
    ]].copy()

df_alarm_box.loc[:, 'alarm_box_id'] = df_alarm_box.index + 1
final_df_alarm_box = move_column_to_first(df_alarm_box, 'alarm_box_id')

df_response_time = fill_empty_datetime_read_func_bool_df[[
   "starfire_incident_id",
   "incident_datetime",
   "dispatch_response_seconds_qy",
   "first_assignment_datetime",
   "first_activation_datetime",
   "valid_dispatch_rspns_time_indc",
   "valid_incident_rspns_time_indc",
   "incident_response_seconds_qy",
   "incident_travel_tm_seconds_qy",
   "first_on_scene_datetime"
    ]].copy()

df_response_time.loc[:, 'response_time_id'] = df_response_time.index + 1
final_df_response_time = move_column_to_first(df_response_time, 'response_time_id')

df_resource_assignment = fill_empty_datetime_read_func_bool_df[[
    "starfire_incident_id",
    "incident_datetime",
    "engines_assigned_quantity",
    "ladders_assigned_quantity",
    "other_units_assigned_quantity"
    ]].copy()

df_resource_assignment.loc[:, 'assignment_id'] = df_resource_assignment.index + 1
final_df_resource_assignment = move_column_to_first(df_resource_assignment, 'assignment_id')

df_geo_information = fill_empty_datetime_read_func_bool_df[[
     "starfire_incident_id",
     "incident_datetime",
     "zipcode",
     "policeprecinct",
     "citycouncildistrict",
     "communitydistrict",
     "communityschooldistrict",
     "congressionaldistrict"
    ]].copy()

df_geo_information.loc[:, 'geo_id'] = df_geo_information.index + 1
final_df_geo_information = move_column_to_first(df_geo_information, 'geo_id')

write_df_incidents_to_postgres = write_df_to_postgres(
    df=df_incidents,
    conn_string=conn_string,
    table_name='incidents_test',
    dtype=incident_mapping,
    if_exists='replace',
    chunk_size=200000
)

write_df_alarm_box_to_postgres = write_df_to_postgres(
    df=final_df_alarm_box,
    conn_string=conn_string,
    table_name='alarm_box',
    dtype=alarm_box_mapping,
    if_exists='replace',
    chunk_size=200000
)

write_df_response_time_to_postgres = write_df_to_postgres(
    df=final_df_response_time,
    conn_string=conn_string,
    table_name='response_time',
    dtype=response_time_mapping,
    if_exists='replace',
    chunk_size=200000
)

write_df_resource_assignment_to_postgres = write_df_to_postgres(
    df=final_df_resource_assignment,
    conn_string=conn_string,
    table_name='resource_assignment',
    dtype=resource_assignment_mapping,
    if_exists='replace',
    chunk_size=200000
)

write_df_geo_information_to_postgres = write_df_to_postgres(
    df=final_df_geo_information,
    conn_string=conn_string,
    table_name='geo_information',
    dtype=geo_information_mapping,
    if_exists='replace',
    chunk_size=200000
)
