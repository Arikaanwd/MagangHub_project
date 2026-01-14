/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : sper_db

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2026-01-10 05:12:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `master_jenis_aset`
-- ----------------------------
DROP TABLE IF EXISTS `master_jenis_aset`;
CREATE TABLE `master_jenis_aset` (
  `id_jenis_aset` int(11) NOT NULL AUTO_INCREMENT,
  `kode_aset` varchar(10) DEFAULT NULL,
  `nama_aset` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_jenis_aset`),
  UNIQUE KEY `kode_aset` (`kode_aset`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of master_jenis_aset
-- ----------------------------
INSERT INTO `master_jenis_aset` VALUES ('1', 'RK', 'Kantor');
INSERT INTO `master_jenis_aset` VALUES ('2', 'RD', 'Rumah Dinas');
INSERT INTO `master_jenis_aset` VALUES ('3', 'MM', 'Mess Menanggal');
INSERT INTO `master_jenis_aset` VALUES ('4', 'LH', 'Lahan');
INSERT INTO `master_jenis_aset` VALUES ('5', 'PK', 'Kontainer');

-- ----------------------------
-- Table structure for `master_kantor`
-- ----------------------------
DROP TABLE IF EXISTS `master_kantor`;
CREATE TABLE `master_kantor` (
  `id_kantor` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_jenis_aset` int(11) NOT NULL,
  `kode_kantor` varchar(10) NOT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `status_aset` enum('Kosong','Disewa','Internal','Perbaikan','Tidak Aktif') DEFAULT 'Kosong',
  `keterangan` varchar(50) NOT NULL,
  PRIMARY KEY (`id_kantor`),
  UNIQUE KEY `kode_kantor` (`kode_kantor`),
  KEY `id_jenis_aset` (`id_jenis_aset`),
  CONSTRAINT `master_kantor_ibfk_1` FOREIGN KEY (`id_jenis_aset`) REFERENCES `master_jenis_aset` (`id_jenis_aset`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of master_kantor
-- ----------------------------
INSERT INTO `master_kantor` VALUES ('1', '1', 'RK-A01', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('2', '1', 'RK-A02', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('3', '1', 'RK-A03', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('4', '1', 'RK-A04', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('5', '1', 'RK-A05', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('6', '1', 'RK-A06', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('7', '1', 'RK-A07', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('8', '1', 'RK-A08', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('9', '1', 'RK-A09', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('10', '1', 'RK-A10', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('11', '1', 'RK-A11', 'Gedung Ex-Kamtib', 'Internal', '');
INSERT INTO `master_kantor` VALUES ('12', '1', 'RK-A12', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('13', '1', 'RK-A13', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('14', '1', 'RK-A14', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('15', '1', 'RK-A15', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('16', '1', 'RK-A16', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('17', '1', 'RK-A17', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('18', '1', 'RK-A18', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('19', '1', 'RK-A19', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('20', '1', 'RK-A20', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('21', '1', 'RK-A21', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('22', '1', 'RK-A22', 'Gedung Ex-Kamtib', 'Internal', '');
INSERT INTO `master_kantor` VALUES ('23', '1', 'RK-A23', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('24', '1', 'RK-A24', 'Gedung Ex-Kamtib', 'Internal', '');
INSERT INTO `master_kantor` VALUES ('25', '1', 'RK-A25', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('26', '1', 'RK-A26', 'Gedung Ex-Kamtib', 'Internal', '');
INSERT INTO `master_kantor` VALUES ('27', '1', 'RK-A27', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('28', '1', 'RK-A28', 'Gedung Ex-Kamtib', 'Internal', '');
INSERT INTO `master_kantor` VALUES ('29', '1', 'RK-B01', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('30', '1', 'RK-B02', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('31', '1', 'RK-B03', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('32', '1', 'RK-B04', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('33', '1', 'RK-B05', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('34', '1', 'RK-B06', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('35', '1', 'RK-B07', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('36', '1', 'RK-B08', 'Gedung Ex-Kamtib', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('37', '1', 'RK-01', 'PIP Lt. Dasar', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('38', '1', 'RK-02', 'Gedung Div. Desain', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('39', '1', 'RK-03', 'Gedung Div. Marketing', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('40', '1', 'RK-04', 'Area Gedung Div. Harkan', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('41', '1', 'RK-05', 'Area Gedung Div. Harkan', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('42', '1', 'RK-06', 'Gedung Bengkel RH-06 Div. Harkan', 'Disewa', '');
INSERT INTO `master_kantor` VALUES ('43', '1', 'RK-07', 'Gedung Ex-Pen. Material Ruang A', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('44', '1', 'RK-08', 'Gedung Ex-Pen. Material Ruang B', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('45', '1', 'RK-09', 'Gedung Ex-Pen. Material Ruang C', 'Kosong', '');
INSERT INTO `master_kantor` VALUES ('46', '1', 'RK-10', 'Gedung Ex-Pen. Material Ruang D', 'Internal', '');
INSERT INTO `master_kantor` VALUES ('47', '1', 'RK-11', 'Gedung Kesind', 'Kosong', 'Anak Perusahaan');
INSERT INTO `master_kantor` VALUES ('48', '1', 'RK-12', 'Gedung Kesind', 'Kosong', 'Anak Perusahaan');
INSERT INTO `master_kantor` VALUES ('49', '1', 'RK-13', 'Gedung Kesind', 'Kosong', 'Anak Perusahaan');
INSERT INTO `master_kantor` VALUES ('50', '1', 'RK-14', 'Gedung Kesind', 'Kosong', 'Anak Perusahaan');
INSERT INTO `master_kantor` VALUES ('51', '1', 'RK-15', 'Gedung Kesind', 'Internal', 'Anak Perusahaan');
INSERT INTO `master_kantor` VALUES ('52', '1', 'RK-16', 'Gedung KOP KB', 'Kosong', 'Anak Perusahaan');
INSERT INTO `master_kantor` VALUES ('53', '1', 'RK-17', 'Gedung Kantin', 'Internal', 'Anak Perusahaan');
INSERT INTO `master_kantor` VALUES ('54', '1', 'RK-18', 'Gedung Div. GE', 'Kosong', 'bengkel');

-- ----------------------------
-- Table structure for `master_kontainer`
-- ----------------------------
DROP TABLE IF EXISTS `master_kontainer`;
CREATE TABLE `master_kontainer` (
  `id_kontainer` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_jenis_aset` int(11) NOT NULL,
  `kode_kontainer` varchar(10) NOT NULL,
  `volume_feet` int(11) DEFAULT NULL,
  `luas_m2` decimal(10,2) DEFAULT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `unit_milik` varchar(100) DEFAULT NULL,
  `status_aset` enum('Kosong','Disewa','Internal','Tidak Aktif','Perbaikan') NOT NULL DEFAULT 'Kosong',
  PRIMARY KEY (`id_kontainer`),
  UNIQUE KEY `kode_kontainer` (`kode_kontainer`) USING BTREE,
  KEY `id_jenis_aset` (`id_jenis_aset`),
  CONSTRAINT `master_kontainer_ibfk_1` FOREIGN KEY (`id_jenis_aset`) REFERENCES `master_jenis_aset` (`id_jenis_aset`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of master_kontainer
-- ----------------------------
INSERT INTO `master_kontainer` VALUES ('2', '5', 'PK-01', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('4', '5', 'PK-02A', '20', '14.40', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('5', '5', 'PK-03', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Disewa');
INSERT INTO `master_kontainer` VALUES ('6', '5', 'PK-04', '20', '14.40', 'BBS2', 'Pihak 2', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('7', '5', 'PK-05', '20', '14.40', 'BBS2', 'Pihak 2', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('8', '5', 'PK-06', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Disewa');
INSERT INTO `master_kontainer` VALUES ('9', '5', 'PK-07', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('10', '5', 'PK-08', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('11', '5', 'PK-09', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('12', '5', 'PK-10', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('13', '5', 'PK-11', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('14', '5', 'PK-12', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('15', '5', 'PK-13', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('16', '5', 'PK-02B', '20', '14.40', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('17', '5', 'PK-14B', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('18', '5', 'PK-15', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('19', '5', 'PK-16', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('20', '5', 'PK-17', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('21', '5', 'PK-18', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('22', '5', 'PK-19', '40', '28.80', 'Dok. Beluga', 'Pihak 2', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('23', '5', 'PK-20A', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('24', '5', 'PK-21', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('25', '5', 'PK-22', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('26', '5', 'PK-23', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('27', '5', 'PK-24', '20', '14.40', 'Dok. Beluga', 'Pihak 2', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('28', '5', 'PK-25', '20', '14.40', 'Dok. Beluga', 'Pihak 2', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('29', '5', 'PK-26', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('30', '5', 'PK-27', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('31', '5', 'PK-28', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('32', '5', 'PK-29', '40', '28.80', 'Dok. Beluga', 'Pihak 2', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('33', '5', 'PK-30', '40', '28.80', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('34', '5', 'PK-31A', '20', '14.40', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('35', '5', 'PK-31B', '20', '14.40', 'Div. Kapal Niaga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('36', '5', 'PK-14A', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('37', '5', 'PK-32', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('38', '5', 'PK-33', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('39', '5', 'PK-34', '20', '14.40', 'Dok. Beluga', 'Pihak 2', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('40', '5', 'PK-35', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('41', '5', 'PK-36', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('42', '5', 'PK-37', '40', '28.80', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('43', '5', 'PK-20B', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');
INSERT INTO `master_kontainer` VALUES ('44', '5', 'PK-38', '20', '14.40', 'Dok. Beluga', 'PT PAL', 'Kosong');

-- ----------------------------
-- Table structure for `master_lahan`
-- ----------------------------
DROP TABLE IF EXISTS `master_lahan`;
CREATE TABLE `master_lahan` (
  `id_lahan` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_jenis_aset` int(11) NOT NULL,
  `kode_lahan` varchar(20) NOT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `status_aset` enum('Kosong','Disewa','Perbaikan','Internal','Tidak Aktif') DEFAULT 'Kosong',
  PRIMARY KEY (`id_lahan`),
  UNIQUE KEY `kode_lahan` (`kode_lahan`),
  KEY `id_jenis_aset` (`id_jenis_aset`),
  CONSTRAINT `master_lahan_ibfk_1` FOREIGN KEY (`id_jenis_aset`) REFERENCES `master_jenis_aset` (`id_jenis_aset`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of master_lahan
-- ----------------------------
INSERT INTO `master_lahan` VALUES ('1', '4', 'LH-01', 'Gedung KPM', 'Disewa');
INSERT INTO `master_lahan` VALUES ('2', '4', 'LH-ATM01', 'ATM BNI', 'Disewa');
INSERT INTO `master_lahan` VALUES ('3', '4', 'LH-ATM02', 'ATM BRI', 'Kosong');
INSERT INTO `master_lahan` VALUES ('4', '4', 'LH-ATM03', 'ATM Mandiri', 'Kosong');
INSERT INTO `master_lahan` VALUES ('5', '4', 'LH-ATM04', 'ATM BSI', 'Disewa');
INSERT INTO `master_lahan` VALUES ('6', '4', 'LH-02', 'Area Kapal Selam', 'Kosong');
INSERT INTO `master_lahan` VALUES ('7', '4', 'LH-03', 'Gedung GSG', 'Kosong');

-- ----------------------------
-- Table structure for `master_mess`
-- ----------------------------
DROP TABLE IF EXISTS `master_mess`;
CREATE TABLE `master_mess` (
  `id_mess` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_jenis_aset` int(11) NOT NULL,
  `kode_mess` varchar(20) NOT NULL,
  `blok` char(5) DEFAULT NULL,
  `status_aset` enum('Kosong','Disewa','Internal','Perbaikan','Tidak Aktif') DEFAULT 'Kosong',
  PRIMARY KEY (`id_mess`),
  UNIQUE KEY `kode_mess` (`kode_mess`),
  KEY `id_jenis_aset` (`id_jenis_aset`),
  CONSTRAINT `master_mess_ibfk_1` FOREIGN KEY (`id_jenis_aset`) REFERENCES `master_jenis_aset` (`id_jenis_aset`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of master_mess
-- ----------------------------
INSERT INTO `master_mess` VALUES ('1', '3', 'MM-01', 'A', 'Kosong');
INSERT INTO `master_mess` VALUES ('2', '3', 'MM-02', 'B', 'Kosong');
INSERT INTO `master_mess` VALUES ('3', '3', 'MM-03', 'C', 'Kosong');
INSERT INTO `master_mess` VALUES ('4', '3', 'MM-04', 'D', 'Kosong');
INSERT INTO `master_mess` VALUES ('5', '3', 'MM-05', 'E', 'Kosong');
INSERT INTO `master_mess` VALUES ('6', '3', 'MM-06', 'F', 'Kosong');
INSERT INTO `master_mess` VALUES ('7', '3', 'MM-07', 'G', 'Kosong');
INSERT INTO `master_mess` VALUES ('8', '3', 'MM-08', 'H', 'Kosong');
INSERT INTO `master_mess` VALUES ('9', '3', 'MM-09', 'AA', 'Kosong');
INSERT INTO `master_mess` VALUES ('10', '3', 'MM-10', 'BB', 'Kosong');
INSERT INTO `master_mess` VALUES ('11', '3', 'MM-11', 'CC', 'Kosong');
INSERT INTO `master_mess` VALUES ('12', '3', 'MM-12', 'DD', 'Kosong');
INSERT INTO `master_mess` VALUES ('13', '3', 'MM-13', 'EE', 'Kosong');
INSERT INTO `master_mess` VALUES ('14', '3', 'MM-14', 'FF', 'Kosong');
INSERT INTO `master_mess` VALUES ('15', '3', 'MM-15', 'GG', 'Kosong');
INSERT INTO `master_mess` VALUES ('16', '3', 'MM-16', 'HH', 'Kosong');
INSERT INTO `master_mess` VALUES ('17', '3', 'MM-17', 'A1', 'Kosong');
INSERT INTO `master_mess` VALUES ('18', '3', 'MM-18', 'B1', 'Kosong');
INSERT INTO `master_mess` VALUES ('19', '3', 'MM-19', 'C1', 'Kosong');
INSERT INTO `master_mess` VALUES ('20', '3', 'MM-20', 'D1', 'Kosong');
INSERT INTO `master_mess` VALUES ('21', '3', 'MM-21', 'E1', 'Kosong');
INSERT INTO `master_mess` VALUES ('22', '3', 'MM-22', 'F1', 'Kosong');
INSERT INTO `master_mess` VALUES ('23', '3', 'MM-23', 'G1', 'Kosong');
INSERT INTO `master_mess` VALUES ('24', '3', 'MM-24', 'H1', 'Kosong');
INSERT INTO `master_mess` VALUES ('25', '3', 'MM-25', 'AA1', 'Kosong');
INSERT INTO `master_mess` VALUES ('26', '3', 'MM-26', 'BB1', 'Kosong');
INSERT INTO `master_mess` VALUES ('27', '3', 'MM-27', 'CC1', 'Kosong');
INSERT INTO `master_mess` VALUES ('28', '3', 'MM-28', 'DD1', 'Kosong');
INSERT INTO `master_mess` VALUES ('29', '3', 'MM-29', 'EE1', 'Kosong');
INSERT INTO `master_mess` VALUES ('30', '3', 'MM-30', 'FF1', 'Kosong');
INSERT INTO `master_mess` VALUES ('31', '3', 'MM-31', 'GG1', 'Kosong');
INSERT INTO `master_mess` VALUES ('32', '3', 'MM-32', 'HH1', 'Kosong');
INSERT INTO `master_mess` VALUES ('33', '3', 'MM-33', 'A2', 'Kosong');
INSERT INTO `master_mess` VALUES ('34', '3', 'MM-34', 'B2', 'Kosong');
INSERT INTO `master_mess` VALUES ('35', '3', 'MM-35', 'C2', 'Kosong');
INSERT INTO `master_mess` VALUES ('36', '3', 'MM-36', 'D2', 'Kosong');
INSERT INTO `master_mess` VALUES ('37', '3', 'MM-37', 'E2', 'Kosong');
INSERT INTO `master_mess` VALUES ('38', '3', 'MM-38', 'F2', 'Kosong');
INSERT INTO `master_mess` VALUES ('39', '3', 'MM-39', 'G2', 'Kosong');
INSERT INTO `master_mess` VALUES ('40', '3', 'MM-40', 'H2', 'Kosong');
INSERT INTO `master_mess` VALUES ('41', '3', 'MM-41', 'AA2', 'Kosong');
INSERT INTO `master_mess` VALUES ('42', '3', 'MM-42', 'BB2', 'Kosong');
INSERT INTO `master_mess` VALUES ('43', '3', 'MM-43', 'CC2', 'Kosong');
INSERT INTO `master_mess` VALUES ('44', '3', 'MM-44', 'DD2', 'Kosong');
INSERT INTO `master_mess` VALUES ('45', '3', 'MM-45', 'EE2', 'Kosong');
INSERT INTO `master_mess` VALUES ('46', '3', 'MM-46', 'FF2', 'Kosong');
INSERT INTO `master_mess` VALUES ('47', '3', 'MM-47', 'GG2', 'Kosong');
INSERT INTO `master_mess` VALUES ('48', '3', 'MM-48', 'HH2', 'Kosong');
INSERT INTO `master_mess` VALUES ('49', '3', 'MM-49', 'A3', 'Kosong');
INSERT INTO `master_mess` VALUES ('50', '3', 'MM-50', 'B3', 'Kosong');
INSERT INTO `master_mess` VALUES ('51', '3', 'MM-51', 'C3', 'Kosong');
INSERT INTO `master_mess` VALUES ('52', '3', 'MM-52', 'D3', 'Kosong');
INSERT INTO `master_mess` VALUES ('53', '3', 'MM-53', 'E3', 'Kosong');
INSERT INTO `master_mess` VALUES ('54', '3', 'MM-54', 'F3', 'Kosong');
INSERT INTO `master_mess` VALUES ('55', '3', 'MM-55', 'G3', 'Kosong');
INSERT INTO `master_mess` VALUES ('56', '3', 'MM-56', 'H3', 'Perbaikan');
INSERT INTO `master_mess` VALUES ('57', '3', 'MM-57', 'AA3', 'Kosong');
INSERT INTO `master_mess` VALUES ('58', '3', 'MM-58', 'BB3', 'Kosong');
INSERT INTO `master_mess` VALUES ('59', '3', 'MM-59', 'CC3', 'Kosong');
INSERT INTO `master_mess` VALUES ('60', '3', 'MM-60', 'DD3', 'Kosong');
INSERT INTO `master_mess` VALUES ('61', '3', 'MM-61', 'EE3', 'Kosong');
INSERT INTO `master_mess` VALUES ('62', '3', 'MM-62', 'FF3', 'Kosong');
INSERT INTO `master_mess` VALUES ('63', '3', 'MM-63', 'GG3', 'Kosong');
INSERT INTO `master_mess` VALUES ('64', '3', 'MM-64', 'HH3', 'Kosong');

-- ----------------------------
-- Table structure for `master_rumdin`
-- ----------------------------
DROP TABLE IF EXISTS `master_rumdin`;
CREATE TABLE `master_rumdin` (
  `id_rumdin` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_jenis_aset` int(11) NOT NULL,
  `kode_rumdin` varchar(20) NOT NULL,
  `alamat` varchar(200) NOT NULL,
  `luas_tanah_m2` varchar(5) DEFAULT NULL,
  `luas_bangunan_m2` varchar(5) DEFAULT NULL,
  `kreditur` varchar(5) NOT NULL,
  `status_aset` enum('Disewa','Kosong','Internal','Tidak Aktif','Perbaikan') DEFAULT 'Kosong',
  PRIMARY KEY (`id_rumdin`),
  UNIQUE KEY `kode_rumdin` (`kode_rumdin`) USING BTREE,
  KEY `id_jenis_aset` (`id_jenis_aset`),
  CONSTRAINT `master_rumdin_ibfk_1` FOREIGN KEY (`id_jenis_aset`) REFERENCES `master_jenis_aset` (`id_jenis_aset`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of master_rumdin
-- ----------------------------
INSERT INTO `master_rumdin` VALUES ('3', '2', 'RD-1', 'Embong Kemiri 19 – 21 Surabaya', '1745', '990', 'PPA', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('4', '2', 'RD-2', 'Darmo Permai Selatan XVI/20', '800', '216', 'PPA', 'Disewa');
INSERT INTO `master_rumdin` VALUES ('5', '2', 'RD-3', 'Darmo Permai Utara XVII No. 20 Surabaya', '560', '123', 'BNI', 'Disewa');
INSERT INTO `master_rumdin` VALUES ('6', '2', 'RD-4', 'Darmo Permai Selatan XVI/5 Surabaya', '308', '132', 'PPA', 'Disewa');
INSERT INTO `master_rumdin` VALUES ('7', '2', 'RD-5', 'Darmo Permai Utara XVII/18', '560', '123', 'BNI', 'Disewa');
INSERT INTO `master_rumdin` VALUES ('8', '2', 'RD-6', 'Kupang Indah XVII/22 Surabaya', '759', '269', 'BNI', 'Disewa');
INSERT INTO `master_rumdin` VALUES ('9', '2', 'RD-7', 'Kencana Sari Timur VII/H36 Surabaya', '480', '280', 'BNI', 'Disewa');
INSERT INTO `master_rumdin` VALUES ('10', '2', 'RD-8', 'Darmo Permai Selatan 14/10, Surabaya', '1872', '442', 'PPA', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('11', '2', 'RD-9', 'Darmo Permai Selatan 14/14, Surabaya', '750', '132', 'PPA', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('12', '2', 'RD-10', 'Darmo Permai Selatan 16/11, Surabaya', '308', '132', 'PPA', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('13', '2', 'RD-11', 'Darmo Permai Selatan 16/26, Surabaya', '814', '216', 'PPA', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('14', '2', 'RD-12', 'Darmo Permai Selatan 16/30, Surabaya', '1056', '216', 'PPA', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('15', '2', 'RD-13', 'Darmo Permai Selatan 16/7, Surabaya', '308', '132', 'PPA', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('16', '2', 'RD-14', 'Darmo Permai Utara 17/10, Surabaya', '490', '123', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('17', '2', 'RD-15', 'Darmo Permai Utara 17/12, Surabaya', '490', '123', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('18', '2', 'RD-16', 'Darmo Permai Utara 17/14, Surabaya', '490', '123', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('19', '2', 'RD-17', 'Darmo Permai Utara 17/16, Surabaya', '490', '123', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('20', '2', 'RD-18', 'Darmo Permai Utara 17/6, Surabaya', '490', '123', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('21', '2', 'RD-19', 'Darmo Permai Utara 17/8, Surabaya', '490', '123', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('22', '2', 'RD-20', 'Kriss Kencana Sari Timur VI/H/14, Surabaya', '408', '235', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('23', '2', 'RD-21', 'Kriss Kencana Sari Timur VII/H/37, Surabaya', '442', '235', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('24', '2', 'RD-22', 'Kriss Kencana Sari Timur VII/J/7, Surabaya', '480', '235', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('25', '2', 'RD-23', 'Kriss Kencana Sari Timur VIII/H/39, Surabaya', '571', '235', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('26', '2', 'RD-24', 'Kriss Kencana Sari Timur VIII/J/1, Surabaya', '384', '235', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('27', '2', 'RD-25', 'Kupang Indah XII/14, Surabaya', '674', '210', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('28', '2', 'RD-26', 'Siaga Raya 2A, Jakarta', '585', '422', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('29', '2', 'RD-27', 'Paradise V / 58, Jakarta', '742', '252', 'BNI', 'Kosong');
INSERT INTO `master_rumdin` VALUES ('30', '2', 'RD-28', 'Delima Timur III / A8, Jakarta', '419', '374', 'BNI', 'Kosong');

-- ----------------------------
-- Table structure for `transaksi_kantor`
-- ----------------------------
DROP TABLE IF EXISTS `transaksi_kantor`;
CREATE TABLE `transaksi_kantor` (
  `id_transaksi` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_kantor` bigint(20) NOT NULL,
  `luas_m2` decimal(10,2) NOT NULL,
  `nomor_surat` varchar(100) DEFAULT NULL,
  `penyewa` varchar(255) DEFAULT NULL,
  `pic_num` varchar(50) DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `durasi_bulan` int(11) DEFAULT NULL,
  `tarif_air` decimal(15,2) NOT NULL,
  `pem_sampah` decimal(15,2) DEFAULT NULL,
  `tarif_listrik` decimal(15,2) NOT NULL,
  `nilai_kontribusi_kantor_perbulan` decimal(15,2) NOT NULL,
  `nilai_kontribusi_pertahun_nonPPN` decimal(15,2) NOT NULL,
  `ket` varchar(50) NOT NULL,
  `no_surat_addendum` varchar(100) NOT NULL,
  `status` enum('Disewa','Selesai','Dibatalkan') NOT NULL DEFAULT 'Disewa',
  PRIMARY KEY (`id_transaksi`),
  KEY `id_kantor` (`id_kantor`),
  CONSTRAINT `transaksi_kantor_ibfk_1` FOREIGN KEY (`id_kantor`) REFERENCES `master_kantor` (`id_kantor`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of transaksi_kantor
-- ----------------------------
INSERT INTO `transaksi_kantor` VALUES ('1', '1', '22.75', 'SPER/KK/09/33000/VI/2025', 'PT Nusa Pratama Karya', '087854076946 (Bu Adinda P)', '2025-07-01', '2025-12-31', '6', '50000.00', '200000.00', '800000.00', '70000.00', '15855000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('2', '2', '22.75', 'SPER/KK/105/34000/XII/2024', 'PT. Bangun Perkasa Jaya Engineering', '085731110397 (P Joko Waluyo)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('3', '3', '22.75', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('4', '4', '22.75', 'SPER/KK/115/34000/XII/2024', 'PT Fajar Alif Makmur', '082231369397 (P. Syafril)', '2025-01-01', '2025-09-30', '9', '50000.00', '200000.00', '800000.00', '70000.00', '23782500.00', 'Addendum Kontrak Perjanjian', 'SPER/KK/115.A/33000/IX/2025', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('5', '5', '22.75', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('6', '6', '22.75', 'SPER/KK/104/34000/XII/2024', 'PT Dua Mitra Lestari', '085852300930 (P Minin)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', 'Addendum Perjanjian Kontrak', 'SPER/KK/104.A/33000/VIII/2025', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('7', '7', '22.75', 'SPER/KK/100/34000/XII/2024', 'PT Global Amanah Nusantara', '083833728203 (Bu. Rahma)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('8', '8', '31.50', 'SPER/KK/118/34000/XII/2024', 'PT Wiratama Indo Makmur', '081249084999 (P Nanang)', '2025-01-01', '2025-08-31', '8', '50000.00', '200000.00', '800000.00', '70000.00', '21140000.00', 'Addendum Perjanjian Kontrak', 'SPER/KK/118.A/33000/VIII/2025', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('9', '9', '22.75', 'SPER/KK/109/34000/XII/2024', 'PT Langgeng Sejahtera Utama', '082211539322 (P. Hadi)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('10', '10', '22.75', 'SPER/KK/121/34000/XII/2024', 'PT Sawega Abdi Setia', '08123589204 (P. Berry Wahono)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('11', '11', '22.75', '-', 'Ruang Rapat AMK', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('12', '12', '22.75', 'SPER/KK/1/34000/XII/2024', 'PT Kanaka Jaya Sheifa', '082143308681 (P. Budi Wibowo)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('13', '13', '22.75', 'SPER/KK/101/34000/XII/2024', 'PT Idtec Marindo', '083833728203 (Rahma)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('14', '14', '22.75', 'SPER/KK/122/34000/XII/2024', 'PT Akasia Sinergi Pratama', '081230341277 (Bu Nurul)', '2025-01-01', '2025-08-31', '8', '50000.00', '200000.00', '800000.00', '70000.00', '21140000.00', 'Addendum Perjanjian Kontrak', 'SPER/KK/122.A/33000/VIII/2025', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('15', '15', '22.75', 'SPER/KK/107/34000/XII/2024', 'PT Dua Dua Kutai Utama', '085784379161 (Bu Sri Yayuk)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('16', '16', '22.75', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('17', '17', '22.75', 'SPER/KK/116/34000/XII/2024', 'PT Putra Teknik Solusi', '08113005088 (P. Momon)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('18', '18', '22.75', 'SPER/KK/117/34000/XII/2024', 'PT Hamid Jaya Mandiri', '081217303025 (Fricky)', '2025-01-01', '2025-08-31', '8', '50000.00', '200000.00', '800000.00', '70000.00', '21140000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('19', '19', '22.75', 'SPER/KK/114/34000/XII/2024', 'PT Sukses Laju Mandiri', '08123030295 (P Suwarno)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('20', '20', '22.75', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('21', '21', '31.85', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('22', '22', '22.75', '-', 'Ruang Arsip Kapal Selam', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('23', '23', '22.75', 'SPER/KK/110/34000/XII/2024', 'PT Budi Setiawan Karya Utama', '085706595560 (P Sasmito)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('24', '24', '22.75', '-', 'Ruang Arsip Kapal Selam', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('25', '25', '22.75', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('26', '26', '22.75', '-', 'Ruang Arsip Kapal Selam', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('27', '27', '22.75', 'SPER/KK/13/33000/VIII/2025', 'PT Matra Kosala Digdaya (Baru)', '089501820702 (Edward Rifai)', '2025-08-14', '2025-09-13', '1', '50000.00', '200000.00', '800000.00', '70000.00', '2642500.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('28', '28', '22.75', '-', 'Ruang Arsip Kapal Selam', '087854076946 (Bu Adinda P)', '2025-07-01', '2025-12-31', '6', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('29', '29', '20.50', 'SPER/KK/119/34000/XII/2024', 'PT Prima Dwi Nusa', '08121725528 (P. Ngatenen)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '29820200.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('30', '30', '44.25', 'SPER/KK/05/34000/III/2025', 'PT Wahyu Bangkit Sentosa', '081553273422 (P. Budi Slamet)', '2025-04-01', '2025-12-31', '9', '50000.00', '200000.00', '800000.00', '70000.00', '36855000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('31', '31', '22.75', 'SPER/KK/102/34000/XII/2024', 'PT Mutiara Technik Utama', '081234652248 (Bu Hindun)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('32', '32', '22.75', 'SPER/KK/103/34000/XII/2024', 'PT Alredho Teknik', '082234205118 (Bu Santy)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('33', '33', '22.75', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('34', '34', '31.25', 'SPER/KK/111A/34000/XII/2024', 'PT Aulia Karya Perdana', '081235955706 (P. Jono)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '38850000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('35', '35', '22.75', 'SPER/KK/106/34000/XII/2024', 'PT Dwi Karya Jaya', '082257876629 (Bu Erna)', '2025-01-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '31710000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('36', '36', '22.75', '-', 'Kosong', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('37', '37', '52.00', 'SPER/KK/99/34000/XI/2024', 'PT Bank Mandiri (Persero) Tbk', '081332700605 (Bu Yulia Lukki)', '2025-07-01', '2025-12-31', '12', '50000.00', '200000.00', '800000.00', '70000.00', '183360000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('38', '38', '36.00', 'SPER/KK/01/34000/I/2023', 'Heinen & Hoopman', '0818830457 (Roy Hanang)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '18000000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('39', '39', '35.00', 'SPER/KK/77/34000/X/2024', 'Naval Group', '', '2024-08-15', '2024-08-14', '0', '0.00', '200000.00', '0.00', '0.00', '42000000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('40', '40', '80.00', 'SPER/KK/14/33000/VIII/2025', 'PT Guna Rogate Indah', '081234508339 (P. Donny)', '2025-09-01', '2025-12-31', '4', '0.00', '200000.00', '0.00', '0.00', '26008000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('41', '41', '40.00', 'SPER/KK/16/33000/IX/2025', 'PT Matra Kosala Digdaya (Baru)', '089501820702 (Edward Rifai)', '2025-09-13', '2025-11-13', '3', '0.00', '200000.00', '0.00', '0.00', '5893868.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('42', '42', '12.48', 'SPER/KK/21/33000/XI/2025', 'PT Mekanika Wira Mandiri Indonesia', '', '2025-11-01', '2026-03-31', '5', '0.00', '200000.00', '0.00', '0.00', '13114400.00', '', '', 'Disewa');
INSERT INTO `transaksi_kantor` VALUES ('43', '43', '200.00', 'SPER/KK/15/33000/VIII/2025', 'CV. Gynara Lima (Cafe Sempulur)', '081333240518 (P. Dondy)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '168000000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('44', '44', '30.00', 'SPER/KK/120/34000/XI/2024', 'CV. Tiga Putra Mulia', '081237484151 (P. Sajuri)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '28200000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('45', '45', '26.00', 'SPER/KK/08/33000/IV/2025', 'PT Bayu Samudera Alam', '085230097007 (Bu Nanik)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '16560000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('46', '46', '26.00', '-', 'Internal PT PAL (PKBL)', '', '0000-00-00', '0000-00-00', '0', '50000.00', '200000.00', '800000.00', '70000.00', '0.00', '', '', '');
INSERT INTO `transaksi_kantor` VALUES ('47', '47', '90.48', 'SPER/KK/113/34000/XII/2024', 'PT Karya Sarika Sejahtera', '085733439699 (Bu Inayah)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '79003200.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('48', '48', '190.00', 'SPER/KK/127/34000/XII/2024', 'Dana Pensiun PAL', '08155293980 (P Didit)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '3000000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('49', '49', '250.05', 'SPER/KK/125/34000/XII/2024', 'PT Palindojaya Utama', '082139732868 (P Mulyana)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '84720000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('50', '50', '269.60', 'SPER/KK/76/34000/VI/2024', 'PT PAL Marine Service', '', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '46090000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('51', '51', '136.51', '-', 'Mitra PAL', '085852226122 (P. Zulmaidi)', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '0.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('52', '52', '602.00', 'SPER/KK/124/34000/XII/2024', 'KOP KB PAL', '', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '3000000.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('53', '53', '910.00', '-', 'Gita Pawestri', '', '2025-01-01', '2025-12-31', '12', '0.00', '200000.00', '0.00', '0.00', '0.00', '', '', 'Selesai');
INSERT INTO `transaksi_kantor` VALUES ('54', '54', '1.35', 'SPER/7/10000/IV/2012', 'PT POSSI', '', '2010-08-15', '2025-08-16', '0', '0.00', '0.00', '0.00', '0.00', '0.00', '', '', 'Selesai');

-- ----------------------------
-- Table structure for `transaksi_kontainer`
-- ----------------------------
DROP TABLE IF EXISTS `transaksi_kontainer`;
CREATE TABLE `transaksi_kontainer` (
  `id_transaksi` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_kontainer` bigint(20) NOT NULL,
  `nomor_surat` varchar(100) DEFAULT NULL,
  `penyewa` varchar(255) DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `durasi_bulan` int(11) DEFAULT NULL,
  `pem_sampah` varchar(20) DEFAULT NULL,
  `nilai_kontribusi_perbulan` decimal(15,2) NOT NULL,
  `nilai_kontribusi_lahan_perbulan` decimal(15,2) NOT NULL,
  `nilai_kontribusi_pertahun_nonPPN` decimal(15,2) NOT NULL,
  `status` enum('Disewa','Selesai','Dibatalkan') NOT NULL DEFAULT 'Disewa',
  PRIMARY KEY (`id_transaksi`),
  KEY `id_kontainer` (`id_kontainer`),
  CONSTRAINT `transaksi_kontainer_ibfk_1` FOREIGN KEY (`id_kontainer`) REFERENCES `master_kontainer` (`id_kontainer`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of transaksi_kontainer
-- ----------------------------
INSERT INTO `transaksi_kontainer` VALUES ('1', '4', 'SPER/KK/02/33000/III/2025\r\n', 'PT. Bayu Samudera Alam\r\n', '2025-04-01', '2025-12-31', '9', '200000', '34000.00', '35000.00', '10742400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('2', '5', 'SPER/KK/17/33000/IX/2025', 'PT. Energi Creative Indonesia', '2025-09-23', '2026-03-23', '7', '200000', '34000.00', '35000.00', '13123200.00', 'Disewa');
INSERT INTO `transaksi_kontainer` VALUES ('3', '6', 'SPER/KK/18/33000/X/2025', 'PT. Gariyan Alfath Saguna', '2025-03-24', '2025-12-31', '10', '200000', '27500.00', '35000.00', '10148387.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('4', '7', 'SPER/KK/19/33000/X/2025', 'PT. Gariyan Alfath Saguna', '2025-08-14', '2025-12-31', '5', '200000', '27500.00', '35000.00', '5003226.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('5', '8', 'SPER/KK/20/33000/X/2025', 'PT. Sukses Laju Mandiri', '2025-10-06', '2026-10-06', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Disewa');
INSERT INTO `transaksi_kontainer` VALUES ('6', '9', 'SPER/KK/11/33000/VII/2025', 'PT. Tri Megah Jaya Abadi', '2025-07-24', '2025-12-31', '7', '200000', '34000.00', '35000.00', '11429885.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('7', '10', 'SPER/KK/153/34000/XII/2024', 'PT. Aditya Rizky Anugrah', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('8', '11', 'SPER/KK/170/34000/XII/2024', 'PT. Akasia Sinergi Pratama', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('9', '12', 'SPER/KK/160/34000/XII/2024', 'PT. Alredho Teknik', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '14323200.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('10', '13', 'SPER/KK/169/34000/XII/2024', 'PT. Arvet Unggul Jaya', '2025-07-24', '2025-12-31', '7', '200000', '34000.00', '35000.00', '14323200.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('11', '14', 'SPER/KK/163/34000/XII/2024', 'PT. Aulia Karya Perdana', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('12', '15', 'SPER/KK/156/34000/XII/2024', 'PT. Bangun Perkasa Jaya Engineering', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('13', '16', 'SPER/KK/160/34000/XII/2024', 'PT. Bayu Samudera Alam', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '14323200.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('14', '17', 'SPER/KK/169/34000/XII/2024', 'PT. Dua Dua Kutai Utama', '2025-07-24', '2025-12-31', '7', '200000', '34000.00', '35000.00', '14323200.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('15', '18', 'SPER/KK/163/34000/XII/2024', 'PT. Dua Mitra Lestari', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('16', '19', 'SPER/KK/156/34000/XII/2024', 'PT. Dua Mitra Lestari', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('17', '20', 'SPER/KK/160/34000/XII/2024', 'PT. Dua Mitra Lestari', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '14323200.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('18', '21', 'SPER/KK/169/34000/XII/2024', 'PT. Dwi Karya Jaya', '2025-07-24', '2025-12-31', '7', '200000', '34000.00', '35000.00', '14323200.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('19', '22', 'SPER/KK/163/34000/XII/2024', 'PT. Dwi Karya Jaya', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '24000000.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('20', '23', 'SPER/KK/156/34000/XII/2024', 'PT. Fajar Alif Makmur', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '14323200.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('21', '24', 'SPER/KK/160/34000/XII/2024', 'PT. IDTEC MARINDO', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('22', '25', 'SPER/KK/169/34000/XII/2024', 'PT. Langgeng Sejahtera Utama', '2025-07-24', '2025-12-31', '7', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('23', '26', 'SPER/KK/163/34000/XII/2024', 'PT. Mutiara Technik Utama', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('24', '27', 'SPER/KK/156/34000/XII/2024', 'PT. Palindo Jaya Utama', '2025-01-01', '2025-12-31', '12', '200000', '27500.00', '35000.00', '13200000.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('25', '28', 'SPER/KK/160/34000/XII/2024', 'PT. Palindo Jaya Utama', '2025-01-01', '2025-12-31', '12', '200000', '27500.00', '35000.00', '13200000.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('26', '29', 'SPER/KK/169/34000/XII/2024', 'PT. Prima Dwi Nusa', '2025-07-24', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('27', '30', 'SPER/KK/163/34000/XII/2024', 'PT. Prima Dwi Nusa', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('28', '31', 'SPER/KK/156/34000/XII/2024', 'PT. Sawega Abdi Setia', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('29', '32', 'SPER/KK/160/34000/XII/2024', 'PT. Sawega Abdi Setia', '2025-01-01', '2025-12-31', '12', '200000', '27500.00', '35000.00', '24000000.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('30', '33', 'SPER/KK/169/34000/XII/2024', 'PT. Wahyu Bangkit Sentosa', '2025-07-24', '2025-12-31', '7', '200000', '34000.00', '35000.00', '26246400.00', 'Selesai');
INSERT INTO `transaksi_kontainer` VALUES ('31', '34', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '200000', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('32', '35', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '200000', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('33', '36', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '200000', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('34', '37', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '200000', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('35', '38', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '200000', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('36', '39', '-', 'kosong milik pelindo', '0000-00-00', '0000-00-00', '0', '200000', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('37', '40', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '0', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('38', '41', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '0', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('39', '42', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '0', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('40', '41', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '0', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('41', '42', '-', 'kosong', '0000-00-00', '0000-00-00', '0', '0', '0.00', '35000.00', '0.00', '');
INSERT INTO `transaksi_kontainer` VALUES ('42', '2', '-', 'MITRA PAL', '2025-01-01', '2025-12-31', '12', '200000', '34000.00', '35000.00', '0.00', '');

-- ----------------------------
-- Table structure for `transaksi_lahan`
-- ----------------------------
DROP TABLE IF EXISTS `transaksi_lahan`;
CREATE TABLE `transaksi_lahan` (
  `id_transaksi` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_lahan` bigint(20) NOT NULL,
  `luas_m2` decimal(10,2) DEFAULT NULL,
  `nomor_surat` varchar(100) DEFAULT NULL,
  `penyewa` varchar(255) DEFAULT NULL,
  `pic_num` varchar(50) DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `durasi_bulan` int(11) DEFAULT NULL,
  `tarif_air` decimal(15,2) NOT NULL,
  `pem_sampah` decimal(15,2) NOT NULL,
  `tarif_listrik` decimal(15,2) NOT NULL,
  `nilai_kontribusi_lahan_perbulan` decimal(15,2) NOT NULL,
  `nilai_kontribusi_pertahun_nonPPN` decimal(15,2) NOT NULL,
  `ket` varchar(20) NOT NULL,
  `status` enum('Disewa','Selesai','Dibatalkan') NOT NULL DEFAULT 'Disewa',
  PRIMARY KEY (`id_transaksi`),
  KEY `id_lahan` (`id_lahan`),
  CONSTRAINT `transaksi_lahan_ibfk_1` FOREIGN KEY (`id_lahan`) REFERENCES `master_lahan` (`id_lahan`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of transaksi_lahan
-- ----------------------------
INSERT INTO `transaksi_lahan` VALUES ('1', '1', '0.00', 'SPER/KK/07/34000/VI/2025', 'PT Epid Menara Asset Co.', '0816665775 (Ibu Farah)', '2025-06-30', '2028-07-10', '36', '0.00', '0.00', '0.00', '0.00', '270000000.00', 'sewa 3 tahun', 'Disewa');
INSERT INTO `transaksi_lahan` VALUES ('2', '2', '8.00', 'SPER/KK/155/34000/XII/2024', 'PT Bank Negara Indonesia (Persero) Tbk', '085330250013 (P Bayu)', '2025-01-01', '2026-12-31', '24', '0.00', '0.00', '0.00', '0.00', '113000000.00', 'sewa 2 tahun', 'Disewa');
INSERT INTO `transaksi_lahan` VALUES ('3', '3', '8.00', 'SPER/KK/167/34000/XII/2024', 'PT Bank Rakyat Indonesia (Persero) Tbk', '081233433572 (Bu Nessa)', '2025-01-01', '2025-12-31', '12', '0.00', '0.00', '0.00', '0.00', '56500000.00', '', 'Selesai');
INSERT INTO `transaksi_lahan` VALUES ('4', '4', '8.00', 'SPER/KK/0028/34000/XI/2024', 'PT Bank Mandiri (Persero) Tbk', '081332700605 (Bu Yulia Lukki)', '2025-01-01', '2025-12-31', '12', '0.00', '0.00', '0.00', '0.00', '56500000.00', '', 'Selesai');
INSERT INTO `transaksi_lahan` VALUES ('5', '5', '6.00', 'SPER/KK/8A/33000/V/2025', 'PT Bank Syariah Indonesia', '085735765548 (BU Husna)', '2025-08-01', '2026-07-31', '12', '0.00', '0.00', '0.00', '0.00', '60000000.00', '', 'Disewa');
INSERT INTO `transaksi_lahan` VALUES ('6', '6', '285.00', 'SPER/KK/68/34000/XII/2024', 'PT PP', '081380940669 (P. Gertaka)', '2025-01-01', '2025-12-31', '12', '0.00', '0.00', '0.00', '0.00', '119700000.00', '', 'Selesai');
INSERT INTO `transaksi_lahan` VALUES ('7', '7', '55.58', 'SPER/KK/168/34000/XII/2024', 'PT Artistama', '081249013197', '2024-12-18', '2025-08-19', '9', '0.00', '0.00', '0.00', '0.00', '17190400.00', '', 'Selesai');

-- ----------------------------
-- Table structure for `transaksi_mess`
-- ----------------------------
DROP TABLE IF EXISTS `transaksi_mess`;
CREATE TABLE `transaksi_mess` (
  `id_transaksi` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_mess` bigint(20) NOT NULL,
  `Penyewa` varchar(100) NOT NULL,
  `unit_kerja` varchar(100) NOT NULL,
  `nomor_surat` varchar(100) DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `durasi_bulan` int(11) DEFAULT NULL,
  `nilai_kontribusi_perbulan` decimal(15,2) DEFAULT NULL,
  `status` enum('Disewa','Selesai','Dibatalkan') NOT NULL DEFAULT 'Disewa',
  PRIMARY KEY (`id_transaksi`),
  KEY `id_mess` (`id_mess`),
  CONSTRAINT `transaksi_mess_ibfk_1` FOREIGN KEY (`id_mess`) REFERENCES `master_mess` (`id_mess`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of transaksi_mess
-- ----------------------------
INSERT INTO `transaksi_mess` VALUES ('1', '1', 'Ferry Teguh Winarto', 'Kapal Selam', 'SPER/MM/01/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('2', '2', 'I Putu Suwantika', 'Pemeliharaan & Perbaikan', 'SPER/MM/02/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('3', '3', 'Hairuman Lating', 'Outsourcing', 'SPER/MM/03/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('4', '4', 'Fauzan Jamil', 'Kapal Perang', 'SPER/MM/04/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('5', '5', 'Zainul Abidin', 'Pemeliharaan & Perbaikan', 'SPER/MM/05/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('6', '6', 'Puji Utomo', 'Technology & QA', 'SPER/MM/06/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('7', '7', 'Achmad Ardiansyah', 'Kapal Perang', 'SPER/MM/07/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('8', '8', 'Kusnomo', 'Kapal Selam', 'SPER/MM/08/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('9', '9', 'Johan Adi Widodo', 'Kapal Perang', 'SPER/MM/35A/33000/VI/2025', '2025-09-01', '2025-12-31', '4', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('10', '10', 'Minahul Karim', 'Desain', 'SPER/MM/10/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('11', '11', 'Antono', 'Kapal Niaga', 'SPER/MM/11/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('12', '12', 'Yakub', 'Rekayasa Umum', 'SPER/MM/12/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('13', '13', 'Sunarno', 'Kapal Perang', 'SPER/MM/13/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('14', '14', 'Tomy Agusrianto', 'Rekayasa Umum', 'SPER/MM/14/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('15', '15', 'Ahmad Hidayaturrahman', 'Kapal Perang', 'SPER/MM/15/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('16', '16', 'Gargarin Frakas Farandika', 'Kapal Perang', 'SPER/MM/16/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '450000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('17', '17', 'Ari Ardiansyah', 'Kapal Niaga', 'SPER/MM/17A/34000/IV/2025', '2024-12-01', '2025-12-31', '13', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('18', '18', 'Agus Hari Supardjo', 'Kapal Selam', 'SPER/MM/18/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('19', '19', 'Arif Rahman Setiawan', 'Kapal Niaga', 'SPER/MM/19/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('20', '21', 'Iwan Dwi Susanto', 'Kapal Selam', 'SPER/MM/20/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('21', '21', 'Eko Priyono', 'Kapal Niaga', 'SPER/MM/21/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('22', '22', 'Mochammad Lutfi', 'Kapal Selam', 'SPER/MM/22/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('23', '23', 'Moh. Nur Iman', 'Technology & QA', 'SPER/MM/54A/33000/I/2025', '2025-02-01', '2025-12-31', '11', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('24', '24', 'Achmadi Apriyanto', 'Rekayasa Umum', 'SPER/MM/23/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('25', '25', 'Joko Setiawan', 'Pemeliharaan & Perbaikan', 'SPER/MM/24/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('26', '26', 'Krisvan Maryuanto Arrido', 'Pemeliharaan & Perbaikan', 'SPER/MM/25/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('27', '27', 'Angga Dwi Rachmadani', 'Kapal Perang', 'SPER/MM/26/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('28', '28', 'Suharyoko', 'Kapal Niaga', 'SPER/MM/27/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('29', '29', 'Panuju Riyono, A.Md', 'Kapal Selam', 'SPER/MM/28/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('30', '30', 'Nurhadi', 'Perbendaharaan', 'SPER/MM/02/33000/IV/2025', '2025-05-01', '2025-12-31', '8', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('31', '31', 'Arif Darmawan', 'Kapal Selam', 'SPER/MM/30/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('32', '32', 'Timbul Sigit Priadi', 'Kapal Niaga', 'SPER/MM/31/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '400000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('33', '33', 'Moh. Hadi Kusumo', 'Kapal Selam', 'SPER/MM/32/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('34', '34', 'Mochammad Taufiq Abdullah', 'Rekayasa Umum', 'SPER/MM/33/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('35', '35', 'Kamil Mucharom', 'Technology & QA', 'SPER/MM/34/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('36', '36', 'Ari Yuli Saputra', 'Pemeliharaan & Perbaikan', 'SPER/MM/04/33000/VIII/2025', '2025-09-01', '2025-12-31', '4', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('37', '37', 'Ahmad Dwi Handoko', 'Kapal Selam', 'SPER/MM/36/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('38', '38', 'Danang Eka Saputro', 'Technology & QA', 'SPER/MM/37/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('39', '39', 'Kateno', 'Kapal Selam', 'SPER/MM/38/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('40', '40', 'Wahyu Nugroho', 'Rekayasa Umum', 'SPER/MM/39/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('41', '41', 'Yusuf Dwi Ekadana', 'MATRA & K3LH', 'SPER/MM/40/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('42', '42', 'Agus Salim', 'Kapal Perang', 'SPER/MM/41/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('43', '43', 'Aris Harmoko', 'Technology & QA', 'SPER/MM/42/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('44', '44', 'Ashka Azhar Abadi', 'Renstra. Perusahaan', 'SPER/MM/43/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('45', '45', 'Muhammad Jumadi', 'Kapal Niaga', 'SPER/MM/44/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('46', '46', 'Jupri', 'Kapal Selam', 'SPER/MM/06/33000/XII/2025', '2025-12-01', '2025-12-31', '1', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('47', '47', 'Zaenal Arifin', 'Kapal Niaga', 'SPER/MM/46/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('48', '48', 'Warih Dwi Juanaji', 'Kapal Selam', 'SPER/MM/05/33000/VIII/2025', '2025-09-01', '2025-12-31', '4', '350000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('49', '49', 'Adi Priyanto', 'Kapal Niaga', 'SPER/MM/48/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('50', '50', 'Dendi Eko Prasetyo', 'Pemeliharaan & Perbaikan', 'SPER/MM/49/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('51', '51', 'Hari Cahyono', 'Kapal Niaga', 'SPER/MM/50/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('52', '52', 'Yuli Wijayanto', 'Kapal Niaga', 'SPER/MM/51/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('53', '53', 'Susanto', 'Rekayasa Umum', 'SPER/MM/52/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('54', '54', 'Sugeng Santoso', 'Pemeliharaan & Perbaikan', 'SPER/MM/53/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('55', '55', 'Hadi Zuana', 'Kapal Perang', 'SPER/MM/03/33000/V/2025', '2025-06-01', '2025-12-31', '7', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('56', '56', 'Butuh Perbaikan', '-', '-', '0000-00-00', '0000-00-00', '0', '0.00', '');
INSERT INTO `transaksi_mess` VALUES ('57', '57', 'Sukariyono', 'Pemeliharaan & Perbaikan', 'SPER/MM/55/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('58', '58', 'Edy Supana', 'Technology & QA', 'SPER/MM/56/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('59', '59', 'Rudi Safrijal', 'Kapal Niaga', 'SPER/MM/57/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('60', '60', 'Midi', 'Kapal Niaga', 'SPER/MM/58/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('61', '61', 'Wahyu Hidayat Nurdiansyah', 'Technology & QA', 'SPER/MM/61/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('62', '62', 'Febri Setiawan', 'Rekayasa Umum', 'SPER/MM/59/34000/XI/2024', '2025-01-01', '2025-12-31', '0', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('63', '63', 'Suselo Stya Mahanto', 'Rekayasa Umum', 'SPER/MM/60/34000/XI/2024', '2025-01-01', '2025-12-31', '12', '300000.00', 'Selesai');
INSERT INTO `transaksi_mess` VALUES ('64', '64', 'Ferdy Hendra Mbayowo', 'Technology & QA', 'SPER/MM/01/33000/II/2025', '2025-03-01', '2025-12-31', '10', '300000.00', 'Selesai');

-- ----------------------------
-- Table structure for `transaksi_rumdin`
-- ----------------------------
DROP TABLE IF EXISTS `transaksi_rumdin`;
CREATE TABLE `transaksi_rumdin` (
  `id_transaksi` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_rumdin` bigint(20) NOT NULL,
  `nomor_surat` varchar(100) DEFAULT NULL,
  `penyewa` varchar(100) DEFAULT NULL,
  `luas_tanah_m2` varchar(5) NOT NULL,
  `luas_bangunan_m2` varchar(5) NOT NULL,
  `pic_number` varchar(50) DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `nilai_kontribusi_pertahun` decimal(15,2) NOT NULL,
  `kreditur` varchar(10) NOT NULL,
  `status` enum('Disewa','Selesai','Dibatalkan') NOT NULL DEFAULT 'Disewa',
  PRIMARY KEY (`id_transaksi`),
  KEY `id_rumdin` (`id_rumdin`),
  CONSTRAINT `transaksi_rumdin_ibfk_1` FOREIGN KEY (`id_rumdin`) REFERENCES `master_rumdin` (`id_rumdin`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of transaksi_rumdin
-- ----------------------------
INSERT INTO `transaksi_rumdin` VALUES ('1', '3', 'SPER/RD/556/34000/XII/2025 Tanggal 18 Desember 2023', 'Ahmad  Dhani  Prasetyo', '1745', '540', '081212707070 (Bu Mira)', '2024-12-01', '2025-11-30', '700000000.00', 'PPA', 'Selesai');
INSERT INTO `transaksi_rumdin` VALUES ('2', '4', 'SPER/RD/03/34000/VI/2025 Tanggal 03 Juni 2024', 'Lukas Janny', '960', '490', '081216880000 (Bu Janny)', '2024-06-01', '2026-05-31', '85162102.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('3', '5', 'SPER/RD/04/34000/IX/2024 Tanggal 02 September 2024', 'Shinta Tirta Dewi', '525', '305', '-', '2024-09-01', '2026-08-31', '72202400.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('4', '6', 'SPER/RD/01/33000/V/2025 Tanggal 01 Mei 2025', 'PT Kusuma Jaya Sejahtera (Endarsono)', '400', '216', '082257723999 (Bu Try Han)', '2025-05-30', '2026-05-29', '54744000.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('5', '7', 'SPER/RD/02/33000/V/2025 Tanggal 30 Mei 2025', 'Joko Husodo', '525', '302', '082211115059 (Joko DPU)', '2025-02-01', '2026-01-31', '66310500.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('6', '8', 'SPER/RD/03/33000/VI/2025 Tanggal 30 Juni 2025', 'Marisca Mukti Widjojo', '758', '239', '0811309825 (Bu Marisca)', '2025-04-01', '2026-03-31', '78000000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('7', '9', 'SPER/RD/04/33000/VIII/2025 Tanggal 01 Agustus 2025', 'Andreas Yuniman Tjandra', '480', '280', '-', '2025-10-01', '2026-09-30', '76000000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('8', '10', '-', 'Kosong', '805', '450', '-', '0000-00-00', '0000-00-00', '242548000.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('9', '11', '-', 'Kosong', '850', '450', '-', '0000-00-00', '0000-00-00', '116115000.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('10', '12', '-', 'Kosong', '400', '216', '-', '0000-00-00', '0000-00-00', '54744000.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('11', '13', '-', 'Rencana akan digunakan untuk Naval (SATGAS)', '960', '490', '-', '2023-12-01', '2024-11-30', '130704000.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('12', '14', '-', 'Kosong', '1000', '490', '-', '0000-00-00', '0000-00-00', '135660000.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('13', '15', '-', 'Kosong', '216', '216', '-', '0000-00-00', '0000-00-00', '54744000.00', 'PPA', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('14', '16', '-', 'Kosong', '525', '100', '-', '0000-00-00', '0000-00-00', '61642500.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('15', '17', '-', 'Kosong', '525', '300', '-', '0000-00-00', '0000-00-00', '66262500.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('16', '18', '-', 'Kosong', '525', '300', '-', '0000-00-00', '0000-00-00', '66262500.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('17', '19', '-', 'Kosong', '525', '300', '-', '0000-00-00', '0000-00-00', '66262500.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('18', '20', '-', 'Kosong', '525', '300', '-', '0000-00-00', '0000-00-00', '59301000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('19', '21', '-', 'Kosong', '490', '174', '-', '0000-00-00', '0000-00-00', '59301000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('20', '22', '-', 'Rencana akan digunakan untuk Naval (SATGAS)', '495', '254', '-', '0000-00-00', '0000-00-00', '54499500.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('21', '23', '-', 'Kosong', '495', '254', '-', '0000-00-00', '0000-00-00', '67426500.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('22', '24', '-', 'Digunakan TKA Jepang', '480', '320', '-', '0000-00-00', '0000-00-00', '81000000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('23', '25', '-', 'Digunakan LD Philipne', '544', '336', '-', '0000-00-00', '0000-00-00', '84000000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('24', '26', '-', 'Kosong', '375', '105', '-', '0000-00-00', '0000-00-00', '66000000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('25', '27', '-', 'Kosong', '525', '300', '-', '0000-00-00', '0000-00-00', '47754000.00', 'BNI', 'Disewa');
INSERT INTO `transaksi_rumdin` VALUES ('26', '28', '-', 'Kosong', '', '', '-', '0000-00-00', '0000-00-00', '188000000.00', 'BNI', '');
INSERT INTO `transaksi_rumdin` VALUES ('27', '29', '-', 'Kosong', '', '', '-', '0000-00-00', '0000-00-00', '486295120.00', 'BNI', '');
INSERT INTO `transaksi_rumdin` VALUES ('28', '30', '-', 'Kosong', '', '', '-', '0000-00-00', '0000-00-00', '114548520.00', 'BNI', '');

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
