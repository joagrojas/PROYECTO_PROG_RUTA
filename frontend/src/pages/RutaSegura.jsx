import { useState, useEffect } from 'react';
import api from '../services/api';

/**
 * Página: Ruta Segura - Análisis de Seguridad Integral
 * 
 * Combina datos de siniestros viales (70%) y delitos (30%) para
 * calcular un índice de peligrosidad por avenida.
 * 
 * Componentes que muestra:
 * 1. Estadísticas generales del sistema
 * 2. Top 5 avenidas más peligrosas
 * 3. Top 5 avenidas más seguras
 * 4. Tabla completa de todas las avenidas
 */

function RutaSegura() {
  // ========================================
  // ESTADO DEL COMPONENTE (useState)
  // ========================================
  
  // Estado para las estadísticas generales
  const [estadisticas, setEstadisticas] = useState(null);
  
  // Estado para el top de avenidas peligrosas
  const [topPeligrosas, setTopPeligrosas] = useState([]);
  
  // Estado para el top de avenidas seguras
  const [topSeguras, setTopSeguras] = useState([]);
  
  // Estado para todas las avenidas
  const [todasAvenidas, setTodasAvenidas] = useState([]);
  
  // Estado de carga (loading)
  const [cargando, setCargando] = useState(true);
  
  // Estado de error
  const [error, setError] = useState(null);

  // ========================================
  // CARGAR DATOS AL MONTAR EL COMPONENTE
  // ========================================
  
  useEffect(() => {
    cargarDatos();
  }, []);

  /**
   * Carga todos los datos necesarios desde el backend.
   * Hace 4 llamadas a la API en paralelo usando Promise.all
   */
  const cargarDatos = async () => {
    try {
      setCargando(true);
      setError(null);

      // Hacer todas las peticiones en paralelo para ser más rápido
      const [statsRes, peligrosasRes, segurasRes, todasRes] = await Promise.all([
        api.get('/reportes/estadisticas-seguridad'),
        api.get('/reportes/top-avenidas-peligrosas?limite=5'),
        api.get('/reportes/top-avenidas-seguras?limite=5'),
        api.get('/reportes/indice-seguridad?orden=peligrosidad')
      ]);

      // Guardar los datos en el estado
      setEstadisticas(statsRes.data);
      setTopPeligrosas(peligrosasRes.data.avenidas);
      setTopSeguras(segurasRes.data.avenidas);
      setTodasAvenidas(todasRes.data.avenidas);

    } catch (err) {
      console.error('Error al cargar datos:', err);
      setError('Error al cargar los datos. Por favor, intenta nuevamente.');
    } finally {
      setCargando(false);
    }
  };

  // ========================================
  // FUNCIONES AUXILIARES
  // ========================================
  
  /**
   * Devuelve la clase CSS de color según la clasificación de riesgo.
   */
  const obtenerColorRiesgo = (clasificacion) => {
    switch (clasificacion) {
      case 'MUY PELIGROSA':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'PELIGROSA':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'RIESGO MODERADO':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'SEGURA':
        return 'bg-green-100 text-green-800 border-green-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  /**
   * Devuelve el emoji según la clasificación de riesgo.
   */
  const obtenerEmoji = (clasificacion) => {
    switch (clasificacion) {
      case 'MUY PELIGROSA':
        return '🔴';
      case 'PELIGROSA':
        return '🟠';
      case 'RIESGO MODERADO':
        return '🟡';
      case 'SEGURA':
        return '🟢';
      default:
        return '⚪';
    }
  };

  // ========================================
  // RENDERIZADO CONDICIONAL
  // ========================================
  
  // Si está cargando, mostrar spinner
  if (cargando) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando análisis de seguridad...</p>
        </div>
      </div>
    );
  }

  // Si hay error, mostrar mensaje de error
  if (error) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-lg max-w-md">
          <p className="font-bold mb-2">Error</p>
          <p>{error}</p>
          <button
            onClick={cargarDatos}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  // ========================================
  // RENDERIZADO PRINCIPAL
  // ========================================
  
  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* ENCABEZADO */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          🛣️ Ruta Segura - Análisis Integral
        </h1>
        <p className="text-gray-600">
          Índice de seguridad combinando siniestros viales (70%) y delitos (30%)
        </p>
      </div>

      {/* ESTADÍSTICAS GENERALES */}
      {estadisticas && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {/* Total de Avenidas */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
            <p className="text-gray-500 text-sm mb-1">Total de Avenidas</p>
            <p className="text-3xl font-bold text-gray-800">{estadisticas.total_avenidas}</p>
          </div>

          {/* Total de Siniestros */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
            <p className="text-gray-500 text-sm mb-1">Total Siniestros</p>
            <p className="text-3xl font-bold text-gray-800">{estadisticas.total_siniestros}</p>
            <p className="text-xs text-gray-500 mt-1">
              {estadisticas.total_fallecidos} fallecidos, {estadisticas.total_heridos} heridos
            </p>
          </div>

          {/* Total de Delitos */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
            <p className="text-gray-500 text-sm mb-1">Total Delitos</p>
            <p className="text-3xl font-bold text-gray-800">{estadisticas.total_delitos}</p>
          </div>

          {/* Promedio de Índice */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
            <p className="text-gray-500 text-sm mb-1">Índice Promedio</p>
            <p className="text-3xl font-bold text-gray-800">{estadisticas.promedio_indice}</p>
            <p className="text-xs text-gray-500 mt-1">
              Rango: {estadisticas.min_indice} - {estadisticas.max_indice}
            </p>
          </div>
        </div>
      )}

      {/* DISTRIBUCIÓN DE RIESGO */}
      {estadisticas && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            📊 Distribución de Riesgo
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-red-50 rounded-lg border border-red-200">
              <p className="text-4xl mb-2">🔴</p>
              <p className="text-2xl font-bold text-red-800">
                {estadisticas.distribucion_riesgo.muy_peligrosas}
              </p>
              <p className="text-sm text-gray-600">Muy Peligrosas</p>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg border border-orange-200">
              <p className="text-4xl mb-2">🟠</p>
              <p className="text-2xl font-bold text-orange-800">
                {estadisticas.distribucion_riesgo.peligrosas}
              </p>
              <p className="text-sm text-gray-600">Peligrosas</p>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg border border-yellow-200">
              <p className="text-4xl mb-2">🟡</p>
              <p className="text-2xl font-bold text-yellow-800">
                {estadisticas.distribucion_riesgo.riesgo_moderado}
              </p>
              <p className="text-sm text-gray-600">Riesgo Moderado</p>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
              <p className="text-4xl mb-2">🟢</p>
              <p className="text-2xl font-bold text-green-800">
                {estadisticas.distribucion_riesgo.seguras}
              </p>
              <p className="text-sm text-gray-600">Seguras</p>
            </div>
          </div>
        </div>
      )}

      {/* TOP 5 - LAYOUT DE DOS COLUMNAS */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* TOP 5 MÁS PELIGROSAS */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span className="text-2xl mr-2">⚠️</span>
            Top 5 Avenidas Más Peligrosas
          </h2>
          <div className="space-y-3">
            {topPeligrosas.map((avenida, index) => (
              <div
                key={avenida.avenida_id}
                className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200 hover:bg-red-100 transition"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl font-bold text-red-800 w-8">
                    {index + 1}
                  </span>
                  <div>
                    <p className="font-semibold text-gray-800">
                      {avenida.avenida_nombre}
                    </p>
                    <p className="text-sm text-gray-600">
                      {avenida.total_siniestros} siniestros, {avenida.total_delitos} delitos
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-red-800">
                    {avenida.indice_peligrosidad.toFixed(1)}
                  </p>
                  <span className="text-xs px-2 py-1 bg-red-200 text-red-800 rounded">
                    {avenida.clasificacion_riesgo}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* TOP 5 MÁS SEGURAS */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span className="text-2xl mr-2">✅</span>
            Top 5 Avenidas Más Seguras
          </h2>
          <div className="space-y-3">
            {topSeguras.map((avenida, index) => (
              <div
                key={avenida.avenida_id}
                className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200 hover:bg-green-100 transition"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl font-bold text-green-800 w-8">
                    {index + 1}
                  </span>
                  <div>
                    <p className="font-semibold text-gray-800">
                      {avenida.avenida_nombre}
                    </p>
                    <p className="text-sm text-gray-600">
                      {avenida.total_siniestros} siniestros, {avenida.total_delitos} delitos
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-800">
                    {avenida.indice_peligrosidad.toFixed(1)}
                  </p>
                  <span className="text-xs px-2 py-1 bg-green-200 text-green-800 rounded">
                    {avenida.clasificacion_riesgo}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* TABLA COMPLETA DE TODAS LAS AVENIDAS */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">
          📋 Todas las Avenidas - Detalle Completo
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full table-auto">
            <thead>
              <tr className="bg-gray-100 border-b-2 border-gray-200">
                <th className="text-left p-3 font-semibold text-gray-700">#</th>
                <th className="text-left p-3 font-semibold text-gray-700">Avenida</th>
                <th className="text-left p-3 font-semibold text-gray-700">Zona</th>
                <th className="text-center p-3 font-semibold text-gray-700">Siniestros</th>
                <th className="text-center p-3 font-semibold text-gray-700">Delitos</th>
                <th className="text-center p-3 font-semibold text-gray-700">Índice</th>
                <th className="text-center p-3 font-semibold text-gray-700">Clasificación</th>
              </tr>
            </thead>
            <tbody>
              {todasAvenidas.map((avenida, index) => (
                <tr
                  key={avenida.avenida_id}
                  className="border-b border-gray-200 hover:bg-gray-50 transition"
                >
                  <td className="p-3 text-gray-600">{index + 1}</td>
                  <td className="p-3">
                    <div>
                      <p className="font-semibold text-gray-800">
                        {avenida.avenida_nombre}
                      </p>
                      <p className="text-xs text-gray-500">
                        {avenida.tipo_via} • {avenida.longitud_km} km
                      </p>
                    </div>
                  </td>
                  <td className="p-3 text-gray-600">{avenida.zona}</td>
                  <td className="p-3 text-center">
                    <p className="font-semibold text-gray-800">
                      {avenida.total_siniestros}
                    </p>
                    <p className="text-xs text-gray-500">
                      {avenida.total_fallecidos}💀 {avenida.total_heridos}🤕
                    </p>
                  </td>
                  <td className="p-3 text-center">
                    <p className="font-semibold text-gray-800">
                      {avenida.total_delitos}
                    </p>
                    <p className="text-xs text-gray-500">
                      {avenida.total_robos}R {avenida.total_asaltos}A
                    </p>
                  </td>
                  <td className="p-3 text-center">
                    <p className="text-xl font-bold text-gray-800">
                      {avenida.indice_peligrosidad.toFixed(1)}
                    </p>
                  </td>
                  <td className="p-3 text-center">
                    <span
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${obtenerColorRiesgo(
                        avenida.clasificacion_riesgo
                      )}`}
                    >
                      <span className="mr-1">
                        {obtenerEmoji(avenida.clasificacion_riesgo)}
                      </span>
                      {avenida.clasificacion_riesgo}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* NOTA EXPLICATIVA */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-bold text-blue-900 mb-2">
          ℹ️ Cómo se calcula el Índice de Seguridad
        </h3>
        <p className="text-blue-800 mb-4">
          El índice combina dos factores principales con ponderación diferencial:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="bg-white rounded p-4 border border-blue-300">
            <p className="font-bold text-blue-900 mb-2">🚗 Siniestros Viales (70%)</p>
            <ul className="list-disc list-inside text-blue-800 space-y-1">
              <li>Cantidad de accidentes</li>
              <li>Víctimas fatales (peso muy alto)</li>
              <li>Heridos</li>
              <li>Nivel de gravedad</li>
            </ul>
          </div>
          <div className="bg-white rounded p-4 border border-blue-300">
            <p className="font-bold text-blue-900 mb-2">🚨 Delitos (30%)</p>
            <ul className="list-disc list-inside text-blue-800 space-y-1">
              <li>Cantidad de delitos</li>
              <li>Tipo (robo, asalto, hurto)</li>
              <li>Nivel de peligrosidad</li>
            </ul>
          </div>
        </div>
        <p className="text-blue-800 mt-4 text-xs">
          <strong>Nota:</strong> El índice de peligrosidad es MAYOR cuanto más peligrosa es la avenida.
          Un índice bajo indica mayor seguridad.
        </p>
      </div>
    </div>
  );
}

export default RutaSegura;