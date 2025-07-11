CREATE DATABASE  IF NOT EXISTS `shixun` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `shixun`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: shixun
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `account` char(11) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `admin_id_UNIQUE` (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'13355535073','scrypt:32768:8:1$ln8IipMh5Jgvddos$f9c273ddcce6bc756576a6f154ac6082aa5bac898bea80669e9c52414b4f09baa52db3377b3c5fc5f9ea04ac6af7d2ce18b58db3384994dfa5d1ab504d5462b7'),(2,'12345678910','scrypt:32768:8:1$V8UnvsGGQ88DvWCS$d3d47d993bd676e37b6f46ed842dd92e17e701740901c15b3803159954bbefe93c8c0322052c919e954e00c42d11323e5a00168caa9aa9bc7693bb75f01e1ac4');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `record` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `video_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `state` int DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `expiration_time` datetime DEFAULT NULL,
  PRIMARY KEY (`record_id`),
  UNIQUE KEY `record_id_UNIQUE` (`record_id`),
  KEY `video_id_idx` (`video_id`),
  KEY `uesr_id_idx` (`user_id`),
  CONSTRAINT `fk_record_users` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_record_video` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
INSERT INTO `record` VALUES (35,5,4,2,'2025-07-07 14:39:13','2025-08-06 14:39:13'),(37,7,4,2,'2025-07-07 14:39:20','2025-08-06 14:39:20'),(38,15,4,2,'2025-07-08 09:05:10','2025-08-07 09:05:10'),(46,23,6,2,'2025-07-08 16:40:27','2025-08-07 16:40:27'),(49,24,6,2,'2025-07-08 17:05:56','2025-08-07 17:05:56');
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `pose_estimate` text,
  `result_id` int NOT NULL,
  PRIMARY KEY (`result_id`),
  UNIQUE KEY `report_id_UNIQUE` (`report_id`),
  CONSTRAINT `fk_report_result` FOREIGN KEY (`result_id`) REFERENCES `result` (`result_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (4,'F:\\download\\shixun\\aimodel\\report\\tt_ball_detect_pose_detect_report.md',1),(16,'F:\\download\\shixun\\aimodel\\report\\te_ball_detect_pose_detect_report.md',5),(17,'F:\\download\\shixun\\aimodel\\report\\test2.mp4_ball_detect_pose_detect_report.md',10);
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result` (
  `result_id` int NOT NULL AUTO_INCREMENT,
  `video_id` int DEFAULT NULL,
  `ball_json_path` varchar(100) DEFAULT NULL,
  `pose_json_path` varchar(100) DEFAULT NULL,
  `ball_video_path` varchar(100) DEFAULT NULL,
  `pose_video_path` varchar(100) DEFAULT NULL,
  `segment_json_path` varchar(100) DEFAULT NULL,
  `annotated_video_path` varchar(100) DEFAULT NULL,
  `recognition_json_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`result_id`),
  UNIQUE KEY `result_id_UNIQUE` (`result_id`),
  KEY `video_idx` (`video_id`),
  CONSTRAINT `fk_result_video` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result`
--

LOCK TABLES `result` WRITE;
/*!40000 ALTER TABLE `result` DISABLE KEYS */;
INSERT INTO `result` VALUES (1,5,'F:\\download\\shixun\\aimodel\\json\\test_ball_detect.json','F:\\download\\shixun\\aimodel\\json\\test_ball_detect_pose_detect.json','F:\\download\\shixun\\aimodel\\video_output\\test_ball_detect.mp4','F:\\download\\shixun\\aimodel\\video_output\\test_ball_detect_pose_detect.mp4','F:\\download\\shixun\\aimodel\\json\\test_ball_detect_segments.json','F:\\download\\shixun\\aimodel\\video_output\\test_action.mp4','F:\\download\\shixun\\aimodel\\json\\test_action.json'),(4,7,'F:\\download\\shixun\\aimodel\\json\\test2_ball_detect.json','F:\\download\\shixun\\aimodel\\json\\test2_ball_detect_pose_detect.json','F:\\download\\shixun\\aimodel\\video_output\\test2_ball_detect.mp4','F:\\download\\shixun\\aimodel\\video_output\\test2_ball_detect_pose_detect.mp4','F:\\download\\shixun\\aimodel\\json\\test2_ball_detect_segments.json','F:\\download\\shixun\\aimodel\\video_output\\test2_ball_detect_pose_detect_action.mp4','F:\\download\\shixun\\aimodel\\json\\test2_ball_detect_pose_detect_action.json'),(5,15,'F:\\download\\shixun\\aimodel\\json\\te_ball_detect.json','F:\\download\\shixun\\aimodel\\json\\te_ball_detect_pose_detect.json','F:\\download\\shixun\\aimodel\\video_output\\te_ball_detect.mp4','F:\\download\\shixun\\aimodel\\video_output\\te_ball_detect_pose_detect.mp4','F:\\download\\shixun\\aimodel\\json\\te_ball_detect_segments.json','F:\\download\\shixun\\aimodel\\video_output\\te_ball_detect_pose_detect_action.mp4','F:\\download\\shixun\\aimodel\\json\\te_ball_detect_pose_detect_action.json'),(9,23,'F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect.json','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_pose_detect.json','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect.mp4','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect_pose_detect.mp4','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_segments.json','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect_pose_detect_action.mp4','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_pose_detect_action.json'),(10,24,'F:\\download\\shixun\\aimodel\\json\\test2.mp4_ball_detect.json','F:\\download\\shixun\\aimodel\\json\\test2.mp4_ball_detect_pose_detect.json','F:\\download\\shixun\\aimodel\\video_output\\test2.mp4_ball_detect.mp4','F:\\download\\shixun\\aimodel\\video_output\\test2.mp4_ball_detect_pose_detect.mp4','F:\\download\\shixun\\aimodel\\json\\test2.mp4_ball_detect_segments.json','F:\\download\\shixun\\aimodel\\video_output\\test2.mp4_ball_detect_pose_detect_action.mp4','F:\\download\\shixun\\aimodel\\json\\test2.mp4_ball_detect_pose_detect_action.json'),(11,23,'F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect.json','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_pose_detect.json','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect.mp4','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect_pose_detect.mp4','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_segments.json','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect_pose_detect_action.mp4','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_pose_detect_action.json'),(12,23,'F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect.json','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_pose_detect.json','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect.mp4','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect_pose_detect.mp4','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_segments.json','F:\\download\\shixun\\aimodel\\video_output\\test.mp4_ball_detect_pose_detect_action.mp4','F:\\download\\shixun\\aimodel\\json\\test.mp4_ball_detect_pose_detect_action.json');
/*!40000 ALTER TABLE `result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `account` char(11) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `nickname` varchar(45) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `register_time` datetime DEFAULT NULL,
  `sex` tinyint DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `note` text,
  `height` float DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `birth` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `id_UNIQUE` (`user_id`),
  UNIQUE KEY `account_UNIQUE` (`account`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (4,'19955535073','scrypt:32768:8:1$WumHZ3HLXaq5E5C4$a9c162e11423bb54d3e83fb6bbb8e9a19f7c9a6f14943edd3950064598c680ed47a91b935e021631652e34f22aab8b91616decff1cab4fe8d549a1d69f95de7d','wky','','2025-07-01 10:35:46',1,'2914251540@qq.com',NULL,NULL,NULL,NULL,NULL),(6,'12345678910','scrypt:32768:8:1$Cdo1uMGxOtfBWgNK$428f564b915ada973f47399dd4b8d4e516b09bd82854a3ca2c638b793fd8cece48f5316d63114edcfb2f07ef3373cdea0747d1c7028431c4ae17b17fa2627c0c','sps','F:\\download\\shixun\\avatar\\证件照原图.jpg','2025-07-01 10:47:40',1,'822684749@qq.com','修改成功',180,90,'重庆',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `video` (
  `video_id` int NOT NULL AUTO_INCREMENT,
  `video_path` varchar(100) DEFAULT NULL,
  `video_name` varchar(45) DEFAULT NULL,
  `video_size` varchar(45) DEFAULT NULL,
  `video_duration` varchar(45) DEFAULT NULL,
  `video_format` varchar(45) DEFAULT NULL,
  `video_resolution` varchar(45) DEFAULT NULL,
  `video_frame_rate` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`video_id`),
  UNIQUE KEY `video_id_UNIQUE` (`video_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video`
--

LOCK TABLES `video` WRITE;
/*!40000 ALTER TABLE `video` DISABLE KEYS */;
INSERT INTO `video` VALUES (1,'E:/rail2.mp4','first','391.4MB','0:03:14','MP4','2560x1440',27.08),(2,'E:/star_rail.mp4','test1','20.61MB','0:00:09','MP4','2560x1440',26.98),(3,'E:/star_rail.mp4','third','20.61MB','0:00:09','MP4','2560x1440',26.98),(4,'E:/rail2.mp4','fourth','391.4MB','0:03:14','MP4','2560x1440',27.08),(5,'F:/download/shixun/aimodel/video/test.mp4','test','2.83MB','0:00:01','MP4','1920x1080',25.00),(7,'F:/download/test2.mp4','test2','2.83MB','0:00:01','MP4','1920x1080',25.00),(8,'F:\\download\\shixun\\aimodel\\video\\testupload','testupload','2964628','0:00:01','','1920x1080',25.00),(9,'F:\\download\\shixun\\aimodel\\video\\testupload.mp4','testupload.mp4','2964628','0:00:01','MP4','1920x1080',25.00),(10,'F:\\download\\shixun\\aimodel\\video\\test_1','test_1','2964628','0:00:01','','1920x1080',25.00),(11,'F:\\download\\shixun\\aimodel\\video\\test_1\\.mp4','test_1','2964628','0:00:01','','1920x1080',25.00),(12,'F:\\download\\shixun\\aimodel\\video\\test_1.mp4','test_1','2964628','0:00:01','MP4','1920x1080',25.00),(13,'F:\\download\\shixun\\aimodel\\video\\test_2.mp4','test_2','2964628','0:00:01','MP4','1920x1080',25.00),(14,'F:\\download\\shixun\\aimodel\\video\\2025-06-15-15-31-42.mp4.mp4','2025-06-15-15-31-42.mp4','15082670','0:00:32','MP4','1920x1080',25.03),(15,'F:\\download\\shixun\\aimodel\\video\\te.mp4','te','2964628','0:00:01','MP4','1920x1080',25.00),(18,'F:\\download\\shixun\\aimodel\\video\\2025-06-15-15-31-42.mp4.mp4','2025-06-15-15-31-42.mp4','15082670','0:00:32','MP4','1920x1080',25.03),(19,'F:\\download\\shixun\\aimodel\\video\\test.mp4.mp4','test.mp4','2964628','0:00:01','MP4','1920x1080',25.00),(20,'F:\\download\\shixun\\aimodel\\video\\test2.mp4.mp4','test2.mp4','2964628','0:00:01','MP4','1920x1080',25.00),(21,'F:\\download\\shixun\\aimodel\\video\\test_2.mp4.mp4','test_2.mp4','2964628','0:00:01','MP4','1920x1080',25.00),(22,'F:\\download\\shixun\\aimodel\\video\\test2.mp4.mp4','test2.mp4','2964628','0:00:01','MP4','1920x1080',25.00),(23,'F:\\download\\shixun\\aimodel\\video\\test.mp4.mp4','test.mp4','2964628','0:00:01','MP4','1920x1080',25.00),(24,'F:\\download\\shixun\\aimodel\\video\\test2.mp4.mp4','test2.mp4','2964628','0:00:01','MP4','1920x1080',25.00),(25,'F:\\download\\shixun\\aimodel\\video\\2025-06-15-15-31-42.mp4.mp4','2025-06-15-15-31-42.mp4','15082670','0:00:32','MP4','1920x1080',25.03);
/*!40000 ALTER TABLE `video` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-09 20:25:20
