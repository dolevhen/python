from sqlalchemy import BIGINT, INT, String, BOOLEAN, TIMESTAMP


incident_mapping = {
     "starfire_incident_id": BIGINT,
     "incident_datetime": TIMESTAMP,
     "incident_borough": String(1000),
     "incident_response_seconds_qy": INT,
     "incident_travel_tm_seconds_qy": INT,
     "incident_classification": String(1000),
     "incident_classification_group": String(1000),
     "incident_close_datetime": TIMESTAMP
 }

alarm_box_mapping = {
     "alarm_box_id": INT,
     "starfire_incident_id": BIGINT,
     "incident_datetime": TIMESTAMP,
     "alarm_box_borough": String(1000),
     "alarm_box_number": INT,
     "alarm_box_location": String(1000),
     "alarm_source_description_tx": String(1000),
     "alarm_level_index_description": String(1000),
     "highest_alarm_level": String(1000)
 }

response_time_mapping = {
     "response_time_id": INT,
     "starfire_incident_id": BIGINT,
     "incident_datetime": TIMESTAMP,
     "dispatch_response_seconds_qy": INT,
     "first_assignment_datetime": TIMESTAMP,
     "first_activation_datetime": TIMESTAMP,
     "valid_dispatch_rspns_time_indc": BOOLEAN,
     "valid_incident_rspns_time_indc": BOOLEAN,
     "incident_response_seconds_qy": INT,
     "incident_travel_tm_seconds_qy": INT,
     "first_on_scene_datetime": TIMESTAMP
 }

resource_assignment_mapping = {
     "assignment_id": INT,
     "starfire_incident_id": BIGINT,
     "incident_datetime": TIMESTAMP,
     "engines_assigned_quantity": INT,
     "ladders_assigned_quantity": INT,
     "other_units_assigned_quantity": INT
 }

geo_information_mapping = {
     "geo_id": INT,
     "starfire_incident_id": BIGINT,
     "incident_datetime": TIMESTAMP,
     "zipcode": INT,
     "policeprecinct": INT,
     "citycouncildistrict": INT,
     "communitydistrict": INT,
     "communityschooldistrict": INT,
     "congressionaldistrict": INT
 }
