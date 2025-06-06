import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import ejecutar_select, ejecutar_modificacion, conectar_db
from queries import vistas_definidas
from config import config


def agregar_producto():
    def guardar():
        id_producto = entry_id.get()
        marca = entry_marca.get()
        nombre = entry_nombre.get()
        discontinuado = entry_discontinuado.get().lower() == "si"
        fecha_baja = entry_fecha.get() or None
        id_categoria = entry_categoria.get() or None

        # Insertar producto
        query_producto = f"""
        INSERT INTO PRODUCTO (idProducto, marca, nombre, discontinuado, fechaBaja)
        VALUES ('{id_producto}', '{marca}', '{nombre}', {1 if discontinuado else 0}, {f"'{fecha_baja}'" if fecha_baja else 'NULL'});
        """
        ejecutar_modificacion(query_producto)

        # Insertar relación categoría (si se especifica)
        if id_categoria:
            query_pertenece = f"""
            INSERT INTO PERTENECE_A (idProducto, idCategoria)
            VALUES ('{id_producto}', '{id_categoria}');
            """
            ejecutar_modificacion(query_pertenece)

        ventana.destroy()
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")

    ventana = tk.Toplevel()
    ventana.title("Agregar Producto")

    campos = [
        ("ID Producto", 0),
        ("Marca", 1),
        ("Nombre", 2),
        ("Discontinuado (si/no)", 3),
        ("Fecha Baja (YYYY-MM-DD) (opcional)", 4),
        ("ID Categoría (opcional)", 5)
    ]
    entries = {}
    for label, row in campos:
        tk.Label(ventana, text=label + ":").grid(row=row, column=0)
        entry = tk.Entry(ventana)
        entry.grid(row=row, column=1)
        entries[label.lower()] = entry

    entry_id = entries["id producto"]
    entry_marca = entries["marca"]
    entry_nombre = entries["nombre"]
    entry_discontinuado = entries["discontinuado (si/no)"]
    entry_fecha = entries["fecha baja (yyyy-mm-dd) (opcional)"]
    entry_categoria = entries["id categoría (opcional)"]

    tk.Button(ventana, text="Guardar", command=guardar).grid(row=6, column=0, columnspan=2, pady=10)

def agregar_presentacion():
    def guardar():
        id_presentacion = entry_id.get()
        precio_unitario = entry_precio.get()
        cantidad = entry_cantidad.get()
        unidades = entry_unidades.get()
        stock = entry_stock.get() or 0
        stock_minimo = entry_stock_min.get() or 0
        id_producto = entry_producto.get()

        query = f"""
        INSERT INTO PRESENTACION_PRODUCTO 
        (idPresentacion, precioUnitario, cantidad, unidades, stock, stockMinimo, idProducto)
        VALUES ('{id_presentacion}', {precio_unitario}, {cantidad}, '{unidades}', {stock}, {stock_minimo}, '{id_producto}');
        """
        ejecutar_modificacion(query)
        ventana.destroy()
        messagebox.showinfo("Éxito", "Presentación de producto agregada correctamente.")

    ventana = tk.Toplevel()
    ventana.title("Agregar Presentación de Producto")

    campos = [
        ("ID Presentación", 0),
        ("Precio Unitario", 1),
        ("Cantidad", 2),
        ("Unidades", 3),
        ("Stock (opcional)", 4),
        ("Stock Mínimo (opcional)", 5),
        ("ID Producto", 6)
    ]
    entries = {}
    for label, row in campos:
        tk.Label(ventana, text=label + ":").grid(row=row, column=0)
        entry = tk.Entry(ventana)
        entry.grid(row=row, column=1)
        entries[label.lower()] = entry

    entry_id = entries["id presentación"]
    entry_precio = entries["precio unitario"]
    entry_cantidad = entries["cantidad"]
    entry_unidades = entries["unidades"]
    entry_stock = entries["stock (opcional)"]
    entry_stock_min = entries["stock mínimo (opcional)"]
    entry_producto = entries["id producto"]

    tk.Button(ventana, text="Guardar", command=guardar).grid(row=7, column=0, columnspan=2, pady=10)

