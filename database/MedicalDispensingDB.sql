-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 19, 2025 at 06:17 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `MedicalDispensingDB`
--

-- --------------------------------------------------------

--
-- Table structure for table `Carers`
--

CREATE TABLE `Carers` (
  `CarerID` int(11) NOT NULL,
  `PatientID` varchar(10) DEFAULT NULL,
  `TypeofCarer` varchar(50) DEFAULT NULL,
  `PreferredContactMethod` varchar(50) DEFAULT NULL,
  `PhoneNumber` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Carers`
--

INSERT INTO `Carers` (`CarerID`, `PatientID`, `TypeofCarer`, `PreferredContactMethod`, `PhoneNumber`, `Email`) VALUES
(10, 'A001', 'NHS', 'Email', '020 3299 9000', 'kchadherance@nhs.net'),
(11, 'A001', 'NHS', 'Email', '020 3299 9000', 'kchadherance@nhs.net'),
(12, 'B002', 'Family', 'SMS', '077 1234 5678', 'familyb002@outlook.com'),
(13, 'C003', 'Family', 'SMS', '077 2345 6789', 'familyc003@outlook.com'),
(14, 'D004', 'Self-care', 'Email', '7074746090', 'tessdunn@outlook.co'),
(15, 'E005', 'NHS', 'SMS', '020 3299 9000', 'kchadherance@nhs.net'),
(16, 'F006', 'Family', 'Email', '077 3456 7890', 'familyf006@outlook.co'),
(17, 'G007', 'Self-care', 'Email', '7844106799', 'khadijaahmed@outlook.co'),
(18, 'H008', 'NHS', 'SMS', '020 3299 9000', 'kchadherance@nhs.net'),
(19, 'I009', 'Self-care', 'Email', '7729569783', 'munaMuhumed410@outlook.com'),
(20, 'J0010', 'Self Carer', 'Email', '+44 7911 123456', 'taylor.bennett@gmail.com'),
(21, 'K0011', 'NHS', 'SMS', '+44 7911 654321', 'jordan.clarke@hotmail.co.uk'),
(22, 'L0012', 'Family', 'Email', '+44 7911 987654', 'avery.morgan@outlook.com'),
(23, 'M0013', 'Self Carer', 'SMS', '+44 7911 321987', 'casey.taylor@gmail.com'),
(24, 'N0014', 'NHS', 'Email', '+44 7911 456789', 'jamie.lee@hotmail.co.uk'),
(25, 'O0015', 'Family', 'SMS', '+44 7911 654987', 'riley.smith@outlook.com'),
(26, 'P0016', 'Self Carer', 'Email', '+44 7911 987321', 'morgan.white@gmail.com'),
(27, 'Q0017', 'NHS', 'SMS', '+44 7911 321654', 'alex.johnson@hotmail.co.uk'),
(28, 'R0018', 'Family', 'Email', '+44 7911 456123', 'sam.brown@outlook.com'),
(29, 'S0019', 'Self Carer', 'SMS', '+44 7911 654654', 'jamie.green@gmail.com'),
(30, 'T0020', 'NHS', 'Email', '+44 7911 987987', 'avery.davis@hotmail.co.uk'),
(31, 'U0021', 'Family', 'SMS', '+44 7911 321321', 'jordan.thompson@outlook.com'),
(32, 'V0022', 'Self Carer', 'Email', '+44 7911 456456', 'casey.martin@gmail.com'),
(33, 'W0023', 'NHS', 'SMS', '+44 7911 654321', 'taylor.wilson@hotmail.co.uk'),
(34, 'X0024', 'Family', 'Email', '+44 7911 987654', 'jamie.harris@outlook.com');

-- --------------------------------------------------------

--
-- Table structure for table `Medication`
--

CREATE TABLE `Medication` (
  `MedicationID` int(11) NOT NULL,
  `PatientID` varchar(10) DEFAULT NULL,
  `MedTypeID` int(11) DEFAULT NULL,
  `HealthCondition` varchar(255) DEFAULT NULL,
  `DosageTime` varchar(50) DEFAULT NULL,
  `Colour` varchar(20) DEFAULT NULL,
  `Status` varchar(100) DEFAULT NULL,
  `MedicationStartDate` date DEFAULT NULL,
  `MedicationEndDate` date DEFAULT NULL,
  `CourseType` varchar(50) DEFAULT NULL,
  `NotificationSent` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Medication`
--

INSERT INTO `Medication` (`MedicationID`, `PatientID`, `MedTypeID`, `HealthCondition`, `DosageTime`, `Colour`, `Status`, `MedicationStartDate`, `MedicationEndDate`, `CourseType`, `NotificationSent`) VALUES
(1, 'A001', 1, 'Coronary artery disease', '08:00, 20:00', 'Red', 'Missed, On Time', '2023-01-16', NULL, 'Chronic', 1),
(2, 'A001', 2, 'Respiratory infections', '14:00', 'Green', 'On Time', '2024-02-14', '2024-03-14', 'Non-Chronic', 0),
(3, 'B002', 3, 'Hypothyroidism', '09:00, 21:00', 'Blue', 'Missed, Missed', '2020-03-17', NULL, 'Chronic', 1),
(4, 'C003', 4, 'Heart failure', '07:30', 'Yellow', 'Missed', '2015-04-18', NULL, 'Chronic', 1),
(5, 'D004', 5, 'PCOS', '13:00', 'Violet', 'On Time', '2019-05-22', NULL, 'Chronic', 0),
(6, 'E005', 6, 'Chronic pain management', '11:00, 22:00', 'Orange', 'On Time, Missed', '2021-06-18', '2025-07-03', 'Non-Chronic', 1),
(7, 'F006', 7, 'Stomach ulcers', '10:00, 16:00', 'Indigo', 'On Time, On Time', '2024-12-12', '2025-05-12', 'Non-Chronic', 0),
(8, 'G007', 8, 'Cardiovascular disease prevention', '15:00', 'White', 'Missed', '2018-08-18', NULL, 'Chronic', 1),
(9, 'H008', 3, 'Thyroid cancer', '18:00', 'Purple', 'On Time', '2016-09-03', NULL, 'Chronic', 0),
(10, 'H008', 4, 'High blood pressure', '08:00, 16:00', 'Pink', 'On Time, On Time', '2016-10-18', NULL, 'Chronic', 0),
(11, 'I009', 5, 'Type 2 Diabetes', '19:15', 'Brown', 'Missed', '2017-11-18', NULL, 'Chronic', 1),
(12, 'J0010', 1, 'Coronary artery disease', '08:00, 20:00', 'Red', 'On Time, On Time', '2023-01-16', NULL, 'Chronic', 0),
(13, 'K0011', 2, 'Respiratory infections', '14:00', 'Green', 'On Time', '2024-02-14', '2024-03-14', 'Non-Chronic', 0),
(14, 'L0012', 3, 'Hypothyroidism', '09:00, 21:00', 'Blue', 'Missed, Missed', '2020-03-17', NULL, 'Chronic', 1),
(15, 'M0013', 4, 'Heart failure', '07:30', 'Yellow', 'On Time', '2015-04-18', NULL, 'Chronic', 0),
(16, 'N0014', 5, 'PCOS', '13:00', 'Violet', 'On Time', '2019-05-22', NULL, 'Chronic', 0),
(17, 'O0015', 6, 'Chronic pain management', '11:00, 22:00', 'Orange', 'On Time, Missed', '2021-06-18', '2025-07-03', 'Non-Chronic', 1),
(18, 'P0016', 7, 'Stomach ulcers', '10:00, 16:00', 'Indigo', 'On Time, On Time', '2024-12-12', '2025-05-12', 'Non-Chronic', 0),
(19, 'Q0017', 8, 'Cardiovascular disease prevention', '15:00', 'White', 'Missed', '2018-08-18', NULL, 'Chronic', 1),
(20, 'R0018', 9, 'Thyroid cancer', '18:00', 'Purple', 'On Time', '2016-09-03', NULL, 'Chronic', 0),
(21, 'S0019', 10, 'High blood pressure', '08:00, 16:00', 'Pink', 'On Time, On Time', '2016-10-18', NULL, 'Chronic', 0),
(22, 'T0020', 10, 'High Cholesterol', '08:00 AM', 'White', 'On Time', '2023-08-01', NULL, 'Chronic', 0),
(23, 'U0021', 13, 'Alzheimer’s Disease', '09:00 AM', 'Yellow', 'On Time', '2023-08-10', NULL, 'Chronic', 0),
(24, 'V0022', 5, 'Type 2 Diabetes', 'Twice Daily', 'Blue', 'On Time, On Time', '2023-08-15', NULL, 'Chronic', 0),
(25, 'W0023', 9, 'Neuropathic Pain', 'Evening', 'Red', 'On Time', '2023-08-20', '2024-08-19', 'Non-Chronic', 0),
(26, 'X0024', 14, 'Bacterial Infection', 'Morning', 'Orange', 'On Time', '2023-08-25', '2023-09-24', 'Acute', 0);

-- --------------------------------------------------------

--
-- Table structure for table `MedicationTypes`
--

CREATE TABLE `MedicationTypes` (
  `MedTypeID` int(11) NOT NULL,
  `MedName` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `MedicationTypes`
--

INSERT INTO `MedicationTypes` (`MedTypeID`, `MedName`) VALUES
(1, 'Amlodipine Besylate'),
(2, 'Azithromycin'),
(3, 'Levothyroxine'),
(4, 'Lisinopril'),
(5, 'Metformin'),
(6, 'Hydrocodone'),
(7, 'Omeprazole'),
(8, 'Simvastatin'),
(9, 'Gabapentin'),
(10, 'Atorvastatin'),
(11, 'Warfarin'),
(12, 'Sertraline'),
(13, 'Donepezil'),
(14, 'Metformin'),
(15, 'Ciprofloxacin');

-- --------------------------------------------------------

--
-- Table structure for table `Patients`
--

CREATE TABLE `Patients` (
  `PatientID` varchar(10) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Patients`
--

INSERT INTO `Patients` (`PatientID`, `Name`, `DateOfBirth`, `Gender`, `Age`) VALUES
('A001', 'Abir Mohamed', '1958-03-11', 'Female', 66),
('B002', 'John Smith', '1950-08-12', 'Male', 74),
('C003', 'Annabel Key', '1950-08-03', 'Female', 74),
('D004', 'Tess Dunn', '1948-04-24', 'Female', 76),
('E005', 'Lilia Rowe', '1940-07-25', 'Female', 84),
('F006', 'Aaryan Mcclain', '1952-06-15', 'Male', 72),
('G007', 'Khadija Ahmed', '1943-01-05', 'Female', 82),
('H008', 'Zubair Horne', '1958-02-12', 'Male', 66),
('I009', 'Muna Muhumed', '1960-12-03', 'Female', 64),
('J0010', 'Taylor Bennett', '1971-01-15', 'Female', 52),
('K0011', 'Jordan Clarke', '1969-05-22', 'Male', 54),
('L0012', 'Avery Morgan', '1970-10-30', 'Female', 53),
('M0013', 'Casey Taylor', '1968-03-18', 'Male', 55),
('N0014', 'Jamie Lee', '1972-06-12', 'Female', 51),
('O0015', 'Riley Smith', '1969-09-05', 'Male', 54),
('P0016', 'Morgan White', '1971-02-25', 'Female', 52),
('Q0017', 'Alex Johnson', '1970-11-11', 'Male', 53),
('R0018', 'Sam Brown', '1968-08-14', 'Female', 55),
('S0019', 'Jamie Green', '1973-04-20', 'Male', 50),
('T0020', 'Avery Davis', '1971-07-30', 'Female', 52),
('U0021', 'Jordan Thompson', '1969-12-05', 'Male', 54),
('V0022', 'Casey Martin', '1970-03-09', 'Female', 53),
('W0023', 'Taylor Wilson', '1968-10-18', 'Male', 55),
('X0024', 'Jamie Harris', '1972-01-28', 'Female', 51);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Carers`
--
ALTER TABLE `Carers`
  ADD PRIMARY KEY (`CarerID`),
  ADD KEY `PatientID` (`PatientID`);

--
-- Indexes for table `Medication`
--
ALTER TABLE `Medication`
  ADD PRIMARY KEY (`MedicationID`),
  ADD KEY `MedTypeID` (`MedTypeID`);

--
-- Indexes for table `MedicationTypes`
--
ALTER TABLE `MedicationTypes`
  ADD PRIMARY KEY (`MedTypeID`);

--
-- Indexes for table `Patients`
--
ALTER TABLE `Patients`
  ADD PRIMARY KEY (`PatientID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Carers`
--
ALTER TABLE `Carers`
  MODIFY `CarerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `Medication`
--
ALTER TABLE `Medication`
  MODIFY `MedicationID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Carers`
--
ALTER TABLE `Carers`
  ADD CONSTRAINT `carers_ibfk_1` FOREIGN KEY (`PatientID`) REFERENCES `Patients` (`PatientID`);

--
-- Constraints for table `Medication`
--
ALTER TABLE `Medication`
  ADD CONSTRAINT `medication_ibfk_1` FOREIGN KEY (`MedTypeID`) REFERENCES `MedicationTypes` (`MedTypeID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
