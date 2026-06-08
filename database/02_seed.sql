INSERT INTO viviendas (direccion, sector, numero_casa) VALUES
('Casa 14, Sector B', 'Sector B', '14'),
('Casa 25, Sector A', 'Sector A', '25'),
('Apartamento 3, Torre 1', 'Torre 1', '3')
ON CONFLICT (direccion) DO NOTHING;
