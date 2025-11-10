"""
Servicio para reportes y consultas estadísticas
Incluye INNER JOIN, GROUP BY y Subconsultas para cumplir requisitos del TP
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

# ========================================
# CONSULTA 1: INNER JOIN
# ========================================
async def obtener_siniestros_por_zona(db: AsyncSession) -> List[Dict]:
    """
    Consulta con INNER JOIN y GROUP BY
    Muestra estadísticas de siniestros por zona geográfica
    """
    query = text("""
        SELECT 
            a.zona,
            a.tipo AS tipo_via,
            COUNT(s.id) AS total_siniestros,
            SUM(s.victimas_fatales) AS total_fallecidos,
            SUM(s.heridos) AS total_heridos,
            ROUND(AVG(s.victimas_fatales + s.heridos), 2) AS promedio_victimas
        FROM siniestros s
        INNER JOIN avenidas a ON s.avenida_id = a.id
        GROUP BY a.zona, a.tipo
        ORDER BY total_siniestros DESC
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "zona": r.zona,
            "tipo_via": r.tipo_via,
            "total_siniestros": r.total_siniestros,
            "total_fallecidos": r.total_fallecidos,
            "total_heridos": r.total_heridos,
            "promedio_victimas": float(r.promedio_victimas) if r.promedio_victimas else 0
        }
        for r in rows
    ]

# ========================================
# CONSULTA 2: SUBCONSULTA
# ========================================
async def obtener_avenidas_peligrosas(db: AsyncSession) -> List[Dict]:
    """
    Consulta con SUBCONSULTA
    Ranking de avenidas más peligrosas usando subconsulta en FROM
    """
    query = text("""
        SELECT 
            a.nombre,
            a.zona,
            a.tipo,
            s.total_siniestros,
            s.total_fallecidos,
            s.total_heridos,
            CASE 
                WHEN s.total_fallecidos > 0 THEN 'Muy Peligrosa'
                WHEN s.total_heridos > 5 THEN 'Peligrosa'
                ELSE 'Moderada'
            END AS clasificacion_riesgo
        FROM avenidas a
        INNER JOIN (
            SELECT 
                avenida_id,
                COUNT(*) AS total_siniestros,
                SUM(victimas_fatales) AS total_fallecidos,
                SUM(heridos) AS total_heridos
            FROM siniestros
            GROUP BY avenida_id
        ) s ON a.id = s.avenida_id
        ORDER BY s.total_fallecidos DESC, s.total_siniestros DESC
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "nombre": r.nombre,
            "zona": r.zona,
            "tipo": r.tipo,
            "total_siniestros": r.total_siniestros,
            "total_fallecidos": r.total_fallecidos,
            "total_heridos": r.total_heridos,
            "clasificacion_riesgo": r.clasificacion_riesgo
        }
        for r in rows
    ]

# ========================================
# CONSULTA 3: GROUP BY con múltiples agregaciones
# ========================================
async def obtener_estadisticas_por_tipo(db: AsyncSession) -> List[Dict]:
    """
    Consulta con INNER JOIN y GROUP BY
    Estadísticas detalladas por tipo de siniestro
    """
    query = text("""
        SELECT 
            ts.nombre AS tipo_siniestro,
            ts.gravedad,
            COUNT(s.id) AS cantidad,
            SUM(s.victimas_fatales) AS fallecidos,
            SUM(s.heridos) AS heridos,
            ROUND(AVG(s.num_vehiculos), 2) AS promedio_vehiculos,
            COUNT(CASE WHEN s.es_fin_de_semana = TRUE THEN 1 END) AS siniestros_fin_semana,
            ROUND(COUNT(CASE WHEN s.es_fin_de_semana = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) AS porcentaje_fin_semana
        FROM siniestros s
        INNER JOIN tipos_siniestro ts ON s.tipo_id = ts.id
        GROUP BY ts.id, ts.nombre, ts.gravedad
        ORDER BY fallecidos DESC, cantidad DESC
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "tipo_siniestro": r.tipo_siniestro,
            "gravedad": r.gravedad,
            "cantidad": r.cantidad,
            "fallecidos": r.fallecidos,
            "heridos": r.heridos,
            "promedio_vehiculos": float(r.promedio_vehiculos) if r.promedio_vehiculos else 0,
            "siniestros_fin_semana": r.siniestros_fin_semana,
            "porcentaje_fin_semana": float(r.porcentaje_fin_semana) if r.porcentaje_fin_semana else 0
        }
        for r in rows
    ]

