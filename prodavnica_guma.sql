-- Kreiranje tabele za gume
CREATE TABLE `gume` (
  `id` int(11) NOT NULL,
  `proizvodjac_id` int(11) DEFAULT NULL,
  `kategorija_id` int(11) DEFAULT NULL,
  `model` varchar(100) NOT NULL,
  `sirina` int(11) NOT NULL,
  `visina` int(11) NOT NULL,
  `precnik` int(11) NOT NULL,
  `sezona` enum('Letnja','Zimska','Sve sezone') NOT NULL,
  `cena` decimal(10,2) NOT NULL,
  `kolicina_na_stanju` int(11) DEFAULT 0,
  `slika_url` varchar(255) DEFAULT NULL,
  `popust` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `gume` (`id`, `proizvodjac_id`, `kategorija_id`, `model`, `sirina`, `visina`, `precnik`, `sezona`, `cena`, `kolicina_na_stanju`, `slika_url`, `popust`) VALUES
(1, 1, 1, 'Pilot Sport 4', 205, 55, 16, 'Letnja', 11012.00, 20, 'michelin_pilot_sport.jpg', 10),
(2, 2, 1, 'Greenways', 205, 55, 16, 'Letnja', 5896.00, 40, 'lassa_greenways.jpg', 10),
(3, 2, 1, 'Snoways 4', 205, 55, 16, 'Zimska', 6430.00, 35, 'lassa_snoways.jpg', 10),
(4, 3, 1, 'Cinturato Winter 2', 205, 55, 16, 'Zimska', 10141.20, 15, 'pirelli_cinturato.jpg', 10),
(5, 1, 1, 'Alpin 6', 195, 65, 15, 'Zimska', 11000.00, 20, 'lassa_snoways.jpg', 10),
(6, 1, 1, 'Pilot Sport 5', 225, 45, 17, 'Letnja', 16500.00, 20, 'lassa_greenways.jpg', 10),
(7, 1, 1, 'CrossClimate 2', 205, 55, 16, 'Sve sezone', 13500.00, 20, 'pirelli_cinturato.jpg', 10),
(8, 1, 2, 'Pilot Alpin 5 SUV', 235, 60, 18, 'Zimska', 21000.00, 20, 'lassa_snoways.jpg', 10),
(9, 4, 1, 'Eskimo S3+', 195, 65, 15, 'Zimska', 5500.00, 20, 'lassa_snoways.jpg', 0),
(10, 4, 1, 'Intensa HP2', 205, 55, 16, 'Letnja', 6000.00, 20, 'lassa_greenways.jpg', 0),
(11, 4, 1, 'All Weather', 205, 55, 16, 'Sve sezone', 6500.00, 20, 'pirelli_cinturato.jpg', 0),
(12, 4, 2, 'Eskimo SUV 2', 225, 65, 17, 'Zimska', 10500.00, 20, 'lassa_snoways.jpg', 0),
(13, 5, 1, 'Winter', 195, 65, 15, 'Zimska', 4800.00, 20, 'lassa_snoways.jpg', 0),
(14, 5, 1, 'High Performance', 205, 55, 16, 'Letnja', 5200.00, 20, 'lassa_greenways.jpg', 0),
(15, 5, 1, 'All Season', 205, 55, 16, 'Sve sezone', 5600.00, 20, 'pirelli_cinturato.jpg', 0),
(16, 5, 3, 'CargoSpeed Winter', 205, 75, 16, 'Zimska', 8000.00, 20, 'lassa_snoways.jpg', 0),
(17, 3, 1, 'Cinturato Winter 2', 205, 55, 16, 'Zimska', 12000.00, 20, 'lassa_snoways.jpg', 0),
(18, 3, 1, 'P Zero', 225, 45, 17, 'Letnja', 17000.00, 20, 'lassa_greenways.jpg', 0),
(19, 3, 1, 'Cinturato All Season SF2', 205, 55, 16, 'Sve sezone', 14000.00, 20, 'pirelli_cinturato.jpg', 0),
(20, 3, 2, 'Scorpion Winter', 235, 60, 18, 'Zimska', 22000.00, 20, 'lassa_snoways.jpg', 0),
(21, 6, 1, 'WinterContact TS 870', 205, 55, 16, 'Zimska', 13000.00, 20, 'lassa_snoways.jpg', 0),
(22, 6, 1, 'PremiumContact 7', 225, 45, 17, 'Letnja', 16000.00, 20, 'lassa_greenways.jpg', 0),
(23, 6, 1, 'AllSeasonContact', 205, 55, 16, 'Sve sezone', 14500.00, 20, 'pirelli_cinturato.jpg', 0),
(24, 6, 2, 'CrossContact ATR', 235, 65, 17, 'Letnja', 19000.00, 20, 'lassa_greenways.jpg', 0),
(25, 7, 1, 'Winter Response 2', 195, 65, 15, 'Zimska', 9500.00, 20, 'lassa_snoways.jpg', 0),
(26, 7, 1, 'Sport Bluresponse', 205, 55, 16, 'Letnja', 10500.00, 20, 'lassa_greenways.jpg', 0),
(27, 7, 1, 'Sport All Season', 225, 45, 17, 'Sve sezone', 12500.00, 20, 'pirelli_cinturato.jpg', 0),
(28, 7, 2, 'Winter Sport 5 SUV', 235, 60, 18, 'Zimska', 18500.00, 20, 'lassa_snoways.jpg', 0),
(29, 8, 1, 'UltraGrip 9+', 195, 65, 15, 'Zimska', 10000.00, 20, 'lassa_snoways.jpg', 0),
(30, 8, 1, 'EfficientGrip Performance 2', 205, 55, 16, 'Letnja', 11500.00, 20, 'lassa_greenways.jpg', 0),
(31, 8, 1, 'Vector 4Seasons Gen-3', 225, 45, 17, 'Sve sezone', 13000.00, 20, 'pirelli_cinturato.jpg', 0),
(32, 8, 2, 'UltraGrip Performance+ SUV', 235, 60, 18, 'Zimska', 20000.00, 20, 'lassa_snoways.jpg', 0),
(33, 9, 1, 'Winter i*cept RS3', 205, 55, 16, 'Zimska', 8500.00, 20, 'lassa_snoways.jpg', 0),
(34, 9, 1, 'Ventus Prime 4', 225, 45, 17, 'Letnja', 9500.00, 20, 'lassa_greenways.jpg', 0),
(35, 9, 1, 'Kinergy 4S2', 205, 55, 16, 'Sve sezone', 10000.00, 20, 'pirelli_cinturato.jpg', 0),
(36, 9, 2, 'Winter i*cept evo3 X', 235, 60, 18, 'Zimska', 16000.00, 20, 'lassa_snoways.jpg', 0),
(37, 2, 1, 'Snoways 4', 205, 55, 16, 'Zimska', 6500.00, 20, 'lassa_snoways.jpg', 0),
(38, 2, 1, 'Greenways', 195, 65, 15, 'Letnja', 6000.00, 20, 'lassa_greenways.jpg', 0),
(39, 2, 1, 'Multiways 2', 205, 55, 16, 'Sve sezone', 7000.00, 20, 'pirelli_cinturato.jpg', 0),
(40, 2, 2, 'Competus Winter 2', 225, 65, 17, 'Zimska', 11000.00, 20, 'lassa_snoways.jpg', 0),
(41, 10, 1, 'Blizzak LM005', 205, 55, 16, 'Zimska', 12500.00, 20, 'lassa_snoways.jpg', 0),
(42, 10, 1, 'Turanza T005', 225, 45, 17, 'Letnja', 14500.00, 20, 'lassa_greenways.jpg', 0),
(43, 10, 1, 'Weather Control A005', 205, 55, 16, 'Sve sezone', 13500.00, 20, 'pirelli_cinturato.jpg', 0),
(44, 10, 2, 'Blizzak LM-80 EVO', 235, 60, 18, 'Zimska', 21500.00, 20, 'lassa_snoways.jpg', 0);

-- Kreiranje tabele za kategorije
CREATE TABLE `kategorije` (
  `id` int(11) NOT NULL,
  `naziv` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `kategorije` (`id`, `naziv`) VALUES
(1, 'Putnička vozila'),
(2, 'Džip / SUV'),
(3, 'Kombi vozila');

-- Kreiranje tabele za korisnike
CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL,
  `ime` varchar(50) NOT NULL,
  `prezime` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `lozinka` varchar(255) NOT NULL,
  `adresa` varchar(255) DEFAULT NULL,
  `telefon` varchar(20) DEFAULT NULL,
  `rola` enum('admin','kupac') DEFAULT 'kupac'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Kreiranje tabele za porudzbine
CREATE TABLE `porudzbine` (
  `id` int(11) NOT NULL,
  `ime_prezime` varchar(100) NOT NULL,
  `adresa` varchar(255) NOT NULL,
  `telefon` varchar(20) NOT NULL,
  `ukupna_cena` decimal(10,2) NOT NULL,
  `datum` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Kreiranje tabele za proizvodjace
CREATE TABLE `proizvodjaci` (
  `id` int(11) NOT NULL,
  `naziv` varchar(50) NOT NULL,
  `zemlja_porekla` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `proizvodjaci` (`id`, `naziv`, `zemlja_porekla`) VALUES
(1, 'Michelin', 'Francuska'),
(2, 'Lassa', 'Turska'),
(3, 'Pirelli', 'Italija'),
(4, 'Sava', 'Slovenija'),
(5, 'Tigar', 'Srbija'),
(6, 'Continental', 'Nemačka'),
(7, 'Dunlop', 'Velika Britanija'),
(8, 'Goodyear', 'SAD'),
(9, 'Hankook', 'Južna Koreja'),
(10, 'Bridgestone', 'Japan');

-- Kreiranje tabele za zakazivanje servisa
CREATE TABLE `zakazivanje_servisa` (
  `id` int(11) NOT NULL,
  `ime_prezime` varchar(100) NOT NULL,
  `telefon` varchar(20) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `vozilo` varchar(100) NOT NULL,
  `vrsta_usluge` varchar(100) NOT NULL,
  `datum_servisa` date NOT NULL,
  `status` enum('Na čekanju','Odobreno','Završeno') DEFAULT 'Na čekanju',
  `datum_kreiranja` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `zakazivanje_servisa` (`id`, `ime_prezime`, `telefon`, `email`, `vozilo`, `vrsta_usluge`, `datum_servisa`, `status`, `datum_kreiranja`) VALUES
(2, 'Drago Biorac', '7877', 'dragobiorac@gmail.com', 'Skoda', 'Veliki servis', '2024-03-03', 'Na čekanju', '2026-03-02 17:44:17');

-- Postavljanje primarnih ključeva i indeksa
ALTER TABLE `gume`
  ADD PRIMARY KEY (`id`),
  ADD KEY `proizvodjac_id` (`proizvodjac_id`),
  ADD KEY `kategorija_id` (`kategorija_id`);

ALTER TABLE `kategorije`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `porudzbine`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `proizvodjaci`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `zakazivanje_servisa`
  ADD PRIMARY KEY (`id`);

-- Postavljanje AUTO_INCREMENT vrednosti
ALTER TABLE `gume`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

ALTER TABLE `kategorije`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `korisnici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `porudzbine`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `proizvodjaci`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

ALTER TABLE `zakazivanje_servisa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

-- Dodavanje stranih kljuceva (Relacije)
ALTER TABLE `gume`
  ADD CONSTRAINT `gume_ibfk_1` FOREIGN KEY (`proizvodjac_id`) REFERENCES `proizvodjaci` (`id`),
  ADD CONSTRAINT `gume_ibfk_2` FOREIGN KEY (`kategorija_id`) REFERENCES `kategorije` (`id`);
  commit;