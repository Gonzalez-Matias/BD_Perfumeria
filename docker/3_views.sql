-- VISTA 1: Productos activos con sus categorías
CREATE OR REPLACE VIEW vista_productos_activos AS
SELECT 
    prod.idproducto, 
    prod.nombre, 
    prod.marca, 
    cat.titulo
FROM PRODUCTO prod 
JOIN PERTENECE_A pert ON prod.idProducto = pert.idProducto
LEFT JOIN CATEGORIA cat ON pert.idCategoria = cat.idCategoria
WHERE prod.discontinuado = 0;

-- VISTA 2: Presentaciones con stock bajo mínimo
CREATE OR REPLACE VIEW vista_stock_bajo AS
SELECT 
    idPresentacion, 
    idProducto, 
    stock, 
    stockMinimo
FROM PRESENTACION_PRODUCTO
WHERE stock < stockMinimo;

-- VISTA 3: Listado de empleados
CREATE OR REPLACE VIEW vista_empleados AS
SELECT 
    cuit, 
    nombre, 
    apellido, 
    mail, 
    telefono
FROM EMPLEADO;

-- VISTA 4: Listado de clientes
CREATE OR REPLACE VIEW vista_clientes AS
SELECT 
    dni, 
    nombre, 
    apellido, 
    telefono
FROM CLIENTE;

-- VISTA 5: Listado de proveedores
CREATE OR REPLACE VIEW vista_proveedores AS
SELECT 
    idProveedor, 
    nombreEmpresa, 
    nombreContacto, 
    mailContacto, 
    telContacto
FROM PROVEEDOR;

-- VISTA 5: Listado de movimientos
CREATE OR REPLACE VIEW vista_movimientos AS
SELECT 
    m.idMov,
    m.fechaHoraMov,
    m.precioTotal,
    CASE
        WHEN EXISTS (SELECT 1 FROM VENTA_DE v WHERE v.idMov = m.idMov) THEN 'Venta'
        WHEN EXISTS (SELECT 1 FROM INGRESO_DE i WHERE i.idMov = m.idMov) THEN 'Ingreso'
        WHEN EXISTS (SELECT 1 FROM AJUSTE_DE a WHERE a.idMov = m.idMov) THEN 'Ajuste'
        ELSE 'Desconocido'
    END AS tipoMovimiento,
    e.cuit AS cuitEmpleado,
    e.nombre AS nombreEmpleado
FROM MOVIMIENTO m
JOIN EMPLEADO e ON m.cuitEmpleado = e.cuit;