# ========================================
# CONSULTA 4: SUBCONSULTA CORRELACIONADA
# ========================================
async def obtener_analisis_vehiculos(db: AsyncSession) -> List[Dict]:
    """
    Consulta con SUBCONSULTA CORRELACIONADA
    Análisis de vehículos con subconsulta para siniestros graves
    """
    query = text("""
        SELECT 
            v.tipo_vehiculo,
            COUNT(DISTINCT v.siniestro_id) AS siniestros_involucrados,
            COUNT(*) AS total_vehiculos,
            SUM(CASE WHEN v.es_fallecido = TRUE THEN 1 ELSE 0 END) AS fallecidos,
            ROUND(SUM(CASE WHEN v.es_fallecido = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS tasa_mortalidad,
            (
                SELECT COUNT(*)
                FROM vehiculos_involucrados v2
                INNER JOIN siniestros s2 ON v2.siniestro_id = s2.id
                WHERE v2.tipo_vehiculo = v.tipo_vehiculo
                AND s2.nivel_gravedad = 'alta'
            ) AS siniestros_gravedad_alta
        FROM vehiculos_involucrados v
        GROUP BY v.tipo_vehiculo
        ORDER BY fallecidos DESC, total_vehiculos DESC
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "tipo_vehiculo": r.tipo_vehiculo,
            "siniestros_involucrados": r.siniestros_involucrados,
            "total_vehiculos": r.total_vehiculos,
            "fallecidos": r.fallecidos,
            "tasa_mortalidad": float(r.tasa_mortalidad) if r.tasa_mortalidad else 0,
            "siniestros_gravedad_alta": r.siniestros_gravedad_alta
        }
        for r in rows
    ]

# ========================================
# Reportes adicionales
# ========================================

async def obtener_resumen_general(db: AsyncSession) -> Dict:
    """Resumen general del sistema"""
    query = text("""
        SELECT 
            COUNT(*) AS total_siniestros,
            SUM(victimas_fatales) AS total_fallecidos,
            SUM(heridos) AS total_heridos,
            COUNT(CASE WHEN nivel_gravedad = 'alta' THEN 1 END) AS siniestros_graves,
            COUNT(CASE WHEN es_fin_de_semana = TRUE THEN 1 END) AS siniestros_fin_semana
        FROM siniestros
    """)
    
    result = await db.execute(query)
    row = result.fetchone()
    
    if not row:
        return {}
    
    return {
        "total_siniestros": row.total_siniestros,
        "total_fallecidos": row.total_fallecidos,
        "total_heridos": row.total_heridos,
        "siniestros_graves": row.siniestros_graves,
        "siniestros_fin_semana": row.siniestros_fin_semana
    }

async def obtener_siniestros_por_mes(db: AsyncSession) -> List[Dict]:
    """Distribución de siniestros por mes"""
    query = text("""
        SELECT 
            YEAR(fecha) AS anio,
            MONTH(fecha) AS mes,
            MONTHNAME(fecha) AS nombre_mes,
            COUNT(*) AS cantidad,
            SUM(victimas_fatales) AS fallecidos,
            SUM(heridos) AS heridos
        FROM siniestros
        GROUP BY YEAR(fecha), MONTH(fecha), MONTHNAME(fecha)
        ORDER BY anio, mes
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "anio": r.anio,
            "mes": r.mes,
            "nombre_mes": r.nombre_mes,
            "cantidad": r.cantidad,
            "fallecidos": r.fallecidos,
            "heridos": r.heridos
        }
        for r in rows
    ]

async def obtener_siniestros_por_dia_semana(db: AsyncSession) -> List[Dict]:
    """Distribución de siniestros por día de la semana"""
    query = text("""
        SELECT 
            dia_semana,
            COUNT(*) AS cantidad,
            SUM(victimas_fatales) AS fallecidos,
            SUM(heridos) AS heridos,
            ROUND(AVG(victimas_fatales + heridos), 2) AS promedio_victimas
        FROM siniestros
        GROUP BY dia_semana
        ORDER BY cantidad DESC
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "dia_semana": r.dia_semana,
            "cantidad": r.cantidad,
            "fallecidos": r.fallecidos,
            "heridos": r.heridos,
            "promedio_victimas": float(r.promedio_victimas) if r.promedio_victimas else 0
        }
        for r in rows
    ]

async def obtener_horarios_criticos(db: AsyncSession) -> List[Dict]:
    """Horarios con mayor cantidad de siniestros"""
    query = text("""
        SELECT 
            HOUR(hora) AS hora,
            COUNT(*) AS cantidad,
            SUM(victimas_fatales) AS fallecidos,
            SUM(heridos) AS heridos,
            CASE 
                WHEN HOUR(hora) BETWEEN 6 AND 9 THEN 'Hora Pico Mañana'
                WHEN HOUR(hora) BETWEEN 17 AND 20 THEN 'Hora Pico Tarde'
                WHEN HOUR(hora) BETWEEN 22 AND 23 OR HOUR(hora) BETWEEN 0 AND 5 THEN 'Madrugada'
                ELSE 'Horario Normal'
            END AS clasificacion
        FROM siniestros
        GROUP BY HOUR(hora)
        ORDER BY cantidad DESC
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "hora": r.hora,
            "cantidad": r.cantidad,
            "fallecidos": r.fallecidos,
            "heridos": r.heridos,
            "clasificacion": r.clasificacion
        }
        for r in rows
    ]

async def obtener_top_marcas_involucradas(db: AsyncSession, limit: int = 10) -> List[Dict]:
    """Top marcas de vehículos más involucradas en siniestros"""
    query = text("""
        SELECT 
            marca,
            COUNT(*) AS cantidad,
            SUM(CASE WHEN es_fallecido = TRUE THEN 1 ELSE 0 END) AS con_fallecidos
        FROM vehiculos_involucrados
        WHERE marca IS NOT NULL AND marca != 'Indefinido'
        GROUP BY marca
        ORDER BY cantidad DESC
        LIMIT :limit
    """)
    
    result = await db.execute(query, {"limit": limit})
    rows = result.fetchall()
    
    return [
        {
            "marca": r.marca,
            "cantidad": r.cantidad,
            "con_fallecidos": r.con_fallecidos
        }
        for r in rows
    ]