def agregar_movimiento_completo():
    ventana = tk.Toplevel()
    ventana.title("Agregar Movimiento")

    # Movimiento base
    tk.Label(ventana, text="ID Movimiento:").grid(row=0, column=0)
    EntryidMov = tk.Entry(ventana)
    EntryidMov.grid(row=0, column=1)

    tk.Label(ventana, text="Fecha (YYYY-MM-DD HH:MM:SS) (opcional):").grid(row=1, column=0)
    entry_fecha = tk.Entry(ventana)
    entry_fecha.grid(row=1, column=1)

    tk.Label(ventana, text="Observación:").grid(row=2, column=0)
    entry_observacion = tk.Entry(ventana)
    entry_observacion.grid(row=2, column=1)

    tk.Label(ventana, text="CUIT Empleado:").grid(row=3, column=0)
    entry_cuit = tk.Entry(ventana)
    entry_cuit.grid(row=3, column=1)

    tipo_var = tk.StringVar()
    tk.Label(ventana, text="Tipo de Movimiento:").grid(row=4, column=0)
    for i, tipo in enumerate(['Venta', 'Ingreso', 'Ajuste']):
        tk.Radiobutton(ventana, text=tipo, variable=tipo_var, value=tipo).grid(row=4, column=1+i, sticky="w")

    frame_extra = tk.Frame(ventana)
    frame_extra.grid(row=5, column=0, columnspan=3)

    extra_entries = {}

    def actualizar_campos_extra():
        for widget in frame_extra.winfo_children():
            widget.destroy()
        if tipo_var.get() == 'Venta':
            tk.Label(frame_extra, text="DNI Cliente:").grid(row=0, column=0)
            extra_entries['dniCliente'] = tk.Entry(frame_extra)
            extra_entries['dniCliente'].grid(row=0, column=1)
        elif tipo_var.get() == 'Ingreso':
            tk.Label(frame_extra, text="ID Proveedor:").grid(row=0, column=0)
            extra_entries['idProveedor'] = tk.Entry(frame_extra)
            extra_entries['idProveedor'].grid(row=0, column=1)

    tipo_var.trace('w', lambda *args: actualizar_campos_extra())

    # Lista para ítems asociados
    items = []

    def agregar_item():
        sub = tk.Toplevel(ventana)
        sub.title("Agregar Ítem")

        tk.Label(sub, text="ID Presentación:").grid(row=0, column=0)
        entry_pres = tk.Entry(sub)
        entry_pres.grid(row=0, column=1)

        tk.Label(sub, text="Cantidad:").grid(row=1, column=0)
        entry_cant = tk.Entry(sub)
        entry_cant.grid(row=1, column=1)

        fields = {}

        if tipo_var.get() == 'Venta':
            tk.Label(sub, text="Porcentaje Desc.:").grid(row=2, column=0)
            entry_desc = tk.Entry(sub)
            entry_desc.grid(row=2, column=1)

            tk.Label(sub, text="Precio Unitario:").grid(row=3, column=0)
            entry_precio = tk.Entry(sub)
            entry_precio.grid(row=3, column=1)

            fields = {'desc': entry_desc, 'precio': entry_precio}

        elif tipo_var.get() == 'Ingreso':
            tk.Label(sub, text="Coste Unitario:").grid(row=2, column=0)
            entry_coste = tk.Entry(sub)
            entry_coste.grid(row=2, column=1)

            tk.Label(sub, text="Descripción:").grid(row=3, column=0)
            entry_desc = tk.Entry(sub)
            entry_desc.grid(row=3, column=1)

            fields = {'coste': entry_coste, 'desc': entry_desc}

        elif tipo_var.get() == 'Ajuste':
            tk.Label(sub, text="Tipo de Ajuste:").grid(row=2, column=0)
            entry_tipo = tk.Entry(sub)
            entry_tipo.grid(row=2, column=1)

            tk.Label(sub, text="Descripción:").grid(row=3, column=0)
            entry_desc = tk.Entry(sub)
            entry_desc.grid(row=3, column=1)

            fields = {'tipo': entry_tipo, 'desc': entry_desc}

        def guardar_item():
            item = {
                'idPres': entry_pres.get(),
                'cantidad': entry_cant.get(),
                'extra': {k: v.get() for k, v in fields.items()}
            }
            items.append(item)
            sub.destroy()
            messagebox.showinfo("Ítem agregado", "Ítem agregado correctamente.")

        tk.Button(sub, text="Guardar Ítem", command=guardar_item).grid(row=4, column=0, columnspan=2)

    def guardar_movimiento():
        idMov = EntryidMov.get()
        fecha = entry_fecha.get()
        observacion = entry_observacion.get()
        cuit = entry_cuit.get()
        dniCliente = extra_entries.get('dniCliente').get() if 'dniCliente' in extra_entries else None
        idProveedor = extra_entries.get('idProveedor').get() if 'idProveedor' in extra_entries else None

        # Insertar MOVIMIENTO
        if fecha:
            query_mov = """
                INSERT INTO MOVIMIENTO (idMov, fechaHoraMov, observacion, cuitEmpleado, dniCliente, idProveedor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params_mov = (idMov, fecha, observacion, cuit, dniCliente, idProveedor)
        else:
            query_mov = """
                INSERT INTO MOVIMIENTO (idMov, observacion, cuitEmpleado, dniCliente, idProveedor)
                VALUES (%s, %s, %s, %s, %s)
            """
            params_mov = (idMov, observacion, cuit, dniCliente, idProveedor)
        ejecutar_modificacion(query_mov, params_mov)

        # Insertar ítems asociados
        for item in items:
            idPres = item['idPres']
            cantidad = item['cantidad']
            extra = item['extra']

            if tipo_var.get() == 'Venta':
                query_venta = """
                    INSERT INTO VENTA_DE (idMov, idPresentacionProd, cantUnidades, porcentajeDesc, precioUnitario)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params_venta = (idMov, idPres, cantidad, extra['desc'], extra['precio'])
                ejecutar_modificacion(query_venta, params_venta)

            elif tipo_var.get() == 'Ingreso':
                query_ingreso = """
                    INSERT INTO INGRESO_DE (idMov, idPresentacionProd, cantUnidades, costeUnitario, descripcion)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params_ingreso = (idMov, idPres, cantidad, extra['coste'], extra['desc'])
                ejecutar_modificacion(query_ingreso, params_ingreso)

            elif tipo_var.get() == 'Ajuste':
                query_ajuste = """
                    INSERT INTO AJUSTE_DE (idMov, idPresentacionProd, cantUnidades, tipoAjuste, descripcion)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params_ajuste = (idMov, idPres, cantidad, extra['tipo'], extra['desc'])
                ejecutar_modificacion(query_ajuste, params_ajuste)

        messagebox.showinfo("Éxito", "Movimiento y detalles insertados correctamente.")
        ventana.destroy()

    tk.Button(ventana, text="Agregar Ítem", command=agregar_item).grid(row=8, column=0, columnspan=3, pady=5)
    tk.Button(ventana, text="Guardar Movimiento", command=guardar_movimiento).grid(row=9, column=0, columnspan=3, pady=10)

