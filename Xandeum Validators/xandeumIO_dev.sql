-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host:
-- Generation Time: Sep 06, 2023 at 03:37 PM
-- Server version: 8.0.34
-- PHP Version: 7.3.31-1~deb10u4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `xandeumIO_dev`
--
CREATE DATABASE IF NOT EXISTS `xandeumIO_dev` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `xandeumIO_dev`;

-- --------------------------------------------------------

--
-- Table structure for table `epochInfo`
--

CREATE TABLE `epochInfo` (
  `epoch` int NOT NULL,
  `slots` int NOT NULL,
  `transactionCount` bigint NOT NULL,
  `sysCreateDate` timestamp NOT NULL,
  `sysChangeDate` timestamp NOT NULL,
  `globalID` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `validatorKYC`
--

CREATE TABLE `validatorKYC` (
  `submittedAt` timestamp NOT NULL,
  `nameFirst` varchar(35) NOT NULL,
  `nameLast` varchar(35) NOT NULL,
  `addressFull` varchar(150) NOT NULL,
  `addressUnit` varchar(25) NOT NULL,
  `addressStreetNumber` int NOT NULL,
  `addressStreet` varchar(50) NOT NULL,
  `addressCity` varchar(50) NOT NULL,
  `addressState` varchar(50) NOT NULL,
  `addressPostCode` varchar(15) NOT NULL,
  `addressCountry` varchar(50) NOT NULL,
  `addressLat` double NOT NULL,
  `addressLon` double NOT NULL,
  `xandLicenseAddress` varchar(44) NOT NULL,
  `ipAddress` varchar(45) NOT NULL,
  `validatorID` varchar(44) NOT NULL,
  `voteID` varchar(44) NOT NULL,
  `eMail` varchar(100) NOT NULL,
  `discordHandle` varchar(100) NOT NULL,
  `internetConnection` varchar(25) NOT NULL,
  `linuxProficiency` varchar(150) NOT NULL,
  `hardwareOwnership` varchar(25) NOT NULL,
  `hardwareType` varchar(25) NOT NULL,
  `hardwareCPU` varchar(25) NOT NULL,
  `hardwareCPUSpeed` varchar(25) NOT NULL,
  `hardwareRAMGB` int NOT NULL,
  `hardwareStoreageType` varchar(25) NOT NULL,
  `hardwareStorageCapacityGB` int NOT NULL,
  `pdfs` varchar(50) NOT NULL,
  `totalAmount` bigint NOT NULL,
  `customerID` varchar(44) NOT NULL,
  `ipAddressSignUp` int NOT NULL,
  `ID` varchar(44) NOT NULL,
  `utmSource` varchar(150) NOT NULL,
  `utmCampaign` varchar(150) NOT NULL,
  `utmTerm` varchar(100) NOT NULL,
  `utmContent` varchar(150) NOT NULL,
  `hardwareDeviceType` varchar(50) NOT NULL,
  `sysCreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `validators`
--

CREATE TABLE `validators` (
  `validatorID` varchar(44) NOT NULL,
  `firstCaptureDate` timestamp NOT NULL,
  `sysCreateDate` timestamp NOT NULL,
  `sysChangeDate` timestamp NOT NULL,
  `globalID` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `validatorsConfig`
--

CREATE TABLE `validatorsConfig` (
  `ipAddress` varchar(45) NOT NULL,
  `port` varchar(5) NOT NULL,
  `gossip` varchar(50) NOT NULL,
  `validatorVersion` varchar(10) NOT NULL,
  `sysCreateDate` timestamp NOT NULL,
  `sysChangeDate` timestamp NOT NULL,
  `fkID` varchar(32) NOT NULL,
  `globalID` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `votingValidators`
--

CREATE TABLE `votingValidators` (
  `validatorID` varchar(44) NOT NULL,
  `voteID` varchar(44) NOT NULL,
  `commission` int NOT NULL,
  `activatedStake` bigint NOT NULL,
  `lastVote` bigint NOT NULL,
  `current` varchar(15) NOT NULL,
  `sysCreateDate` timestamp NOT NULL,
  `sysChangeDate` timestamp NOT NULL,
  `fkID` varchar(32) NOT NULL,
  `GlobalID` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `votingValidatorVotes`
--

CREATE TABLE `votingValidatorVotes` (
  `epoch` int NOT NULL,
  `credits` bigint NOT NULL,
  `previousCredits` bigint NOT NULL,
  `sysCreateDate` timestamp NOT NULL,
  `sysChangeDate` timestamp NOT NULL,
  `fkID` varchar(32) NOT NULL,
  `GlobalID` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `validatorKYC`
--
ALTER TABLE `validatorKYC`
  ADD PRIMARY KEY (`voteID`);

--
-- Indexes for table `validators`
--
ALTER TABLE `validators`
  ADD PRIMARY KEY (`validatorID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
