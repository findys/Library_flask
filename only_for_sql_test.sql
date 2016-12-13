-- phpMyAdmin SQL Dump
-- version 4.0.10.11
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2016-12-11 04:24:23
-- 服务器版本: 5.5.21-log
-- PHP 版本: 5.4.45

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `Sql_Class`
--

-- --------------------------------------------------------

--
-- 表的结构 `books`
--

CREATE TABLE IF NOT EXISTS `books` (
  `Book_id` varchar(255) NOT NULL,
  `book_name` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `publishing` varchar(255) DEFAULT NULL,
  `Category_id` varchar(255) DEFAULT NULL,
  `price` decimal(19,4) DEFAULT NULL,
  `Date_in` datetime DEFAULT NULL,
  `Quanity_in` int(11) DEFAULT NULL,
  `Quanity_out` int(11) DEFAULT NULL,
  `Quanity_loss` int(11) DEFAULT NULL,
  PRIMARY KEY (`Book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `books`
--

INSERT INTO `books` (`Book_id`, `book_name`, `author`, `publishing`, `Category_id`, `price`, `Date_in`, `Quanity_in`, `Quanity_out`, `Quanity_loss`) VALUES
('b001', '并行计算', '王一', '北京大学出版社', 'ca01', 21.0000, '2010-03-07 00:00:00', 10, 3, 0),
('b002', '建筑艺术', '李白', '清华大学出版社', 'ca06', 40.0000, '2010-05-17 00:00:00', 8, 2, 0),
('b003', '神奇的科学', '刘力', '清华大学出版社', 'ca04', 18.0000, '2009-12-09 00:00:00', 5, 0, 1),
('b004', '网络原理', '张扬', '邮电出版社', 'ca05', 38.0000, '2010-02-23 00:00:00', 1, 1, 0),
('b005', '肺病防治', '李小明', '人民卫生出版社', 'ca03', 16.0000, '2009-04-05 00:00:00', 5, 0, 0),
('b006', '养殖技术', '王平', '中国农业出版社', 'ca02', 11.0000, '2010-08-01 00:00:00', 3, 1, 0),
('b007', '分布式系统', '陈东', '武汉大学出版社', 'ca01', 32.0000, '2010-06-13 00:00:00', 8, 0, 1),
('b520', 'i', 'love', 'jsl', 'ca04', 520.0000, '2016-12-07 17:02:00', 520, 0, 0),
('b521', 'test', 'test', 'test', 'ca04', 520.0000, '2016-12-07 17:02:00', 520, 0, 0),
('b522', '平凡的世界', 'test', 'test', 'ca04', 520.0000, '2016-12-07 17:02:00', 520, 0, 0);

-- --------------------------------------------------------

--
-- 表的结构 `borrow`
--

CREATE TABLE IF NOT EXISTS `borrow` (
  `Reader_id` varchar(255) NOT NULL,
  `Book_id` varchar(255) NOT NULL,
  `Date_borrow` datetime DEFAULT NULL,
  `Date_return` datetime DEFAULT NULL,
  `loss` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Reader_id`,`Book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `borrow`
--

INSERT INTO `borrow` (`Reader_id`, `Book_id`, `Date_borrow`, `Date_return`, `loss`) VALUES
('r001', 'b001', '2016-09-02 00:00:00', '2016-09-02 00:00:00', '否'),
('r001', 'b002', '2016-08-02 00:00:00', '2016-09-02 00:00:00', '否'),
('r001', 'b003', '2010-05-17 00:00:00', NULL, '是'),
('r001', 'b006', '2010-05-17 00:00:00', '2011-05-17 00:00:00', '否'),
('r001', 'b007', '2010-05-17 00:00:00', NULL, '否'),
('r002', 'b001', '2010-05-17 00:00:00', '2011-06-17 00:00:00', '否'),
('r004', 'b001', '2015-11-02 00:00:00', '2015-11-02 00:00:00', '否'),
('r004', 'b002', '2016-08-10 00:00:00', '2016-09-10 00:00:00', '否'),
('r004', 'b006', '2015-08-10 00:00:00', '2015-09-10 00:00:00', '否'),
('r006', 'b001', '2016-08-10 00:00:00', '2016-09-10 00:00:00', '否'),
('r006', 'b004', '2016-06-24 00:00:00', '2016-08-24 00:00:00', '否');

-- --------------------------------------------------------

--
-- 表的结构 `b_category`
--

CREATE TABLE IF NOT EXISTS `b_category` (
  `category_id` varchar(255) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `b_category`
--

INSERT INTO `b_category` (`category_id`, `category`) VALUES
('ca01', '计算机'),
('ca02', '农学'),
('ca03', '医学'),
('ca04', '科普'),
('ca05', '通讯'),
('ca06', '建筑');

-- --------------------------------------------------------

--
-- 表的结构 `loss_reporting`
--

CREATE TABLE IF NOT EXISTS `loss_reporting` (
  `Reader_id` varchar(255) NOT NULL,
  `Loss_date` datetime DEFAULT NULL,
  PRIMARY KEY (`Reader_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `loss_reporting`
--

INSERT INTO `loss_reporting` (`Reader_id`, `Loss_date`) VALUES
('r001', '0000-00-00 00:00:00'),
('r005', '2016-09-01 00:00:00');

-- --------------------------------------------------------

--
-- 表的结构 `member_level`
--

CREATE TABLE IF NOT EXISTS `member_level` (
  `level` varchar(255) NOT NULL,
  `days` int(11) DEFAULT NULL,
  `numbers` int(11) DEFAULT NULL,
  `fee` int(11) DEFAULT NULL,
  PRIMARY KEY (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `member_level`
--

INSERT INTO `member_level` (`level`, `days`, `numbers`, `fee`) VALUES
('普通', 30, 2, 10),
('金卡', 90, 5, 100),
('银卡', 60, 3, 50);

-- --------------------------------------------------------

--
-- 表的结构 `readers`
--

CREATE TABLE IF NOT EXISTS `readers` (
  `Reader_id` varchar(255) NOT NULL,
  `reader_name` varchar(255) DEFAULT NULL,
  `sex` varchar(255) DEFAULT NULL,
  `birthday` datetime DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `card_name` varchar(255) DEFAULT NULL,
  `Card_id` varchar(255) DEFAULT NULL,
  `level` varchar(255) DEFAULT NULL,
  `day` datetime DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Reader_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `readers`
--

INSERT INTO `readers` (`Reader_id`, `reader_name`, `sex`, `birthday`, `phone`, `mobile`, `card_name`, `Card_id`, `level`, `day`, `password`) VALUES
('admin', NULL, NULL, NULL, 123456, NULL, NULL, NULL, NULL, NULL, 'nimda'),
('r001', '李红', '女', '1988-03-08 00:00:00', 62127790, '13671100110', '身份证', ' 230106198803070178', '金卡', '2012-08-01 00:00:00', 'r001'),
('r002', '刘晓', '男', '1998-08-09 00:00:00', 84778123, '13671007896', '身份证', '210103199008094326', '普通', '2011-08-01 00:00:00', '1'),
('r003', '张英', '女', '2001-02-21 00:00:00', 84900581, '13901020111', '身份证', '230106200102216634', '普通', '2010-08-01 00:00:00', '1'),
('r004', '张刚', '男', '1970-11-12 00:00:00', 51681212, '13812669002', '身份证', '230106197011120145', '金卡', '2010-06-20 00:00:00', '1'),
('r005', '刘静', '女', '1999-10-07 00:00:00', 51681213, '13756705671', '身份证', '230106199910070766', '普通', '2009-04-05 00:00:00', '1'),
('r006', '王成林', '男', '1990-05-18 00:00:00', 82161100, '13683304305', '身份证', '230106199005180842', '银卡', '2010-08-01 00:00:00', '1'),
('r007', '徐晨', '男', '2001-09-24 00:00:00', 82190703, '13901229706', '身份证', '230106200109247092', '普通', '2010-05-15 00:00:00', '1'),
('r008', '范晓天', '女', '1998-08-25 00:00:00', 62220506, '15851327667', '身份证', '230106199808258261', '普通', '2008-12-20 00:00:00', '1'),
('r009', '姜武', '男', '1997-07-09 00:00:00', 62220712, '15810034321', '身份证', '230106199707095578', '普通', '2013-08-01 00:00:00', '1'),
('r520', '颜硕', '男', '1995-03-28 00:00:00', 9999999, '18801307030', '身份证', '999999999999999999', '金卡', '2016-12-10 00:00:00', '520'),
('r521', '李炀', '男', '1995-03-20 00:00:00', 12345678, '12345678912', '身份证', '222222222222222222', '普通', '2016-12-10 23:00:00', '222');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
