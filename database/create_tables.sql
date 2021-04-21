CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `age` tinyint
);

CREATE TABLE `events` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `event` ENUM ('leaving_bed', 'arriving_at_toilet', 'leaving_toilet', 'arriving_at_bed', 'notification', 'leaving_path') NOT NULL,
  `time` datetime NOT NULL DEFAULT (now()),
  `user_id` int
);

ALTER TABLE `events` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

