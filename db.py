import mysql.connector
from tkinter import messagebox
from config import config

def conectar_db():
    """
    Establece la conexión con la base de datos usando la configuración de 'config.py'.
    Devuelve una conexión activa o None si hay error.
    """
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
        return None

def ejecutar_select(query, params=None):
    """
    Ejecuta una consulta SELECT con o sin parámetros.
    Devuelve una tupla: (columnas, resultados).
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            return columnas, resultados
        except mysql.connector.Error as err:
            messagebox.showerror("Error en la consulta", str(err))
            return [], []
        finally:
            cursor.close()
            conn.close()

def ejecutar_modificacion(query, params=None):
    """
    Ejecuta una consulta de modificación de datos (INSERT, UPDATE, DELETE).
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error al ejecutar", str(err))
        finally:
            cursor.close()
            conn.close()
