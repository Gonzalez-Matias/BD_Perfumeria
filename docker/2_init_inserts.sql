-- CLIENTE
INSERT INTO CLIENTE (dni, nombre, apellido, telefono)
VALUES
('12345678', 'Juan', 'Pérez', '1234-5678'),
('87654321', 'Ana', 'García', '8765-4321'),
('23456789', 'Lucas', 'Martínez', '1155-7788'),
('34567890', 'Sofía', 'González', '1166-8899'),
('45678901', 'Martín', 'Rodríguez', '1177-9900'),
('56789012', 'Valentina', 'Pérez', '1188-0011');

-- EMPLEADO
INSERT INTO EMPLEADO (cuit, nombre, apellido, mail, telefono)
VALUES
('20123456789', 'Carlos', 'Gómez', 'carlos.gomez@empresa.com', '1122334455'),
('27876543217', 'María', 'López', 'maria.lopez@empresa.com', '9988776655');

-- PROVEEDOR
INSERT INTO PROVEEDOR (idProveedor, nombreEmpresa, nombreContacto, mailContacto, telContacto)
VALUES
('PROV01', 'Proveedora S.A.', 'Luis Fernández', 'lfernandez@proveedora.com', '1133557799'),
('PROV02', 'Distribuidora SRL', 'Laura Torres', 'ltorres@distribuidora.com', '1144668800');

-- PRODUCTO
INSERT INTO PRODUCTO (idProducto, marca, nombre, discontinuado, fechaBaja)
VALUES
('PROD01', 'Acme', 'Perfume Floral', FALSE, NULL),
('PROD02', 'Lux', 'Colonia Fresca', FALSE, NULL),
('PROD03', 'Seda', 'Shampoo', FALSE, NULL),
('PROD04', 'Dove', 'Acondicionador', FALSE, NULL),
('PROD05', 'Luxe', 'Crema Hidratante', FALSE, NULL),
('PROD06', 'Acme', 'Gel de Ducha', FALSE, NULL),
('PROD07', 'Nivea', 'Desodorante', FALSE, NULL),
('PROD08', 'Lux', 'Jabón de Tocador', FALSE, NULL),
('PROD09', 'Seda', 'Spray Capilar', FALSE, NULL),
('PROD10', 'Luxe', 'Serum Facial', FALSE, NULL),
('PROD11', 'Acme', 'Perfume Cítrico', FALSE, NULL),
('PROD12', 'Dove', 'Loción Corporal', FALSE, NULL),
('PROD13', 'Nivea', 'Crema de Manos', FALSE, NULL),
('PROD14', 'Lux', 'Body Splash', FALSE, NULL),
('PROD15', 'Luxe', 'Aceite Corporal', FALSE, NULL),
('PROD16', 'Acme', 'Sales de Baño', FALSE, NULL),
('PROD17', 'Seda', 'Bálsamo Labial', FALSE, NULL);

-- Categorías superiores
INSERT INTO CATEGORIA (idCategoria, titulo, activa, descripcion, idCatSuperior)
VALUES
('CAT00', 'Perfumería', TRUE, 'Categoría principal de productos de fragancias', NULL),
('CAT10', 'Cosmética', TRUE, 'Productos de cosmética y cuidado de la piel', NULL),
('CAT20', 'Higiene y Belleza', TRUE, 'Productos para higiene personal y belleza', NULL);

-- Categorías hijas con jerarquía directa
INSERT INTO CATEGORIA (idCategoria, titulo, activa, descripcion, idCatSuperior)
VALUES
('CAT01', 'Fragancias', TRUE, 'Perfumes y colonias', 'CAT00'),
('CAT02', 'Cuidado Personal', TRUE, 'Shampoo, acondicionadores y productos de baño', 'CAT20'),
('CAT03', 'Hidratación y Cuidado de la Piel', TRUE, 'Cremas, lociones y aceites', 'CAT10'),
('CAT04', 'Maquillaje', TRUE, 'Productos de maquillaje y belleza', 'CAT10');


-- PRESENTACION_PRODUCTO
INSERT INTO PRESENTACION_PRODUCTO (idPresentacion, precioUnitario, cantidad, unidades, stock, stockMinimo, idProducto)
VALUES
('PRES01', 150.00, 50, 'ml', 100, 20, 'PROD01'),
('PRES02', 120.00, 75, 'ml', 80, 15, 'PROD02'),
('PRES03', 350.00, 250, 'ml', 50, 10, 'PROD03'),
('PRES04', 340.00, 250, 'ml', 60, 12, 'PROD04'),
('PRES05', 400.00, 200, 'gr', 45, 10, 'PROD05'),
('PRES06', 220.00, 300, 'ml', 70, 15, 'PROD06'),
('PRES07', 180.00, 50, 'ml', 90, 20, 'PROD07'),
('PRES08', 160.00, 1, 'unid', 85, 18, 'PROD08'),
('PRES09', 275.00, 100, 'ml', 55, 12, 'PROD09'),     
('PRES10', 500.00, 30, 'ml', 40, 10, 'PROD10'),    
('PRES11', 155.00, 50, 'ml', 95, 20, 'PROD11'),      
('PRES12', 300.00, 200, 'ml', 65, 15, 'PROD12'),     
('PRES13', 250.00, 50, 'gr', 75, 18, 'PROD13'),      
('PRES14', 200.00, 150, 'ml', 60, 12, 'PROD14'),    
('PRES15', 350.00, 100, 'ml', 50, 10, 'PROD15'),     
('PRES16', 400.00, 500, 'gr', 45, 10, 'PROD16'),     
('PRES17', 150.00, 15, 'gr', 80, 15, 'PROD17'),
('PRES18', 250.00, 100, 'ml', 80, 15, 'PROD01'),
('PRES19', 200.00, 150, 'ml', 60, 10, 'PROD02'),
('PRES20', 600.00, 500, 'ml', 40, 8, 'PROD03'),
('PRES21', 750.00, 400, 'gr', 30, 5, 'PROD05'),
('PRES22', 300.00, 100, 'ml', 70, 15, 'PROD07'),
('PRES23', 650.00, 1000, 'gr', 10, 2, 'PROD16'),
('PRES24', 400.00, 100, 'gr', 40, 8, 'PROD13'),
('PRES25', 450.00, 3, 'unid', 20, 6, 'PROD08');