def agregar_empleado():
    def guardar():
        cuit = entry_cuit.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        mail = entry_mail.get()
        telefono = entry_telefono.get()

        query = f"""
        INSERT INTO EMPLEADO (cuit, nombre, apellido, mail, telefono)
        VALUES ('{cuit}', '{nombre}', '{apellido}', '{mail}', '{telefono}');
        """
        ejecutar_modificacion(query)
        ventana_agregar.destroy()

    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Empleado")

    tk.Label(ventana_agregar, text="CUIT:").grid(row=0, column=0)
    entry_cuit = tk.Entry(ventana_agregar)
    entry_cuit.grid(row=0, column=1)

    tk.Label(ventana_agregar, text="Nombre:").grid(row=1, column=0)
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.grid(row=1, column=1)

    tk.Label(ventana_agregar, text="Apellido:").grid(row=2, column=0)
    entry_apellido = tk.Entry(ventana_agregar)
    entry_apellido.grid(row=2, column=1)

    tk.Label(ventana_agregar, text="Mail:").grid(row=3, column=0)
    entry_mail = tk.Entry(ventana_agregar)
    entry_mail.grid(row=3, column=1)

    tk.Label(ventana_agregar, text="Teléfono:").grid(row=4, column=0)
    entry_telefono = tk.Entry(ventana_agregar)
    entry_telefono.grid(row=4, column=1)

    tk.Button(ventana_agregar, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

def agregar_cliente():
    def guardar():
        dni = entry_dni.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        telefono = entry_telefono.get()
        query = f"""
        INSERT INTO CLIENTE (dni, nombre, apellido, telefono)
        VALUES ('{dni}', '{nombre}', '{apellido}', '{telefono}');
        """
        ejecutar_modificacion(query)
        ventana.destroy()

    ventana = tk.Toplevel()
    ventana.title("Agregar Cliente")

    campos = [("DNI", 0), ("Nombre", 1), ("Apellido", 2), ("Teléfono", 3)]
    entries = {}
    for label, row in campos:
        tk.Label(ventana, text=label + ":").grid(row=row, column=0)
        entry = tk.Entry(ventana)
        entry.grid(row=row, column=1)
        entries[label.lower()] = entry

    entry_dni = entries["dni"]
    entry_nombre = entries["nombre"]
    entry_apellido = entries["apellido"]
    entry_telefono = entries["teléfono"]

    tk.Button(ventana, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=10)

def menu_agregar_persona():
    def seleccion(tipo):
        ventana.destroy()
        if tipo == "Cliente":
            agregar_cliente()
        elif tipo == "Empleado":
            agregar_empleado()

    ventana = tk.Toplevel()
    ventana.title("Agregar Persona")

    tk.Label(ventana, text="¿Qué desea agregar?").pack(pady=10)

    btn_cliente = tk.Button(ventana, text="Cliente", command=lambda: seleccion("Cliente"))
    btn_cliente.pack(pady=5)

    btn_empleado = tk.Button(ventana, text="Empleado", command=lambda: seleccion("Empleado"))
    btn_empleado.pack(pady=5)

def mostrar_vista():
    ventana = tk.Toplevel()
    ventana.title("Mostrar Vista")

    conn = conectar_db()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.views WHERE table_schema = %s", (config['database'],))
    vistas_db = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    # Combinar vistas de queries definidas y de la base
    vistas_total = list(vistas_definidas.keys()) + vistas_db

    if not vistas_total:
        messagebox.showinfo("Sin vistas", "No hay vistas definidas.")
        ventana.destroy()
        return

    # Generar un diccionario de nombres bonitos
    vistas_dict = {}
    for vista in vistas_total:
        nombre_bonito = vista.replace("_", " ").capitalize()
        vistas_dict[nombre_bonito] = vista

    tk.Label(ventana, text="Seleccioná una vista:").pack(pady=5)
    lista_vistas = ttk.Combobox(ventana, values=list(vistas_dict.keys()), state="readonly")
    lista_vistas.pack(pady=5)

    def ejecutar_vista():
        seleccion = lista_vistas.get()
        if not seleccion:
            return

        vista_seleccionada = vistas_dict[seleccion]
        if vista_seleccionada in vistas_definidas:
            mostrar_vista_con_parametros(vista_seleccionada)
        else:
            mostrar_vista_sin_parametros(vista_seleccionada)

    tk.Button(ventana, text="Mostrar Vista", command=ejecutar_vista).pack(pady=10)

def mostrar_vista_con_parametros(nombre_vista):
    vista = vistas_definidas[nombre_vista]
    params_values = []
    for param in vista['params']:
        value = simpledialog.askstring(param, f"Ingrese el valor para '{param}':")
        if value is None:
            return
        params_values.append(value)

    # Duplicar el valor si se repite en la consulta
    if vista['query'].count('%s') > len(params_values):
        # Duplicamos el primer valor (o todos los que sean necesarios)
        while len(params_values) < vista['query'].count('%s'):
            params_values.append(params_values[0])

    conn = conectar_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(vista['query'], params_values)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
    except Exception as err:
        messagebox.showerror("Error", f"No se pudo ejecutar la vista:\n{err}")
        return
    finally:
        cursor.close()
        conn.close()

    mostrar_resultados(f"Vista: {vista['descripcion']}", columnas, resultados)
def mostrar_vista_sin_parametros(vista_nombre):
    conn = conectar_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {vista_nombre}")
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
    except Exception as err:
        messagebox.showerror("Error", f"No se pudo ejecutar la vista:\n{err}")
        return
    finally:
        cursor.close()
        conn.close()

    mostrar_resultados(f"Vista: {vista_nombre}", columnas, resultados)

def mostrar_resultados(titulo, columnas, filas):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    for fila in filas:
        tree.insert("", tk.END, values=fila)
    tree.pack(expand=True, fill='both')