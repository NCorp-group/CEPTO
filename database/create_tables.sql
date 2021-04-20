CREATE TABLE `users` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(255),
  `age` int
);

CREATE TABLE `events` (
  `event_id` int PRIMARY KEY,
  `day` date NOT NULL,
  `leaving_bed` timestamp,
  `arriving_at_toilet` timestamp,
  `leaving_toilet` timestamp,
  `arriving_at_bed` timestamp,
  `user_id` int UNIQUE NOT NULL
);

ALTER TABLE `events` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