-- PERTENECE_A
INSERT INTO PERTENECE_A (idProducto, idCategoria)
VALUES
('PROD01', 'CAT01'), -- Perfume Floral
('PROD02', 'CAT01'), -- Colonia Fresca
('PROD03', 'CAT02'), -- Shampoo
('PROD04', 'CAT02'), -- Acondicionador
('PROD05', 'CAT03'), -- Crema Hidratante
('PROD06', 'CAT02'), -- Gel de Ducha
('PROD07', 'CAT02'), -- Desodorante
('PROD08', 'CAT02'), -- Jabón de Tocador
('PROD09', 'CAT02'), -- Spray Capilar
('PROD10', 'CAT03'), -- Serum Facial
('PROD11', 'CAT01'), -- Perfume Cítrico
('PROD12', 'CAT03'), -- Loción Corporal
('PROD13', 'CAT03'), -- Crema de Manos
('PROD14', 'CAT01'), -- Body Splash
('PROD15', 'CAT03'), -- Aceite Corporal
('PROD16', 'CAT03'), -- Sales de Baño
('PROD17', 'CAT03'); -- Bálsamo Labial

-- MOVIMIENTO
-- Uno para cliente
INSERT INTO MOVIMIENTO (idMov, fechaHoraMov, observacion, cuitEmpleado, dniCliente, idProveedor)
VALUES
('MOV01', '2025-05-15 10:30:00', 'Venta de jabón', '20123456789', '12345678', NULL),
('MOV02', '2025-05-18 14:45:00', 'Compra de detergente', '27876543217', NULL, 'PROV02'),
('MOV03', '2025-05-19 09:15:00', 'Venta de crema hidratante', '20123456789', '23456789', NULL),
('MOV04', '2025-05-22 16:20:00', 'Compra de shampoo', '27876543217', NULL, 'PROV01'),
('MOV05', '2025-05-25 11:00:00', 'Ajuste de stock', '20123456789', NULL, NULL),
('MOV06', '2025-05-27 13:30:00', 'Venta de serum facial', '27876543217', '34567890', NULL),
('MOV07', '2025-05-29 15:10:00', 'Compra de sales de baño', '20123456789', NULL, 'PROV02'),
('MOV08', '2025-05-30 09:50:00', 'Venta de desodorante', '27876543217', '45678901', NULL),
('MOV09', '2025-05-31 14:00:00', 'Ajuste de stock por vencimiento', '20123456789', NULL, NULL),
('MOV10', '2025-06-01 10:45:00', 'Venta de crema de manos', '27876543217', '56789012', NULL);

-- AJUSTE_DE
INSERT INTO AJUSTE_DE (idMov, idPresentacionProd, cantUnidades, tipoAjuste, descripcion)
VALUES
('MOV05', 'PRES06', 5, 'MERMA/ROTURA', 'Envases rotos durante transporte'),
('MOV09', 'PRES12', 3, 'VENCIMIENTO', 'Producto vencido');

-- INGRESO_DE
INSERT INTO INGRESO_DE (idMov, idPresentacionProd, cantUnidades, costeUnitario, descripcion)
VALUES
('MOV02', 'PRES02', 30, 180.00, 'Compra de detergente a proveedor'),
('MOV04', 'PRES03', 40, 300.00, 'Compra de shampoo a proveedor'),
('MOV07', 'PRES16', 20, 350.00, 'Compra de sales de baño');

-- VENTA_DE
INSERT INTO VENTA_DE (idMov, idPresentacionProd, cantUnidades, porcentajeDesc, precioUnitario)
VALUES
('MOV01', 'PRES01', 5, 10.00, 150.00),       -- Venta de jabón
('MOV01', 'PRES12', 2, 0.00, 300.00),       -- Venta de jabón
('MOV03', 'PRES05', 10, 5.00, 400.00),       -- Venta de crema hidratante
('MOV06', 'PRES10', 3, 0.00, 500.00),        -- Venta de serum facial 
('MOV08', 'PRES07', 8, 10.00, 180.00),       -- Venta de desodorante
('MOV10', 'PRES13', 12, 7.50, 250.00);       -- Venta de crema de manos
