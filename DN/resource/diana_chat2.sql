-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 24-08-2023 a las 22:23:29
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `diana.chat2`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cajeros`
--

CREATE TABLE `cajeros` (
  `id_cajero` int(11) NOT NULL COMMENT 'identificador unico',
  `nombre_cajero` text NOT NULL COMMENT 'nombre y apellido del cajero(cliente).',
  `celular` varchar(255) NOT NULL COMMENT 'Numero de celular del cajero. El mismo numero con el q se va a contactar con diana.',
  `mail` varchar(255) NOT NULL COMMENT 'Mail del cajero(cliente). Necesario para enviar facturas del servicio y reportes de actualizaciones.',
  `plan` text NOT NULL COMMENT 'Plan de servicio adquirido. planes:\r\n1)Plan starter.\r\n2)Plan automático.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cajeros`
--

INSERT INTO `cajeros` (`id_cajero`, `nombre_cajero`, `celular`, `mail`, `plan`) VALUES
(7, 'Cajero One', '+54 9 11 5851-0454', '+54 9 11 5851-0454@', 'starter');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plataformas`
--

CREATE TABLE `plataformas` (
  `id_plataforma` int(11) NOT NULL,
  `nombre_plataforma` varchar(20) NOT NULL COMMENT '	'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `plataformas`
--

INSERT INTO `plataformas` (`id_plataforma`, `nombre_plataforma`) VALUES
(3, '24live'),
(4, 'camelBet'),
(1, 'jugalo'),
(2, 'siempregana');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros`
--

CREATE TABLE `registros` (
  `id_registro` int(11) NOT NULL,
  `id_cajero` int(11) NOT NULL,
  `nombre_plataf` varchar(20) NOT NULL,
  `operacion` varchar(11) NOT NULL,
  `monto` int(11) NOT NULL,
  `usuario` varchar(20) NOT NULL,
  `fecha_hora` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `registros`
--

INSERT INTO `registros` (`id_registro`, `id_cajero`, `nombre_plataf`, `operacion`, `monto`, `usuario`, `fecha_hora`) VALUES
(72, 7, 'camelBet', 'carga', 1000, 'samuel33a3', '2023-08-21 20:24:20');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `id_cajero` int(11) NOT NULL COMMENT 'Clave foránea. Toma el id_cajero de la tabla cajeros. Objetivo: identificar los usuarios de cada cajero.',
  `usuario` varchar(50) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `id_plataforma` int(20) NOT NULL COMMENT '1: jugalo.net\r\n2: siempregana.net\r\n3: megafaraon.com'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `id_cajero`, `usuario`, `clave`, `id_plataforma`) VALUES
(19, 7, 'pepa123b', 'pipo123bb', 1),
(20, 7, 'botcasino99', 'bot99casino', 4);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cajeros`
--
ALTER TABLE `cajeros`
  ADD PRIMARY KEY (`id_cajero`);

--
-- Indices de la tabla `plataformas`
--
ALTER TABLE `plataformas`
  ADD PRIMARY KEY (`id_plataforma`),
  ADD KEY `nombre_plataforma` (`nombre_plataforma`);

--
-- Indices de la tabla `registros`
--
ALTER TABLE `registros`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `id_cajero` (`id_cajero`),
  ADD KEY `nombre_plataf` (`nombre_plataf`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `id_cajero` (`id_cajero`),
  ADD KEY `usuarios_ibfk_3` (`id_plataforma`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cajeros`
--
ALTER TABLE `cajeros`
  MODIFY `id_cajero` int(11) NOT NULL AUTO_INCREMENT COMMENT 'identificador unico', AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `plataformas`
--
ALTER TABLE `plataformas`
  MODIFY `id_plataforma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `registros`
--
ALTER TABLE `registros`
  MODIFY `id_registro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `registros`
--
ALTER TABLE `registros`
  ADD CONSTRAINT `registros_ibfk_1` FOREIGN KEY (`id_cajero`) REFERENCES `cajeros` (`id_cajero`) ON UPDATE CASCADE,
  ADD CONSTRAINT `registros_ibfk_2` FOREIGN KEY (`nombre_plataf`) REFERENCES `plataformas` (`nombre_plataforma`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_cajero`) REFERENCES `cajeros` (`id_cajero`) ON UPDATE CASCADE,
  ADD CONSTRAINT `usuarios_ibfk_3` FOREIGN KEY (`id_plataforma`) REFERENCES `plataformas` (`id_plataforma`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
