-- TABLAS
CREATE TABLE CLIENTE (
    dni VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE EMPLEADO (
    cuit VARCHAR(12) PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    mail VARCHAR(36) NOT NULL,
    telefono VARCHAR(24) NOT NULL
);

CREATE TABLE PROVEEDOR (
    idProveedor VARCHAR(10) PRIMARY KEY,
    nombreEmpresa VARCHAR(20) NOT NULL,
    nombreContacto VARCHAR(20) NOT NULL,
    mailContacto VARCHAR(36) NOT NULL,
    telContacto VARCHAR(24) NOT NULL
);

CREATE TABLE PRODUCTO (
    idProducto VARCHAR(10) PRIMARY KEY,
    marca VARCHAR(20) NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    discontinuado BOOLEAN NOT NULL,
    fechaBaja DATE
);

CREATE TABLE CATEGORIA (
    idCategoria VARCHAR(10) PRIMARY KEY ,
    titulo TEXT NOT NULL,
    activa BOOLEAN NOT NULL,
    descripcion TEXT,
    idCatSuperior VARCHAR(10),
    FOREIGN KEY (idCatSuperior) REFERENCES CATEGORIA(idCategoria)
);

CREATE TABLE PRESENTACION_PRODUCTO (
    idPresentacion VARCHAR(10) PRIMARY KEY,
    precioUnitario DECIMAL(10,2) NOT NULL CHECK (precioUnitario > 0),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    unidades VARCHAR(4) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    stockMinimo INT NOT NULL DEFAULT 0,
    idProducto VARCHAR(10) NOT NULL,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto)
);

CREATE TABLE PERTENECE_A (
    idProducto VARCHAR(10) NOT NULL,
    idCategoria VARCHAR(10) NOT NULL,
    PRIMARY KEY (idProducto, idCategoria),
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto),
    FOREIGN KEY (idCategoria) REFERENCES CATEGORIA(idCategoria)
);

CREATE TABLE MOVIMIENTO (
    idMov VARCHAR(10) PRIMARY KEY,
    precioTotal DECIMAL(10,2) NOT NULL DEFAULT 0.00 CHECK (precioTotal >= 0),
    fechaHoraMov DATETIME NOT NULL DEFAULT CURRENT_DATE(),
    observacion TEXT,
    cuitEmpleado VARCHAR(12) NOT NULL,
    dniCliente VARCHAR(10),
    idProveedor VARCHAR(10),
    FOREIGN KEY (cuitEmpleado) REFERENCES EMPLEADO(cuit),
    FOREIGN KEY (dniCliente) REFERENCES CLIENTE(dni),
    FOREIGN KEY (idProveedor) REFERENCES PROVEEDOR(idProveedor),
    CHECK (
        NOT (dniCliente IS NOT NULL AND idProveedor IS NOT NULL)
    )
);

CREATE TABLE AJUSTE_DE (
    idMov VARCHAR(10) NOT NULL,
    idPresentacionProd VARCHAR(10) NOT NULL,
    cantUnidades INT NOT NULL CHECK (cantUnidades > 0),
    tipoAjuste VARCHAR(20) NOT NULL CHECK (tipoAjuste IN ('MERMA/ROTURA', 'VENCIMIENTO', 'PERDIDA')),
    descripcion TEXT NOT NULL,
    PRIMARY KEY (idMov, idPresentacionProd),
    FOREIGN KEY (idMov) REFERENCES MOVIMIENTO(idMov),
    FOREIGN KEY (idPresentacionProd) REFERENCES PRESENTACION_PRODUCTO(idPresentacion)
);

CREATE TABLE INGRESO_DE (
    idMov VARCHAR(10) NOT NULL,
    idPresentacionProd VARCHAR(10) NOT NULL,
    cantUnidades INT NOT NULL CHECK (cantUnidades > 0),
    costeUnitario DECIMAL(10,2) NOT NULL CHECK (costeUnitario > 0),
    descripcion TEXT,
    PRIMARY KEY (idMov, idPresentacionProd),
    FOREIGN KEY (idMov) REFERENCES MOVIMIENTO(idMov),
    FOREIGN KEY (idPresentacionProd) REFERENCES PRESENTACION_PRODUCTO(idPresentacion)
);

CREATE TABLE VENTA_DE (
    idMov VARCHAR(10) NOT NULL,
    idPresentacionProd VARCHAR(10) NOT NULL,
    cantUnidades INT NOT NULL CHECK (cantUnidades > 0),
    porcentajeDesc DECIMAL(5,2) DEFAULT 0,
    precioUnitario DECIMAL(10,2) NOT NULL CHECK (precioUnitario > 0),
    PRIMARY KEY (idMov, idPresentacionProd),
    FOREIGN KEY (idMov) REFERENCES MOVIMIENTO(idMov),
    FOREIGN KEY (idPresentacionProd) REFERENCES PRESENTACION_PRODUCTO(idPresentacion)
);

