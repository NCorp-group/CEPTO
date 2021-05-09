DROP DATABASE IF EXISTS lightguide_dev;
CREATE DATABASE lightguide_dev;
USE lightguide_dev;


CREATE TABLE events (
    id int PRIMARY KEY AUTO_INCREMENT,
    timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Format is YYYY-MM-DD HH:MM:SS',
    event_type_id int NOT NULL,
    -- patient_id varchar(255) NOT NULL,
    -- gateway_id varchar(255) NOT NULL
    patient_id int NOT NULL,
    gateway_id int NOT NULL
);

CREATE TABLE event_types (
    id int PRIMARY KEY AUTO_INCREMENT,
    event_type varchar(255) UNIQUE NOT NULL COMMENT 'Represents an observable event in the LightGuide system e.g. user leaving bed'
);

CREATE TABLE patients (
    id int PRIMARY KEY AUTO_INCREMENT,
    patient_id varchar(255) UNIQUE NOT NULL,
    full_name varchar(255) NOT NULL
);

CREATE TABLE caregivers (
    id int PRIMARY KEY AUTO_INCREMENT,
    caregiver_id varchar(255) UNIQUE NOT NULL,
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
    id int NOT NULL UNIQUE
);

CREATE TABLE gateways (
    id int PRIMARY KEY AUTO_INCREMENT,
    gateway_id varchar(255) NOT NULL UNIQUE
);


ALTER TABLE events ADD FOREIGN KEY (event_type_id) REFERENCES event_types (id);

ALTER TABLE events ADD FOREIGN KEY (patient_id) REFERENCES patients (id);

ALTER TABLE events ADD FOREIGN KEY (gateway_id) REFERENCES gateways (id);

ALTER TABLE sensors ADD FOREIGN KEY (gateway_id) REFERENCES gateways (id);


INSERT INTO event_types(event_type) VALUES
    ('arrived_at_bed'),
    ('arrived_at_toilet'),
    ('left_bed'),
    ('left_path'),
    ('left_toilet'),
    ('notification');

INSERT INTO patients(patient_id, full_name) VALUES('041cb23-31f4-4b27-a20b-d160564e2e68', 'test_patient');

INSERT INTO caregivers(caregiver_id, username, login_credential_hash) VALUES('fef16dcd-87d2-4f2d-a92e-7af18dd605a7', 'caregiver', '3f27b5bf43f45bc9142d9057b78869637f62d8b7ea705403411302c2a6970edb');

INSERT INTO gateways(gateway_id) VALUES('1fb3b683-7fd5-4581-b201-30ac171e5414');

INSERT INTO caregiver_patient_relation(caregiver_id, patient_id) VALUES(1, 1);