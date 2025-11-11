"""
Servicio de Análisis de Seguridad - Ruta Segura
Consulta la vista v_indice_seguridad_avenidas para obtener el índice de seguridad
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional


# ========================================
# CLASE: AvenidaSeguridad
# ========================================
class AvenidaSeguridad:
    """
    Clase que representa los datos de seguridad de una avenida.
    
    Esta es una clase simple de POO (Programación Orientada a Objetos)
    que encapsula los datos y proporciona métodos útiles.
    
    Conceptos aplicados:
    - Encapsulación: Los datos están agrupados en un objeto
    - Constructor (__init__): Inicializa el objeto con los datos
    - Métodos: Funciones que operan sobre los datos del objeto
    """
    
    def __init__(self, row: dict):
        """
        Constructor: Inicializa un objeto AvenidaSeguridad desde un diccionario.
        
        Args:
            row: Diccionario con los datos de una fila de la vista SQL
        """
        # Datos básicos de la avenida
        self.avenida_id = row.get("avenida_id")
        self.avenida_nombre = row.get("avenida_nombre")
        self.tipo_via = row.get("tipo_via")
        self.zona = row.get("zona")
        self.longitud_km = float(row.get("longitud_km", 0))
        
        # Estadísticas de siniestros
        self.total_siniestros = row.get("total_siniestros", 0)
        self.total_fallecidos = row.get("total_fallecidos", 0)
        self.total_heridos = row.get("total_heridos", 0)
        self.siniestros_gravedad_alta = row.get("siniestros_gravedad_alta", 0)
        self.siniestros_gravedad_media = row.get("siniestros_gravedad_media", 0)
        self.siniestros_gravedad_baja = row.get("siniestros_gravedad_baja", 0)
        
        # Estadísticas de delitos
        self.total_delitos = row.get("total_delitos", 0)
        self.delitos_peligrosidad_alta = row.get("delitos_peligrosidad_alta", 0)
        self.delitos_peligrosidad_media = row.get("delitos_peligrosidad_media", 0)
        self.delitos_peligrosidad_baja = row.get("delitos_peligrosidad_baja", 0)
        self.total_robos = row.get("total_robos", 0)
        self.total_asaltos = row.get("total_asaltos", 0)
        self.total_hurtos = row.get("total_hurtos", 0)
        
        # Puntajes e índice
        self.puntaje_siniestros = float(row.get("puntaje_siniestros", 0))
        self.puntaje_delitos = float(row.get("puntaje_delitos", 0))
        self.indice_peligrosidad = float(row.get("indice_peligrosidad", 0))
        self.clasificacion_riesgo = row.get("clasificacion_riesgo", "SEGURA")
    
    def to_dict(self) -> dict:
        """
        Convierte el objeto a un diccionario para enviarlo como JSON.
        
        Returns:
            dict: Todos los atributos del objeto en formato diccionario
        """
        return {
            "avenida_id": self.avenida_id,
            "avenida_nombre": self.avenida_nombre,
            "tipo_via": self.tipo_via,
            "zona": self.zona,
            "longitud_km": self.longitud_km,
            "total_siniestros": self.total_siniestros,
            "total_fallecidos": self.total_fallecidos,
            "total_heridos": self.total_heridos,
            "siniestros_gravedad_alta": self.siniestros_gravedad_alta,
            "siniestros_gravedad_media": self.siniestros_gravedad_media,
            "siniestros_gravedad_baja": self.siniestros_gravedad_baja,
            "total_delitos": self.total_delitos,
            "delitos_peligrosidad_alta": self.delitos_peligrosidad_alta,
            "delitos_peligrosidad_media": self.delitos_peligrosidad_media,
            "delitos_peligrosidad_baja": self.delitos_peligrosidad_baja,
            "total_robos": self.total_robos,
            "total_asaltos": self.total_asaltos,
            "total_hurtos": self.total_hurtos,
            "puntaje_siniestros": self.puntaje_siniestros,
            "puntaje_delitos": self.puntaje_delitos,
            "indice_peligrosidad": self.indice_peligrosidad,
            "clasificacion_riesgo": self.clasificacion_riesgo
        }
    
    def es_segura(self) -> bool:
        """
        Determina si la avenida se considera segura.
        
        Returns:
            bool: True si la avenida es segura o tiene riesgo moderado
        """
        return self.clasificacion_riesgo in ["SEGURA", "RIESGO MODERADO"]
    
    def es_peligrosa(self) -> bool:
        """
        Determina si la avenida se considera peligrosa.
        
        Returns:
            bool: True si la avenida es peligrosa o muy peligrosa
        """
        return self.clasificacion_riesgo in ["PELIGROSA", "MUY PELIGROSA"]


# ========================================
# FUNCIÓN: OBTENER ÍNDICE DE SEGURIDAD DE TODAS LAS AVENIDAS
# ========================================
async def obtener_indice_seguridad_avenidas(
    db: AsyncSession,
    orden: str = "peligrosidad",
    limite: Optional[int] = None
) -> List[dict]:
    """
    Obtiene el índice de seguridad de todas las avenidas.
    
    Consulta la vista v_indice_seguridad_avenidas que calcula
    el índice combinando siniestros (70%) y delitos (30%).
    
    Args:
        db: Sesión de base de datos asíncrona
        orden: Criterio de ordenamiento:
               - "peligrosidad": Ordena de más a menos peligrosas (default)
               - "nombre": Ordena alfabéticamente por nombre
               - "zona": Ordena por zona
        limite: Número máximo de resultados (opcional)
    
    Returns:
        List[dict]: Lista de avenidas con sus índices de seguridad
    
    Ejemplo de uso:
        avenidas = await obtener_indice_seguridad_avenidas(db, orden="peligrosidad", limite=10)
        # Devuelve las 10 avenidas más peligrosas
    """
    # Determinar el ORDER BY según el parámetro
    if orden == "nombre":
        order_by = "avenida_nombre ASC"
    elif orden == "zona":
        order_by = "zona ASC, indice_peligrosidad DESC"
    else:  # Por defecto: peligrosidad
        order_by = "indice_peligrosidad DESC"
    
    # Construir la query
    query_str = f"""
        SELECT * FROM v_indice_seguridad_avenidas
        ORDER BY {order_by}
    """
    
    # Agregar LIMIT si se especificó
    if limite:
        query_str += f" LIMIT :limite"
    
    # Ejecutar la consulta
    query = text(query_str)
    
    if limite:
        result = await db.execute(query, {"limite": limite})
    else:
        result = await db.execute(query)
    
    avenidas = result.fetchall()
    
    # Convertir cada fila a objeto AvenidaSeguridad y luego a dict
    return [AvenidaSeguridad(dict(a._mapping)).to_dict() for a in avenidas]


# ========================================
# FUNCIÓN: OBTENER AVENIDA ESPECÍFICA
# ========================================
async def obtener_indice_seguridad_avenida(
    db: AsyncSession,
    avenida_id: int
) -> Optional[dict]:
    """
    Obtiene el índice de seguridad de una avenida específica.
    
    Args:
        db: Sesión de base de datos
        avenida_id: ID de la avenida a consultar
    
    Returns:
        dict: Datos de seguridad de la avenida o None si no existe
    """
    query = text("""
        SELECT * FROM v_indice_seguridad_avenidas
        WHERE avenida_id = :avenida_id
    """)
    
    result = await db.execute(query, {"avenida_id": avenida_id})
    avenida = result.fetchone()
    
    if not avenida:
        return None
    
    return AvenidaSeguridad(dict(avenida._mapping)).to_dict()


# ========================================
# FUNCIÓN: OBTENER TOP AVENIDAS SEGURAS
# ========================================
async def obtener_top_avenidas_seguras(
    db: AsyncSession,
    limite: int = 5
) -> List[dict]:
    """
    Obtiene las avenidas más seguras (menor índice de peligrosidad).
    
    Args:
        db: Sesión de base de datos
        limite: Número de avenidas a devolver (default: 5)
    
    Returns:
        List[dict]: Lista de las avenidas más seguras
    """
    query = text("""
        SELECT * FROM v_indice_seguridad_avenidas
        ORDER BY indice_peligrosidad ASC
        LIMIT :limite
    """)
    
    result = await db.execute(query, {"limite": limite})
    avenidas = result.fetchall()
    
    return [AvenidaSeguridad(dict(a._mapping)).to_dict() for a in avenidas]


# ========================================
# FUNCIÓN: OBTENER TOP AVENIDAS PELIGROSAS
# ========================================
async def obtener_top_avenidas_peligrosas(
    db: AsyncSession,
    limite: int = 5
) -> List[dict]:
    """
    Obtiene las avenidas más peligrosas (mayor índice de peligrosidad).
    
    Args:
        db: Sesión de base de datos
        limite: Número de avenidas a devolver (default: 5)
    
    Returns:
        List[dict]: Lista de las avenidas más peligrosas
    """
    query = text("""
        SELECT * FROM v_indice_seguridad_avenidas
        ORDER BY indice_peligrosidad DESC
        LIMIT :limite
    """)
    
    result = await db.execute(query, {"limite": limite})
    avenidas = result.fetchall()
    
    return [AvenidaSeguridad(dict(a._mapping)).to_dict() for a in avenidas]


# ========================================
# FUNCIÓN: OBTENER ESTADÍSTICAS GENERALES
# ========================================
async def obtener_estadisticas_generales(db: AsyncSession) -> dict:
    """
    Calcula estadísticas generales del sistema.
    
    Args:
        db: Sesión de base de datos
    
    Returns:
        dict: Estadísticas agregadas del sistema
    """
    
    query = text("""
        SELECT
            COUNT(*) as total_avenidas,
            SUM(total_siniestros) as total_siniestros_sistema,
            SUM(total_delitos) as total_delitos_sistema,
            SUM(total_fallecidos) as total_fallecidos_sistema,
            SUM(total_heridos) as total_heridos_sistema,
            AVG(indice_peligrosidad) as promedio_indice,
            MAX(indice_peligrosidad) as max_indice,
            MIN(indice_peligrosidad) as min_indice,
            SUM(CASE WHEN clasificacion_riesgo COLLATE utf8mb4_general_ci = 'MUY PELIGROSA' COLLATE utf8mb4_general_ci THEN 1 ELSE 0 END) as avenidas_muy_peligrosas,
            SUM(CASE WHEN clasificacion_riesgo COLLATE utf8mb4_general_ci = 'PELIGROSA' COLLATE utf8mb4_general_ci THEN 1 ELSE 0 END) as avenidas_peligrosas,
            SUM(CASE WHEN clasificacion_riesgo COLLATE utf8mb4_general_ci = 'RIESGO MODERADO' COLLATE utf8mb4_general_ci THEN 1 ELSE 0 END) as avenidas_riesgo_moderado,
            SUM(CASE WHEN clasificacion_riesgo COLLATE utf8mb4_general_ci = 'SEGURA' COLLATE utf8mb4_general_ci THEN 1 ELSE 0 END) as avenidas_seguras
        FROM v_indice_seguridad_avenidas
    """)

    result = await db.execute(query)
    stats = result.fetchone()
    
    return {
        "total_avenidas": stats.total_avenidas,
        "total_siniestros": stats.total_siniestros_sistema,
        "total_delitos": stats.total_delitos_sistema,
        "total_fallecidos": stats.total_fallecidos_sistema,
        "total_heridos": stats.total_heridos_sistema,
        "promedio_indice": round(float(stats.promedio_indice or 0), 2),
        "max_indice": round(float(stats.max_indice or 0), 2),
        "min_indice": round(float(stats.min_indice or 0), 2),
        "distribucion_riesgo": {
            "muy_peligrosas": stats.avenidas_muy_peligrosas,
            "peligrosas": stats.avenidas_peligrosas,
            "riesgo_moderado": stats.avenidas_riesgo_moderado,
            "seguras": stats.avenidas_seguras
        }
    }


# ========================================
# FUNCIÓN: COMPARAR DOS AVENIDAS
# ========================================
async def comparar_avenidas(
    db: AsyncSession,
    avenida_id_1: int,
    avenida_id_2: int
) -> dict:
    """
    Compara el índice de seguridad entre dos avenidas.
    
    Args:
        db: Sesión de base de datos
        avenida_id_1: ID de la primera avenida
        avenida_id_2: ID de la segunda avenida
    
    Returns:
        dict: Comparación detallada entre ambas avenidas
    """
    # Obtener ambas avenidas
    avenida_1 = await obtener_indice_seguridad_avenida(db, avenida_id_1)
    avenida_2 = await obtener_indice_seguridad_avenida(db, avenida_id_2)
    
    if not avenida_1 or not avenida_2:
        return None
    
    # Calcular diferencias
    diff_siniestros = avenida_1["total_siniestros"] - avenida_2["total_siniestros"]
    diff_delitos = avenida_1["total_delitos"] - avenida_2["total_delitos"]
    diff_indice = avenida_1["indice_peligrosidad"] - avenida_2["indice_peligrosidad"]
    
    # Determinar cuál es más segura
    mas_segura = avenida_1 if avenida_1["indice_peligrosidad"] < avenida_2["indice_peligrosidad"] else avenida_2
    
    return {
        "avenida_1": avenida_1,
        "avenida_2": avenida_2,
        "diferencias": {
            "siniestros": diff_siniestros,
            "delitos": diff_delitos,
            "indice_peligrosidad": round(diff_indice, 2)
        },
        "mas_segura": {
            "nombre": mas_segura["avenida_nombre"],
            "id": mas_segura["avenida_id"]
        }
    }


# ========================================
# NOTAS TÉCNICAS
# ========================================
"""
CONCEPTOS DE POO APLICADOS:

1. Clase (Class):
   - Plantilla para crear objetos
   - Define atributos (datos) y métodos (funciones)
   - Ejemplo: AvenidaSeguridad es una clase

2. Objeto (Object):
   - Instancia de una clase
   - Ejemplo: avenida = AvenidaSeguridad(datos)

3. Constructor (__init__):
   - Método especial que inicializa el objeto
   - Se ejecuta automáticamente al crear el objeto
   - Recibe los datos y los guarda en self

4. Self:
   - Referencia al objeto actual
   - Permite acceder a los atributos del objeto
   - Ejemplo: self.avenida_nombre

5. Métodos:
   - Funciones que pertenecen a la clase
   - Operan sobre los datos del objeto
   - Ejemplo: to_dict(), es_segura()

6. Encapsulación:
   - Agrupar datos relacionados en un objeto
   - Facilita el manejo de información compleja
   - Hace el código más organizado y mantenible

BENEFICIOS DE USAR POO:
- Código más organizado y legible
- Fácil de mantener y extender
- Reutilizable en diferentes partes del proyecto
- Separa la lógica de datos de la lógica de negocio
"""