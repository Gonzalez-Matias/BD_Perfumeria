vistas_definidas = {
    "productos_por_categoria": {
        "descripcion": "Productos por Categoría",
        "query": """
            SELECT P.nombre AS "%s"
            FROM PRODUCTO P
            JOIN PERTENECE_A PA ON P.idProducto = PA.idProducto
            JOIN CATEGORIA C ON PA.idCategoria = C.idCategoria
            WHERE C.titulo = %s;
        """,
        "params": ["Categoría"] 
    },
    "ingresos_por_producto": {
        "descripcion": "Ingresos por Producto",
        "query": """
            SELECT 
                prod.nombre,
                mov.fechaHoraMov,
                ID.cantUnidades,
                pProd.cantidad,
                pProd.unidades,
                ID.costeUnitario
            FROM INGRESO_DE ID
            JOIN MOVIMIENTO mov ON ID.idMov = mov.idMov
            JOIN PRESENTACION_PRODUCTO pProd ON ID.idPresentacionProd = pProd.idPresentacion
            JOIN PRODUCTO prod ON pProd.idProducto = prod.idProducto
            WHERE prod.idProducto = %s;
        """,
        "params": ["ID Producto"]
    }
}