"""
Router de reportes y estadísticas
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from decimal import Decimal
import logging
from sqlalchemy.exc import ProgrammingError

from config.database import get_db
from services import reportes as reportes_service

router = APIRouter(prefix="/reportes", tags=["Reportes"])

def _serialize_row(row) -> Dict:
    if not row:
        return {}
    d = dict(row)
    for k, v in list(d.items()):
        if isinstance(v, Decimal):
            try:
                if v == v.to_integral_value():
                    d[k] = int(v)
                else:
                    d[k] = float(v)
            except Exception:
                d[k] = float(v)
    return d

def _serialize_rows(rows) -> List[Dict]:
    return [_serialize_row(r) for r in rows]

async def _table_exists(db: AsyncSession, table_name: str) -> bool:
    sql = text("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = :t
    """)
    r = await db.execute(sql, {"t": table_name})
    cnt = r.scalar()
    try:
        return int(cnt) > 0
    except Exception:
        return bool(cnt)

async def _column_exists(db: AsyncSession, table_name: str, column_name: str) -> bool:
    sql = text("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = :t AND column_name = :c
    """)
    r = await db.execute(sql, {"t": table_name, "c": column_name})
    cnt = r.scalar()
    try:
        return int(cnt) > 0
    except Exception:
        return bool(cnt)

@router.get("/resumen-general")
async def resumen_general(db: AsyncSession = Depends(get_db)):
    try:
        sql = text("""
          SELECT COUNT(*) AS total_siniestros,
                 COALESCE(SUM(victimas_fatales),0) AS total_fallecidos,
                 COALESCE(SUM(heridos),0) AS total_heridos
          FROM siniestros;
        """)
        result = await db.execute(sql)
        row = result.mappings().first()
        return JSONResponse(content=_serialize_row(row))
    except Exception as e:
        logging.exception("Error en resumen_general")
        return JSONResponse(content={"detail": "Error interno"}, status_code=500)

@router.get("/siniestros-por-zona")
async def siniestros_por_zona(db: AsyncSession = Depends(get_db)):
    """
    Consulta adaptativa para devolver siniestros por 'zona'.
    - Si existe tabla 'zonas' y columna 'zona_id' en siniestros: hace JOIN y usa zonas.nombre.
    - Si no, intenta agrupar por 'avenida' (avenidas/avenida_id).
    - Si ninguna columna relacionada existe, agrupa por fecha (día) como fallback simple.
    """
    try:
        # preferir zonas
        zonas_table = await _table_exists(db, "zonas")
        has_zona_col = await _column_exists(db, "siniestros", "zona_id")
        if zonas_table and has_zona_col:
            sql = text("""
              SELECT z.nombre AS zona, COUNT(*) AS total
              FROM siniestros s
              JOIN zonas z ON s.zona_id = z.id
              GROUP BY z.nombre
              ORDER BY total DESC;
            """)
            result = await db.execute(sql)
            rows = result.mappings().all()
            return JSONResponse(content=_serialize_rows(rows))

        # intentar avenidas (muchos modelos usan avenida_id)
        avenidas_table = await _table_exists(db, "avenidas")
        has_avenida_col = await _column_exists(db, "siniestros", "avenida_id")
        if avenidas_table and has_avenida_col:
            sql = text("""
              SELECT a.nombre AS zona, COUNT(*) AS total
              FROM siniestros s
              JOIN avenidas a ON s.avenida_id = a.id
              GROUP BY a.nombre
              ORDER BY total DESC;
            """)
            result = await db.execute(sql)
            rows = result.mappings().all()
            return JSONResponse(content=_serialize_rows(rows))

        # si no hay tablas relacionadas, agrupar por la columna disponible (tipo_id / usuario_id) o por día
        if await _column_exists(db, "siniestros", "tipo_id"):
            sql = text("""
              SELECT s.tipo_id AS zona, COUNT(*) AS total
              FROM siniestros s
              GROUP BY s.tipo_id
              ORDER BY total DESC;
            """)
            result = await db.execute(sql)
            rows = result.mappings().all()
            return JSONResponse(content=_serialize_rows(rows))

        # fallback final: contar por fecha (por día) para al menos devolver algo
        sql = text("""
          SELECT DATE(fecha) AS zona, COUNT(*) AS total
          FROM siniestros
          GROUP BY DATE(fecha)
          ORDER BY total DESC
          LIMIT 50;
        """)
        result = await db.execute(sql)
        rows = result.mappings().all()
        return JSONResponse(content=_serialize_rows(rows))
    except ProgrammingError:
        logging.exception("ProgrammingError en siniestros_por_zona")
        return JSONResponse({"detail": "Error de consulta en la base de datos"}, status_code=500)
    except Exception:
        logging.exception("Error fallback siniestros_por_zona")
        return JSONResponse({"detail": "Error interno"}, status_code=500)

@router.get("/estadisticas-por-tipo")
async def estadisticas_por_tipo(db: AsyncSession = Depends(get_db)):
    """
    Intenta estadísticas por tipo con join a tipos_siniestro.
    Si la tabla no existe, fallback por tipo_id.
    """
    try:
        sql = text("""
          SELECT t.nombre AS tipo, COUNT(*) AS total, COALESCE(AVG(s.nivel_gravedad),0) AS gravedad_media
          FROM siniestros s
          JOIN tipos_siniestro t ON s.tipo_id = t.id
          GROUP BY t.nombre
          ORDER BY total DESC;
        """)
        result = await db.execute(sql)
        rows = result.mappings().all()
        return JSONResponse(content=_serialize_rows(rows))
    except ProgrammingError:
        logging.exception("Tabla 'tipos_siniestro' ausente, aplicando fallback por tipo_id")
        try:
            sql = text("""
              SELECT s.tipo_id AS tipo, COUNT(*) AS total
              FROM siniestros s
              GROUP BY s.tipo_id
              ORDER BY total DESC;
            """)
            result = await db.execute(sql)
            rows = result.mappings().all()
            return JSONResponse(content=_serialize_rows(rows))
        except Exception:
            logging.exception("Error fallback estadisticas_por_tipo")
            return JSONResponse({"detail": "Error interno"}, status_code=500)
    except Exception:
        logging.exception("Error en estadisticas_por_tipo")
        return JSONResponse({"detail": "Error interno"}, status_code=500)

@router.get("/siniestros-por-dia-semana")
async def siniestros_por_dia_semana(db: AsyncSession = Depends(get_db)):
    """
    Compatible con MariaDB/MySQL: WEEKDAY(fecha) devuelve 0=Monday..6=Sunday,
    sumamos 1 para obtener ISO 1..7.
    """
    try:
        sql = text("""
          SELECT (WEEKDAY(fecha) + 1) AS dia_semana, COUNT(*) AS total
          FROM siniestros
          GROUP BY dia_semana
          ORDER BY dia_semana;
        """)
        result = await db.execute(sql)
        rows = result.mappings().all()
        return JSONResponse(content=_serialize_rows(rows))
    except Exception:
        logging.exception("Error en siniestros_por_dia_semana")
        return JSONResponse({"detail": "Error interno"}, status_code=500)

# Nuevo endpoint solicitado por el frontend
@router.get("/estadisticas")
async def estadisticas(db: AsyncSession = Depends(get_db)):
    """
    Endpoint agregado para /reportes/estadisticas.
    Devuelve estadísticas agregadas (puedes ampliar la consulta según necesites).
    """
    try:
        sql = text("""
          SELECT COUNT(*) AS total_siniestros,
                 COALESCE(SUM(victimas_fatales),0) AS total_fallecidos,
                 COALESCE(SUM(heridos),0) AS total_heridos
          FROM siniestros;
        """)
        result = await db.execute(sql)
        row = result.mappings().first()
        return JSONResponse(content=_serialize_row(row))
    except Exception as e:
        logging.exception("Error en estadisticas")
        return JSONResponse(content={"detail": "Error interno"}, status_code=500)