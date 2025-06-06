
# Sistema de Gestión para Perfumería

Este proyecto es una aplicación de escritorio desarrollada en Python con Tkinter que permite gestionar productos, movimientos y vistas de una base de datos MariaDB. La base de datos se ejecuta en un contenedor Docker para facilitar el despliegue y la portabilidad.

---

## 📦 Estructura del Proyecto

```
proyecto/
├── main.py
├── views.py
├── db.py
├── config.py
├── queries.py
├── docker-compose.yml
├── docker/
│   ├── 0_init_database.sql
│   ├── 1_init_ddl.sql
│   ├── 2_init_inserts.sql
│   ├── 3_views.sql
│   └── Dockerfile
└── README.md
```

- **main.py**: Lanza la interfaz gráfica y gestiona el ciclo de vida del contenedor.
- **views.py**: Contiene las ventanas y formularios de la app.
- **db.py**: Módulo para conectarse a la base de datos.
- **config.py**: Configuración de la base de datos.
- **queries.py**: Definición de consultas parametrizadas.
- **docker/**: Archivos SQL de inicialización y Dockerfile.
- **docker-compose.yml**: Define el servicio de la base de datos.

---

## 🚀 Tecnologías Usadas

- **Python 3.12.2** con Tkinter para la interfaz gráfica.
- **MariaDB** como base de datos relacional.
- **Docker y docker-compose** para contener la base de datos.
- **SQL** para la definición de tablas, vistas y triggers.

---

## ▶️ Ejecutar la Aplicación

1. Asegurate de tener Docker y docker-compose instalados.
2. Desde la carpeta raíz del proyecto, ejecutá:

```bash
python main.py
```

La aplicación abrirá la interfaz gráfica con botones para:
- Agregar personas (clientes y empleados).
- Agregar productos y presentaciones.
- Gestionar movimientos de inventario.
- Consultar vistas predefinidas.

El propio `main.py` se encarga de iniciar y detener el contenedor automáticamente al abrir y cerrar la aplicación.

---

## ℹ️ Nota Importante

La primera vez que ejecutes la aplicación, Docker Compose descargará automáticamente la imagen de MariaDB (esto puede tardar un poco dependiendo de tu conexión a Internet). En ejecuciones posteriores, la imagen estará disponible localmente y la aplicación levantará el contenedor mucho más rápido.

---

## ⚙️ Notas de Configuración

- Las contraseñas y nombres de base de datos están definidos en el `Dockerfile` y `docker-compose.yml`.
- Los scripts SQL en `docker/` se ejecutan automáticamente al inicializar el contenedor.
- Se usa el puerto `3306` para MariaDB.

---

## 📊 Vistas Implementadas

El sistema incluye vistas en MariaDB para facilitar las consultas, como:
- `vista_productos_activos`
- `vista_stock_bajo`
- `vista_empleados`
- `vista_clientes`
- `vista_proveedores`
- `vista_movimientos_totales`

Podés consultarlas desde la interfaz de la aplicación.
