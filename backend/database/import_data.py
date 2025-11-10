"""
Script para importar datos de CSVs a la base de datos MySQL
Sistema de Gestión de Siniestros Viales - CSVs con separador ;
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import bcrypt
import os

# Configuración de conexión a MySQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': '',
    'database': 'siniestros_viales'
}

def conectar_db():
    """Establece conexión con MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✓ Conexión exitosa a MySQL")
            return conn
    except Error as e:
        print(f"✗ Error al conectar: {e}")
        return None

def leer_csv_seguro(nombre_archivo):
    """Lee CSV con diferentes encodings y separadores"""
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    separadores = [';', ',', '\t']
    
    for encoding in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(nombre_archivo, encoding=encoding, sep=sep)
                if len(df.columns) > 1:
                    print(f"   ✓ Leído con encoding: {encoding}, separador: '{sep}'")
                    print(f"   Columnas: {list(df.columns)[:5]}...")
                    return df
            except:
                continue
    
    print(f"   ✗ No se pudo leer: {nombre_archivo}")
    return None

def importar_usuarios(conn):
    """Importa usuarios (crea por defecto)"""
    usuarios_default = [
        ('admin@rutasegura.com', 'admin123', 'Administrador Sistema', 'admin', '2024-01-15'),
        ('editor@rutasegura.com', 'editor123', 'Carlos Rodriguez', 'editor', '2024-01-15'),
        ('consultor@rutasegura.com', 'consultor123', 'Ana Martinez', 'consultor', '2024-01-15')
    ]
    
    cursor = conn.cursor()
    count = 0
    
    for email, password, nombre, rol, fecha_registro in usuarios_default:
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query = """
            INSERT INTO usuarios (email, password_hash, nombre, rol, fecha_registro, activo)
            VALUES (%s, %s, %s, %s, %s, 1)
            ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
        """
        
        cursor.execute(query, (email, password_hash, nombre, rol, fecha_registro))
        count += 1
    
    conn.commit()
    cursor.close()
    print(f"   ✓ Creados {count} usuarios")
    return count

def importar_avenidas(conn):
    """Importa avenidas desde CSV"""
    archivo = 'AVENIDAS.csv'
    
    if not os.path.exists(archivo):
        print(f"   ✗ {archivo} no encontrado")
        return 0
    
    try:
        df = leer_csv_seguro(archivo)
        if df is None:
            return 0
        
        cursor = conn.cursor()
        count = 0
        
        df.columns = df.columns.str.strip()
        
        for _, row in df.iterrows():
            query = """
                INSERT INTO avenidas (nombre, tipo, zona, longitud_km)
                VALUES (%s, %s, %s, %s)
            """
            
            values = (
                str(row['nombre']).strip(),
                str(row['tipo']).strip(),
                str(row['zona']).strip(),
                float(row['longitud_km'])
            )
            
            cursor.execute(query, values)
            count += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✓ Importados {count} registros")
        return count
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        conn.rollback()
        return 0

def importar_tipos_siniestro(conn):
    """Importa tipos de siniestro desde CSV"""
    archivo = 'TIPOS_SINIESTRO.csv'
    
    if not os.path.exists(archivo):
        print(f"   ✗ {archivo} no encontrado")
        return 0
    
    try:
        df = leer_csv_seguro(archivo)
        if df is None:
            return 0
        
        cursor = conn.cursor()
        count = 0
        
        df.columns = df.columns.str.strip()
        
        for _, row in df.iterrows():
            query = """
                INSERT INTO tipos_siniestro (nombre, gravedad, descripcion)
                VALUES (%s, %s, %s)
            """
            
            descripcion = None
            if 'descripcion' in df.columns and pd.notna(row.get('descripcion')):
                descripcion = str(row['descripcion']).strip()
            
            values = (
                str(row['nombre']).strip(),
                str(row['gravedad']).strip(),
                descripcion
            )
            
            cursor.execute(query, values)
            count += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✓ Importados {count} registros")
        return count
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        conn.rollback()
        return 0

