-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           8.0.18 - MySQL Community Server - GPL
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Copiando estrutura do banco de dados para cbrs
CREATE DATABASE IF NOT EXISTS `cbrs` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cbrs`;

-- Copiando estrutura para tabela cbrs.cbrs
CREATE TABLE IF NOT EXISTS `cbrs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CHV` varchar(255) DEFAULT '0',
  `CNPJ_C010` varchar(255) DEFAULT '0',
  `DATA` varchar(255) DEFAULT '0',
  `cod_item` varchar(255) DEFAULT '0',
  `desc_item` varchar(255) DEFAULT '0',
  `vl_item` varchar(255) DEFAULT '0',
  `CFOP` varchar(255) DEFAULT '0',
  `CST_PIS` varchar(255) DEFAULT '0',
  `VL_BC_PIS` varchar(255) DEFAULT '0',
  `ALIQ_PIS` varchar(255) DEFAULT '0',
  `QUANT_BC_PIS` varchar(255) DEFAULT '0',
  `VL_PIS` varchar(255) DEFAULT '0',
  `CST_COFINS` varchar(255) DEFAULT '0',
  `VL_BC_COFINS` varchar(255) DEFAULT '0',
  `ALI_COFINS` varchar(255) DEFAULT '0',
  `QUANT_BC_COFINS` varchar(255) DEFAULT '0',
  `VL_CONFIS` varchar(255) DEFAULT '0',
  `DESC_0200` varchar(255) DEFAULT '0',
  `TIOPO_ITEM` varchar(255) DEFAULT '0',
  `COD_NCM` varchar(255) DEFAULT '0',
  `NOME_PART` varchar(255) DEFAULT NULL,
  `CNPJ_PART` varchar(255) DEFAULT NULL,
  `CPF_PART` varchar(255) DEFAULT NULL,
  `COD_MUNIC_PART` varchar(255) DEFAULT NULL,
  `MUNICIPIO` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Exportação de dados foi desmarcado.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
