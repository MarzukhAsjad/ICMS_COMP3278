-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET GLOBAL time_zone = '+8:00';

DROP DATABASE IF EXISTS project;
Create database project;
use project;
# Create TABLE 'Student'
CREATE TABLE `Student` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (student_id)

);


CREATE TABLE `Course` (
  `course_name` varchar(50) NOT NULL, 
  `course_id` varchar(100) NOT NULL, 

  PRIMARY KEY (course_id)
);


CREATE TABLE `Course_Materials` (
  `material_id` int NOT NULL AUTO_INCREMENT,
  `course_id` varchar(50) NOT NULL, 
  `material_type` varchar(50) NOT NULL, 
  `material` varchar(100) NOT NULL,

  PRIMARY KEY (material_id),
  FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE `Study` (
  `student_id` int NOT NULL,
  `course_id` varchar(50) NOT NULL, 

  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (course_id) REFERENCES Course(course_id)
);


# Create TABLE 'Class'
CREATE TABLE `Class` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `classroom_address` varchar(50) NOT NULL, 
  `course_id` varchar(50) NOT NULL, 
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL,
  
  PRIMARY KEY (class_id),
  FOREIGN KEY (course_id) REFERENCES Course(course_id)
);



# Create TABLE 'Activity'
CREATE TABLE `Activity` (
  `activity_id` int NOT NULL AUTO_INCREMENT,
  `activity` varchar(50) NOT NULL, 
  `activity_time` datetime NOT NULL,
  `student_id` int NOT NULL,

  PRIMARY KEY (activity_id),
  FOREIGN KEY (student_id) REFERENCES Student(student_id)
);



INSERT into Student (`student_id`, `name`)
VALUES ('0','Your_name');

INSERT into Course (`course_name`, `course_id`)
VALUES ('Database Management Course', 'COMP3278');

INSERT into Course(`course_name`, `course_id`)
VALUES ('Introduction to Java', 'COMP2396');

INSERT into Course(`course_name`, `course_id`)
VALUES ('Cyber Security', 'COMP3355');

INSERT into Course(`course_name`, `course_id`)
VALUES ('Functional Programming', 'COMP3258');

INSERT into Study (`student_id`, `course_id`)
VALUES (0, 'COMP3278');
INSERT into Study(`student_id`, `course_id`)
VALUES (0, 'COMP2396');
INSERT into Study(`student_id`, `course_id`)
VALUES (0, 'COMP3355');
INSERT into Study(`student_id`, `course_id`)
VALUES (0, 'COMP3258');

INSERT into Class (class_id, classroom_address, course_id, start_time, end_time)
VALUES (0,'MTW3', 'COMP3278', '2022-11-20 16:20:00','2022-11-20 17:20:00');
INSERT into Class (class_id, classroom_address, course_id, start_time, end_time)
VALUES (1,'CPD 1.17', 'COMP3278', '2022-11-20 17:20:00','2022-11-20 18:20:00');
INSERT into Class (class_id, classroom_address, course_id, start_time, end_time)
VALUES (2,'MTW9', 'COMP3278', '2022-11-20 18:20:00','2022-11-20 19:20:00');
INSERT into Class (class_id, classroom_address, course_id, start_time, end_time)
VALUES (3,'MTW4', 'COMP3278', '2022-11-20 19:20:00','2022-11-20 19:20:00');

INSERT into Class(class_id, classroom_address, course_id, start_time, end_time)
VALUES (4, 'MTW1', 'COMP3258', '2022-11-21 11:00:00','2022-11-21 12:30:00');
INSERT into Class(class_id, classroom_address, course_id, start_time, end_time)
VALUES (5, 'MTW7', 'COMP2396', '2022-11-21 12:45:00','2022-11-22 16:30:00');
INSERT into Class(class_id, classroom_address, course_id, start_time, end_time)
VALUES (6, 'MTW6', 'COMP3355', '2022-11-22 11:45:00','2022-11-22 14:30:00');
INSERT into Class(class_id, classroom_address, course_id, start_time, end_time)
VALUES (7, 'MTW4', 'COMP2396', '2022-11-22 16:45:00','2022-11-22 19:30:00');
INSERT into Class(class_id, classroom_address, course_id, start_time, end_time)
VALUES (8, 'MTW3', 'COMP3258', '2022-11-23 11:00:00','2022-11-22 12:30:00');


Insert into Activity (activity_id, activity, activity_time, student_id)
VALUES (0,'Login', '2022-11-19 15:30:00',0);
Insert into Activity
VALUES (1,'View Course Info', '2022-11-19 15:30:01',0);
Insert into Activity
VALUES (2,'View Timetable', '2022-11-19 15:31:00',0);
Insert into Activity
VALUES (3,'Login', '2022-11-20 11:30:00',0);
Insert into Activity
VALUES (4,'View Course Info', '2022-11-20 11:30:02',0);
Insert into Activity
VALUES (5,'Login', '2022-11-20 12:30:34',0);


Insert into Course_Materials (material_id, course_id, material_type, material)
values (0,'COMP3278', 'others', 'assignment1.pdf') ;

Insert into Course_Materials (material_id, course_id, material_type, material)
values (1,'COMP3278', 'lecture_notes', 'Lecture_1.pdf') ;

Insert into Course_Materials (material_id, course_id, material_type, material)
values (3,'COMP3278', 'others', 'lab_1.zip') ;

Insert into Course_Materials (material_id, course_id, material_type, material)
values (4,'COMP3278', 'tutorial_notes', 'lab_1.zip') ;



Drop database if exists facerecognition;
Create database facerecognition;
use facerecognition;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

DROP TABLE IF EXISTS `Student`;

# Create TABLE 'Student'
CREATE TABLE `Student` (
  `student_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Student` WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
INSERT INTO `Student` VALUES (1, "Your_name", NOW(), '2021-01-20');
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;




