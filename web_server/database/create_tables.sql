DROP DATABASE IF EXISTS lightguide_db;
CREATE DATABASE lightguide_db;
USE lightguide_db;


CREATE TABLE events (
    id int PRIMARY KEY AUTO_INCREMENT,
    timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Format is YYYY-MM-DD HH:MM:SS',
    event_type_id int NOT NULL,
    patient_id int NOT NULL,
    gateway_id int NOT NULL,
    visit_id int NOT NULL COMMENT 'Represent a full bathroom visit. Incremented every time left_bed occurs'
);

CREATE TABLE event_types (
    id int PRIMARY KEY AUTO_INCREMENT,
    event_type varchar(255) UNIQUE NOT NULL COMMENT 'Represents an observable event in the LightGuide system e.g. user leaving bed'
);

CREATE TABLE patients (
    id int PRIMARY KEY AUTO_INCREMENT,
    HEUCOD_patient_id varchar(255) UNIQUE NOT NULL COMMENT 'only relevant for HEUCOD compatability',
    full_name varchar(255) NOT NULL
);

CREATE TABLE caregivers (
    id int PRIMARY KEY AUTO_INCREMENT,
    HEUCOD_caregiver_id varchar(255) UNIQUE NOT NULL COMMENT 'only relevant for HEUCOD compatability',
    username varchar(255) UNIQUE NOT NULL,
    login_credential_hash varchar(255) NOT NULL
);


CREATE TABLE caregiver_patient_relation (
    id int PRIMARY KEY AUTO_INCREMENT,
    caregiver_id int NOT NULL,
    patient_id int NOT NULL
);

ALTER TABLE caregiver_patient_relation ADD FOREIGN KEY (caregiver_id) REFERENCES caregivers (id);
ALTER TABLE caregiver_patient_relation ADD FOREIGN KEY (patient_id) REFERENCES patients (id);

CREATE TABLE sensors (
    id int PRIMARY KEY AUTO_INCREMENT,
    sensor_type ENUM ('pir_sensor', 'vibration_sensor') NOT NULL,
    device_model varchar(255) NOT NULL,
    device_vendor varchar(255) NOT NULL,
    HEUCOD_sensor_id char(128) NOT NULL UNIQUE,
    gateway_id int NOT NULL
);

CREATE TABLE gateways (
    id int PRIMARY KEY AUTO_INCREMENT,
    HEUCOD_gateway_id varchar(255) NOT NULL UNIQUE COMMENT 'only relevant for HEUCOD compatability'
);

CREATE TABLE number_of_visits (
    count int NOT NULL COMMENT 'DO NOT MODIFY THIS TABLE, only allowed way is to call increment_visit_id()'
);

INSERT INTO number_of_visits(count) VALUES(0);

ALTER TABLE events ADD FOREIGN KEY (event_type_id) REFERENCES event_types (id);

ALTER TABLE events ADD FOREIGN KEY (patient_id) REFERENCES patients (id);

ALTER TABLE events ADD FOREIGN KEY (gateway_id) REFERENCES gateways (id);

ALTER TABLE sensors ADD FOREIGN KEY (gateway_id) REFERENCES gateways (id);


CREATE PROCEDURE lightguide_db.increment_visit_id()
MODIFIES SQL DATA
/* BEGIN */
    UPDATE number_of_visits
        SET count = count + 1;
/* END; */


INSERT INTO event_types(event_type) VALUES
    ('arrived_at_bed'),
    ('arrived_at_bathroom'),
    ('left_bed'),
    ('left_path'),
    ('left_bathroom'),
    ('alert');

INSERT INTO patients(HEUCOD_patient_id, full_name) VALUES('041cb23-31f4-4b27-a20b-d160564e2e687', 'test_patient');

INSERT INTO caregivers(HEUCOD_caregiver_id, username, login_credential_hash) VALUES('fef16dcd-87d2-4f2d-a92e-7af18dd605a7', 'caregiver', '3f27b5bf43f45bc9142d9057b78869637f62d8b7ea705403411302c2a6970edb');

INSERT INTO gateways(HEUCOD_gateway_id) VALUES('1fb3b683-7fd5-4581-b201-30ac171e5414');

INSERT INTO caregiver_patient_relation(caregiver_id, patient_id) VALUES(1, 1);


INSERT INTO sensors(sensor_type, device_model, device_vendor, HEUCOD_sensor_id, gateway_id) VALUES
    ('pir_sensor', '0x00158d00057acbe7', 'Aqara', '5a679d06-6cd5-454d-bb86-2b1b5bdbdbb1', 1),
    ('pir_sensor', '0x00158d0005729f17', 'Aqara', 'a7236416-0a5a-4119-9144-98293c99ab74', 1),
    ('pir_sensor', '0x00158d00057b4d2a', 'Aqara', 'f3616519-a5f5-498b-b743-359f70457c10', 1),
    ('pir_sensor', '0x00158d00057b28ef', 'Aqara', '10126825-8f93-4063-86a5-297e63caf692', 1),
    ('pir_sensor', '0x00158d00057b2dce', 'Aqara', '97db76dd-0cda-4e1e-9148-dc93487e141b', 1);


-- INSERT INTO events(event_type_id, patient_id, gateway_id, visit_id) VALUES
--    (1, '1', '1', 1),
--    (2, '1', '1', 1),
--    (3, '1', '1', 1),
--    (4, '1', '1', 1),
--    (1, '1', '1', 2);
