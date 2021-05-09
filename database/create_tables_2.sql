
CREATE TABLE events (
  id int PRIMARY KEY AUTO_INCREMENT,
  ts timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_type_id int NOT NULL,
  patient_id varchar(255) NOT NULL,
  gateway_id varchar(255) NOT NULL
);

CREATE TABLE event_types (
  id int PRIMARY KEY AUTO_INCREMENT,
  event_type varchar(255) UNIQUE NOT NULL COMMENT 'Represents an observable event in the LightGuide system e.g. user leaving bed'
);

CREATE TABLE patients (
  patient_id varchar(255) PRIMARY KEY
);

CREATE TABLE sensors (
  id int PRIMARY KEY AUTO_INCREMENT,
  sensor_type ENUM ('pir_sensor', 'vibration_sensor') NOT NULL,
  device_model varchar(255) NOT NULL,
  device_vendor varchar(255) NOT NULL,
  gateway_id varchar(255) NOT NULL
);

CREATE TABLE gateways (
  gateway_id varchar(255) PRIMARY KEY
);


ALTER TABLE events ADD FOREIGN KEY (event_type_id) REFERENCES event_types (id);

ALTER TABLE events ADD FOREIGN KEY (patient_id) REFERENCES patients (patient_id);

ALTER TABLE events ADD FOREIGN KEY (gateway_id) REFERENCES gateways (gateway_id);

ALTER TABLE sensors ADD FOREIGN KEY (gateway_id) REFERENCES gateways (gateway_id);


INSERT INTO event_types(event_type) VALUES
    ('arrived_at_bed'),
    ('arrived_at_toilet'),
    ('left_bed'),
    ('left_path'),
    ('left_toilet'),
    ('notification');

INSERT INTO patients(patient_id) VALUES('041cb23-31f4-4b27-a20b-d160564e2e68');

INSERT INTO gateways(gateway_id) VALUES('1fb3b683-7fd5-4581-b201-30ac171e5414');