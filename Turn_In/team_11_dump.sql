-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: team_11
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book` (
  `isbn` varchar(20) NOT NULL,
  `subject` varchar(11) DEFAULT NULL,
  `title` varchar(32) DEFAULT NULL,
  `publisher` varchar(32) DEFAULT NULL,
  `author` varchar(32) DEFAULT NULL,
  `description` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES ('10823','Farming','Pears','Statefarm','Luan Kipper','How to grow pears'),('111111','Mathematics','Calc 2','Case','Chris','What'),('112233','Math','Calc 1','Cengage','Tom','An introduction to calculus'),('12','12','12','12','1212','12'),('123','Farming','Ice','Penguin','Gary','ice fishing'),('1234','Calc','Run Time vs Number of Threads','New York','Strang','asdf'),('222222','Math','Calc 1','Cengage','Tom','No'),('2332432432','cs','computers','yahoo','Jeremy','test'),('2343','Farming','Milking For Dummies','Farmhouse','Luke','how to milk well'),('340412930','CS','Databases for Dummies','Penguin','Jeremy','Good book'),('4444','Science','Cheerios','Honey','Bee','Bee Book'),('7804230897','Comp Sci','Google','Larry','Timmothy','Email'),('89732','Math','Red Book','Penguin','Cleveland','Red'),('982374234249132','Math','Calc 4','Penguin','Strangi','Clac 4 tb'),('98765432','Farming','Blue Bell','Farmhouse','Linny','Blue bell ice');
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listing`
--

DROP TABLE IF EXISTS `listing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `listing` (
  `listing_id` int(11) NOT NULL AUTO_INCREMENT,
  `price` varchar(11) DEFAULT NULL,
  `listing_status` varchar(11) DEFAULT NULL,
  `listing_condition` varchar(32) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `order_basket_id` int(11) DEFAULT NULL,
  `book_isbn` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`listing_id`),
  KEY `order_basket_id` (`order_basket_id`),
  KEY `book_isbn` (`book_isbn`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `listing_ibfk_1` FOREIGN KEY (`order_basket_id`) REFERENCES `order_basket` (`order_basket_id`),
  CONSTRAINT `listing_ibfk_2` FOREIGN KEY (`book_isbn`) REFERENCES `book` (`isbn`),
  CONSTRAINT `listing_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing`
--

LOCK TABLES `listing` WRITE;
/*!40000 ALTER TABLE `listing` DISABLE KEYS */;
INSERT INTO `listing` VALUES (25,'10','SOLD','New',20,NULL,'2332432432'),(26,'7.89','SELLING','Used - Acceptable',21,NULL,'112233'),(27,'100','SELLING','Used - Like New',21,NULL,'112233'),(28,'32','SELLING','Used - Very Good',21,NULL,'4444'),(29,'50.00','SELLING','Used - Good',15,NULL,'10823'),(30,'52','SELLING','Used - Like New',15,NULL,'112233'),(31,'46','SOLD','Used - Very Good',20,NULL,'4444');
/*!40000 ALTER TABLE `listing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_basket`
--

DROP TABLE IF EXISTS `order_basket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_basket` (
  `order_basket_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `address` varchar(32) DEFAULT NULL,
  `order_basket_status` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`order_basket_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `order_basket_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=149888 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_basket`
--

LOCK TABLES `order_basket` WRITE;
/*!40000 ALTER TABLE `order_basket` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_basket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(11) NOT NULL,
  `userpassword` varchar(11) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (15,'Bertram','coco'),(20,'ssd','1321'),(21,'greg','password');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-01 22:03:13