DELIMITER $$

-- TRIGGERS
-- INGRESO_DE: suma al stock
CREATE TRIGGER tr_ingreso_de_insert_inv
AFTER INSERT ON INGRESO_DE
FOR EACH ROW
BEGIN
    UPDATE PRESENTACION_PRODUCTO
    SET stock = stock + NEW.cantUnidades
    WHERE idPresentacion = NEW.idPresentacionProd;
END$$

CREATE TRIGGER tr_ingreso_de_update_inv
AFTER UPDATE ON INGRESO_DE
FOR EACH ROW
BEGIN
    UPDATE PRESENTACION_PRODUCTO
    SET stock = stock - OLD.cantUnidades + NEW.cantUnidades
    WHERE idPresentacion = NEW.idPresentacionProd;
END$$

-- VENTA_DE: resta del stock
CREATE TRIGGER tr_venta_de_insert_inv
AFTER INSERT ON VENTA_DE
FOR EACH ROW
BEGIN
    UPDATE PRESENTACION_PRODUCTO
    SET stock = stock - NEW.cantUnidades
    WHERE idPresentacion = NEW.idPresentacionProd;
END$$

CREATE TRIGGER tr_venta_de_update_inv
AFTER UPDATE ON VENTA_DE
FOR EACH ROW
BEGIN
    UPDATE PRESENTACION_PRODUCTO
    SET stock = stock + OLD.cantUnidades - NEW.cantUnidades
    WHERE idPresentacion = NEW.idPresentacionProd;
END$$

-- AJUSTE_DE: resta del stock
CREATE TRIGGER tr_ajuste_de_insert
AFTER INSERT ON AJUSTE_DE
FOR EACH ROW
BEGIN
    UPDATE PRESENTACION_PRODUCTO
    SET stock = stock - NEW.cantUnidades
    WHERE idPresentacion = NEW.idPresentacionProd;
END$$

CREATE TRIGGER tr_ajuste_de_update
AFTER UPDATE ON AJUSTE_DE
FOR EACH ROW
BEGIN
    UPDATE PRESENTACION_PRODUCTO
    SET stock = stock + OLD.cantUnidades - NEW.cantUnidades
    WHERE idPresentacion = NEW.idPresentacionProd;
END$$

CREATE TRIGGER tr_venta_de_insert
AFTER INSERT ON VENTA_DE
FOR EACH ROW
BEGIN
    DECLARE totalVenta DECIMAL(10,2);
    -- Calculamos el total sumando todas las líneas del movimiento aplicando descuento
    SELECT 
        SUM(precioUnitario * cantUnidades * (1 - (porcentajeDesc / 100)))
    INTO totalVenta
    FROM VENTA_DE
    WHERE idMov = NEW.idMov;

    -- Actualizamos el precioTotal en MOVIMIENTO
    UPDATE MOVIMIENTO
    SET precioTotal = totalVenta
    WHERE idMov = NEW.idMov;
END$$

CREATE TRIGGER tr_venta_de_update
AFTER UPDATE ON VENTA_DE
FOR EACH ROW
BEGIN
    DECLARE totalVenta DECIMAL(10,2);
    -- Calculamos el total sumando todas las líneas del movimiento aplicando descuento
    SELECT 
        SUM(precioUnitario * cantUnidades * (1 - (porcentajeDesc / 100)))
    INTO totalVenta
    FROM VENTA_DE
    WHERE idMov = NEW.idMov;

    -- Actualizamos el precioTotal en MOVIMIENTO
    UPDATE MOVIMIENTO
    SET precioTotal = totalVenta
    WHERE idMov = NEW.idMov;
END$$

CREATE TRIGGER tr_ingreso_de_insert
AFTER INSERT ON INGRESO_DE
FOR EACH ROW
BEGIN
    DECLARE totalIngreso DECIMAL(10,2);
    -- Calculamos el total sumando todas las líneas del movimiento
    SELECT 
        SUM(costeUnitario * cantUnidades)
    INTO totalIngreso
    FROM INGRESO_DE
    WHERE idMov = NEW.idMov;

    -- Actualizamos el precioTotal en MOVIMIENTO
    UPDATE MOVIMIENTO
    SET precioTotal = totalIngreso
    WHERE idMov = NEW.idMov;
END$$

CREATE TRIGGER tr_ingreso_de_update
AFTER UPDATE ON INGRESO_DE
FOR EACH ROW
BEGIN
    DECLARE totalIngreso DECIMAL(10,2);
    -- Calculamos el total sumando todas las líneas del movimiento
    SELECT 
        SUM(costeUnitario * cantUnidades)
    INTO totalIngreso
    FROM INGRESO_DE
    WHERE idMov = NEW.idMov;

    -- Actualizamos el precioTotal en MOVIMIENTO
    UPDATE MOVIMIENTO
    SET precioTotal = totalIngreso
    WHERE idMov = NEW.idMov;
END$$

DELIMITER ;