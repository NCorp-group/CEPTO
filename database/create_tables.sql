/* CREATE DATABASE IF NOT EXISTS lightguide_dev; */
/* USE lightguide_dev; */

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
  user_id int PRIMARY KEY AUTO_INCREMENT,
  full_name varchar(255) NOT NULL,
  date_of_birth date
) ENGINE=InnoDB;

DROP TABLE IF EXISTS event_types;

CREATE TABLE IF NOT EXISTS event_types (
  event_type_id int PRIMARY KEY AUTO_INCREMENT,
  event_type varchar(255) UNIQUE NOT NULL COMMENT 'Represents an observable event in the LightGuide system e.g. user leaving bed'
) ENGINE=InnoDB;

DROP TABLE IF EXISTS events;

CREATE TABLE IF NOT EXISTS events (
  event_id int PRIMARY KEY AUTO_INCREMENT,
  time_of_occurence datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id int NOT NULL,
  event_type_id int NOT NULL
  /* CONSTRAINT fk_e_et FOREIGN KEY (event_type_id) REFERENCES event_types (event_type_id), */
  /* CONSTRAINT fk_e_u FOREIGN KEY (user_id) REFERENCES users (user_id) */
) ENGINE=InnoDB;


INSERT INTO event_types(event_type) VALUES
    ('arriving_at_bed'),
    ('arriving_at_toilet'),
    ('leaving_bed'),
    ('leaving_path'),
    ('leaving_toilet'),
    ('notification');

/* ALTER TABLE event_types ADD FOREIGN KEY (event_type_id) REFERENCES events (event_type_id); */

/* ALTER TABLE events ADD FOREIGN KEY (event_type_id) REFERENCES event_types (event_type_id); */

ALTER TABLE events ADD FOREIGN KEY (user_id) REFERENCES users (user_id);