def importar_siniestros(conn):
    """Importa siniestros desde CSV"""
    archivo = 'SINIESTROS.csv'
    
    if not os.path.exists(archivo):
        print(f"   ✗ {archivo} no encontrado")
        return 0
    
    try:
        df = leer_csv_seguro(archivo)
        if df is None:
            return 0
        
        cursor = conn.cursor()
        count = 0
        
        df.columns = df.columns.str.strip()
        
        for _, row in df.iterrows():
            query = """
                INSERT INTO siniestros (
                    fecha, hora, avenida_id, tipo_id, nivel_gravedad,
                    victimas_fatales, heridos, num_vehiculos, dia_semana,
                    es_fin_de_semana, usuario_id, observaciones
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            observaciones = None
            if 'observaciones' in df.columns and pd.notna(row.get('observaciones')):
                observaciones = str(row['observaciones']).strip()
            
            values = (
                row['fecha'],
                row['hora'],
                int(row['avenida_id']),
                int(row['tipo_id']),
                str(row['nivel_gravedad']).strip(),
                int(row['victimas_fatales']),
                int(row['heridos']),
                int(row['num_vehiculos']),
                str(row['dia_semana']).strip(),
                bool(int(row['es_fin_de_semana'])),
                int(row['usuario_id']),
                observaciones
            )
            
            cursor.execute(query, values)
            count += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✓ Importados {count} registros")
        return count
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        conn.rollback()
        return 0

def importar_vehiculos(conn):
    """Importa vehículos involucrados desde CSV"""
    archivo = 'VEHICULOS_INVOLUCRADOS.csv'
    
    if not os.path.exists(archivo):
        print(f"   ✗ {archivo} no encontrado")
        return 0
    
    try:
        df = leer_csv_seguro(archivo)
        if df is None:
            return 0
        
        cursor = conn.cursor()
        count = 0
        
        df.columns = df.columns.str.strip()
        
        for _, row in df.iterrows():
            query = """
                INSERT INTO vehiculos_involucrados (
                    siniestro_id, tipo_vehiculo, marca, modelo, rol, es_fallecido
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            marca = row.get('marca', 'Indefinido')
            if pd.isna(marca) or str(marca).strip() == '':
                marca = 'Indefinido'
            
            modelo = row.get('modelo', 'Indefinido')
            if pd.isna(modelo) or str(modelo).strip() == '':
                modelo = 'Indefinido'
            
            es_fallecido = row.get('es_fallecido', False)
            if pd.isna(es_fallecido):
                es_fallecido = False
            if isinstance(es_fallecido, str):
                es_fallecido = es_fallecido.lower() in ['true', '1', 'si', 'sí', 'yes']
            
            values = (
                int(row['siniestro_id']),
                str(row['tipo_vehiculo']).strip(),
                str(marca).strip(),
                str(modelo).strip(),
                str(row['rol']).strip(),
                bool(es_fallecido)
            )
            
            cursor.execute(query, values)
            count += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✓ Importados {count} registros")
        return count
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        conn.rollback()
        return 0

def importar_delitos(conn):
    """Importa reportes delictivos desde CSV"""
    archivo = 'DELITOS.csv'
    
    if not os.path.exists(archivo):
        print(f"   ✗ {archivo} no encontrado")
        return 0
    
    try:
        df = leer_csv_seguro(archivo)
        if df is None:
            return 0
        
        cursor = conn.cursor()
        count = 0
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()
        
        for _, row in df.iterrows():
            query = """
                INSERT INTO reportes_delictivos (
                    fecha, hora, avenida_id, tipo_delito, nivel_peligrosidad,
                    descripcion, usuario_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Manejar descripción opcional
            descripcion = None
            if 'descripcion' in df.columns and pd.notna(row.get('descripcion')):
                descripcion = str(row['descripcion']).strip()
            
            values = (
                row['fecha'],
                row['hora'],
                int(row['avenida_id']),
                str(row['tipo_delito']).strip(),
                str(row['nivel_peligrosidad']).strip(),
                descripcion,
                int(row['usuario_id'])
            )
            
            cursor.execute(query, values)
            count += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✓ Importados {count} registros")
        return count
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        conn.rollback()
        return 0

def main():
    """Función principal"""
    print("=" * 50)
    print("  IMPORTACIÓN DE DATOS - RUTA SEGURA")
    print("=" * 50)
    
    conn = conectar_db()
    
    if not conn:
        return
    
    try:
        resultados = {}
        
        print("\n1. Importando usuarios...")
        resultados['usuarios'] = importar_usuarios(conn)
        
        print("\n2. Importando avenidas...")
        resultados['avenidas'] = importar_avenidas(conn)
        
        print("\n3. Importando tipos de siniestro...")
        resultados['tipos_siniestro'] = importar_tipos_siniestro(conn)
        
        print("\n4. Importando siniestros...")
        resultados['siniestros'] = importar_siniestros(conn)
        
        print("\n5. Importando vehículos involucrados...")
        resultados['vehiculos_involucrados'] = importar_vehiculos(conn)
        
        print("\n6. Importando reportes delictivos...")
        resultados['reportes_delictivos'] = importar_delitos(conn)
        
        # Resumen
        print("\n📊 RESUMEN DE IMPORTACIÓN:")
        print("-" * 50)
        total = 0
        for tabla, count in resultados.items():
            print(f"  {tabla:30} {count:3} registros")
            total += count
        print("-" * 50)
        print(f"  {'TOTAL':30} {total:3} registros")
        
        print("\n" + "=" * 50)
        print("  ✓ IMPORTACIÓN COMPLETADA")
        print("=" * 50)
        
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("-" * 50)
        print("  Admin:")
        print("    Email: admin@rutasegura.com")
        print("    Password: admin123")
        print("\n  Editor:")
        print("    Email: editor@rutasegura.com")
        print("    Password: editor123")
        print("\n  Consultor:")
        print("    Email: consultor@rutasegura.com")
        print("    Password: consultor123")
        print("-" * 50)
        
    except Exception as e:
        print(f"\n✗ Error general: {e}")
        
    finally:
        if conn.is_connected():
            conn.close()
            print("\n✓ Conexión cerrada")

if __name__ == "__main__":
    main()