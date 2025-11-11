/**
 * ==========================================
 * PÁGINA RUTA SEGURA
 * ==========================================
 * 
 * Esta es la página PRINCIPAL del sistema.
 * Muestra el índice de seguridad de las avenidas combinando:
 * - Datos de siniestros viales (70% del peso)
 * - Datos de reportes delictivos (30% del peso)
 * 
 * FUNCIONALIDADES:
 * 1. Ver índice de seguridad de todas las avenidas
 * 2. Ordenar por peligrosidad, nombre o zona
 * 3. Ver top 5 más seguras y más peligrosas
 * 4. Comparar dos avenidas específicas
 * 5. Visualización con colores según nivel de riesgo
 * 
 * CONCEPTOS APLICADOS:
 * - Estado con hooks (useState, useEffect)
 * - Llamadas asíncronas a API
 * - Renderizado condicional
 * - Componentes reutilizables
 * - Manejo de errores
 * ==========================================
 */

import { useState, useEffect } from 'react';
import { 
  Shield, 
  AlertTriangle, 
  TrendingUp, 
  RefreshCw,
  GitCompare
} from 'lucide-react';

// Importar servicios de la API
// Asegúrate de que tu api.js tenga reportesService exportado
import { reportesService } from '../services/api';

export default function RutaSegura() {
  // ==========================================
  // ESTADOS DEL COMPONENTE
  // ==========================================
  
  // Estado principal: lista de avenidas con su índice
  const [avenidas, setAvenidas] = useState([]);
  
  // Estado de carga y errores
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Estado para filtros y ordenamiento
  const [ordenamiento, setOrdenamiento] = useState('peligrosidad'); // peligrosidad, nombre, zona
  const [limite, setLimite] = useState(null); // null = todas
  
  // Estado para comparación de avenidas
  const [mostrarComparacion, setMostrarComparacion] = useState(false);
  const [avenida1, setAvenida1] = useState('');
  const [avenida2, setAvenida2] = useState('');
  const [resultadoComparacion, setResultadoComparacion] = useState(null);
  
  // Estado para tops
  const [topSeguras, setTopSeguras] = useState([]);
  const [topPeligrosas, setTopPeligrosas] = useState([]);

  // ==========================================
  // EFECTOS (useEffect)
  // ==========================================
  
  /**
   * Efecto principal: cargar datos al montar el componente
   * Se ejecuta cuando cambian: ordenamiento o límite
   */
  useEffect(() => {
    cargarDatos();
  }, [ordenamiento, limite]);

  /**
   * Efecto secundario: cargar tops
   * Se ejecuta solo una vez al montar
   */
  useEffect(() => {
    cargarTops();
  }, []);

  // ==========================================
  // FUNCIONES DE CARGA DE DATOS
  // ==========================================

  /**
   * Cargar índice de seguridad de todas las avenidas
   */
  const cargarDatos = async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('📊 Cargando índice de seguridad...');
      
      // Llamar al endpoint con parámetros
      const params = {
        orden: ordenamiento,
        ...(limite && { limite })
      };
      
      const response = await reportesService.getIndiceSeguridad(params);
      
      console.log('✅ Datos recibidos:', response);
      
      // El backend devuelve { total, orden, avenidas: [...] }
      setAvenidas(response.avenidas || response);
      
    } catch (err) {
      console.error('❌ Error al cargar datos:', err);
      setError('Error al cargar el índice de seguridad. Verifica que el backend esté corriendo.');
      
      // Datos de ejemplo para desarrollo (puedes comentar esto en producción)
      setAvenidas([
        {
          id: 1,
          nombre: 'Av. Perón',
          zona: 'Centro',
          total_siniestros: 45,
          total_delitos: 28,
          indice_peligrosidad: 8.5,
          nivel_riesgo: 'alto'
        },
        {
          id: 2,
          nombre: 'Calle Rivadavia',
          zona: 'Norte',
          total_siniestros: 12,
          total_delitos: 8,
          indice_peligrosidad: 3.2,
          nivel_riesgo: 'bajo'
        },
        {
          id: 3,
          nombre: 'Ruta 38',
          zona: 'Este',
          total_siniestros: 32,
          total_delitos: 15,
          indice_peligrosidad: 6.8,
          nivel_riesgo: 'medio'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Cargar tops (más seguras y más peligrosas)
   */
  const cargarTops = async () => {
    try {
      const [seguras, peligrosas] = await Promise.all([
        reportesService.getTopAvenidasSeguras(5),
        reportesService.getTopAvenidasPeligrosas(5)
      ]);
      
      setTopSeguras(seguras.avenidas || seguras);
      setTopPeligrosas(peligrosas.avenidas || peligrosas);
      
    } catch (err) {
      console.error('Error al cargar tops:', err);
    }
  };

  /**
   * Comparar dos avenidas
   */
  const compararAvenidas = async () => {
    if (!avenida1 || !avenida2) {
      alert('Por favor selecciona dos avenidas para comparar');
      return;
    }
    
    if (avenida1 === avenida2) {
      alert('Debes seleccionar dos avenidas diferentes');
      return;
    }
    
    try {
      const resultado = await reportesService.compararAvenidas(
        parseInt(avenida1), 
        parseInt(avenida2)
      );
      setResultadoComparacion(resultado);
    } catch (err) {
      console.error('Error al comparar:', err);
      alert('Error al comparar las avenidas');
    }
  };

  // ==========================================
  // FUNCIONES AUXILIARES
  // ==========================================

  /**
   * Determinar el color según el nivel de riesgo
   */
  const getColorRiesgo = (nivelRiesgo) => {
    const colores = {
      'alto': 'bg-red-100 text-red-800 border-red-300',
      'medio': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      'bajo': 'bg-green-100 text-green-800 border-green-300',
      'muy_bajo': 'bg-blue-100 text-blue-800 border-blue-300'
    };
    return colores[nivelRiesgo] || colores['medio'];
  };

  /**
   * Obtener ícono según nivel de riesgo
   */
  const getIconoRiesgo = (nivelRiesgo) => {
    if (nivelRiesgo === 'alto') return <AlertTriangle className="w-5 h-5" />;
    if (nivelRiesgo === 'bajo' || nivelRiesgo === 'muy_bajo') return <Shield className="w-5 h-5" />;
    return <TrendingUp className="w-5 h-5" />;
  };

  /**
   * Formatear número con 2 decimales
   */
  const formatearIndice = (valor) => {
    return parseFloat(valor).toFixed(2);
  };

  // ==========================================
  // RENDERIZADO CONDICIONAL
  // ==========================================

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Cargando índice de seguridad...</p>
        </div>
      </div>
    );
  }

  // ==========================================
  // RENDERIZADO PRINCIPAL
  // ==========================================

  return (
    <div className="space-y-6 p-6">
      {/* ENCABEZADO */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
            <Shield className="w-8 h-8 text-blue-600" />
            Ruta Segura
          </h1>
          <p className="text-gray-600 mt-1">
            Índice de seguridad integral de avenidas (Siniestros + Delitos)
          </p>
        </div>
        <button
          onClick={cargarDatos}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Actualizar
        </button>
      </div>

      {/* ALERTA DE ERROR */}
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2" />
            <p className="text-yellow-800">{error}</p>
          </div>
        </div>
      )}

      {/* CONTROLES DE FILTRADO */}
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Ordenamiento */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Ordenar por
            </label>
            <select
              value={ordenamiento}
              onChange={(e) => setOrdenamiento(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="peligrosidad">Peligrosidad (Mayor a Menor)</option>
              <option value="nombre">Nombre (A-Z)</option>
              <option value="zona">Zona</option>
            </select>
          </div>

          {/* Límite de resultados */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Mostrar
            </label>
            <select
              value={limite || ''}
              onChange={(e) => setLimite(e.target.value ? parseInt(e.target.value) : null)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Todas las avenidas</option>
              <option value="10">Top 10</option>
              <option value="20">Top 20</option>
              <option value="5">Top 5</option>
            </select>
          </div>

          {/* Botón de comparación */}
          <div className="flex items-end">
            <button
              onClick={() => setMostrarComparacion(!mostrarComparacion)}
              className="w-full flex items-center justify-center gap-2 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              <GitCompare className="w-4 h-4" />
              Comparar Avenidas
            </button>
          </div>
        </div>
      </div>

      {/* PANEL DE COMPARACIÓN (Condicional) */}
      {mostrarComparacion && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <GitCompare className="w-5 h-5 text-purple-600" />
            Comparar dos avenidas
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <select
              value={avenida1}
              onChange={(e) => setAvenida1(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="">Selecciona avenida 1</option>
              {avenidas.map((av) => (
                <option key={av.id} value={av.id}>
                  {av.nombre}
                </option>
              ))}
            </select>

            <select
              value={avenida2}
              onChange={(e) => setAvenida2(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="">Selecciona avenida 2</option>
              {avenidas.map((av) => (
                <option key={av.id} value={av.id}>
                  {av.nombre}
                </option>
              ))}
            </select>

            <button
              onClick={compararAvenidas}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Comparar
            </button>
          </div>

          {/* Resultado de comparación */}
          {resultadoComparacion && (
            <div className="mt-4 p-4 bg-white rounded-lg">
              <h4 className="font-semibold mb-2">Resultado:</h4>
              <div className="grid grid-cols-2 gap-4">
                <div className="border-r border-gray-200 pr-4">
                  <p className="font-medium text-blue-600">{resultadoComparacion.avenida_1?.nombre}</p>
                  <p className="text-sm text-gray-600">
                    Índice: {formatearIndice(resultadoComparacion.avenida_1?.indice_peligrosidad)}
                  </p>
                </div>
                <div className="pl-4">
                  <p className="font-medium text-blue-600">{resultadoComparacion.avenida_2?.nombre}</p>
                  <p className="text-sm text-gray-600">
                    Índice: {formatearIndice(resultadoComparacion.avenida_2?.indice_peligrosidad)}
                  </p>
                </div>
              </div>
              <p className="mt-3 text-center text-green-700 font-medium">
                {resultadoComparacion.mensaje || 'Comparación completada'}
              </p>
            </div>
          )}
        </div>
      )}

      {/* TOPS: Más seguras y más peligrosas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Top Más Seguras */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-green-800">
            <Shield className="w-5 h-5" />
            Top 5 Avenidas Más Seguras
          </h3>
          <div className="space-y-2">
            {topSeguras.length > 0 ? (
              topSeguras.map((av, index) => (
                <div key={av.id} className="flex items-center justify-between bg-white p-3 rounded-lg">
                  <div className="flex items-center gap-3">
                    <span className="font-bold text-green-600">#{index + 1}</span>
                    <div>
                      <p className="font-medium">{av.nombre}</p>
                      <p className="text-sm text-gray-500">{av.zona}</p>
                    </div>
                  </div>
                  <span className="text-sm font-semibold text-green-700">
                    {formatearIndice(av.indice_peligrosidad || 0)}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No hay datos disponibles</p>
            )}
          </div>
        </div>

        {/* Top Más Peligrosas */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-red-800">
            <AlertTriangle className="w-5 h-5" />
            Top 5 Avenidas Más Peligrosas
          </h3>
          <div className="space-y-2">
            {topPeligrosas.length > 0 ? (
              topPeligrosas.map((av, index) => (
                <div key={av.id} className="flex items-center justify-between bg-white p-3 rounded-lg">
                  <div className="flex items-center gap-3">
                    <span className="font-bold text-red-600">#{index + 1}</span>
                    <div>
                      <p className="font-medium">{av.nombre}</p>
                      <p className="text-sm text-gray-500">{av.zona}</p>
                    </div>
                  </div>
                  <span className="text-sm font-semibold text-red-700">
                    {formatearIndice(av.indice_peligrosidad || 0)}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No hay datos disponibles</p>
            )}
          </div>
        </div>
      </div>

      {/* TABLA PRINCIPAL: Todas las avenidas */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-6">
          <h3 className="text-lg font-semibold mb-4">
            Índice de Seguridad por Avenida ({avenidas.length} resultados)
          </h3>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avenida
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Zona
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Siniestros
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Delitos
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Índice
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nivel de Riesgo
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {avenidas.length > 0 ? (
                  avenidas.map((avenida) => (
                    <tr key={avenida.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {avenida.nombre}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-600">
                          {avenida.zona}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-center">
                        <span className="text-sm text-gray-900">
                          {avenida.total_siniestros || 0}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-center">
                        <span className="text-sm text-gray-900">
                          {avenida.total_delitos || 0}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-center">
                        <span className="text-lg font-bold text-gray-900">
                          {formatearIndice(avenida.indice_peligrosidad || 0)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex justify-center">
                          <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border ${getColorRiesgo(avenida.nivel_riesgo)}`}>
                            {getIconoRiesgo(avenida.nivel_riesgo)}
                            {avenida.nivel_riesgo?.replace('_', ' ').toUpperCase() || 'MEDIO'}
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                      No hay datos disponibles
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* PIE DE PÁGINA CON INFORMACIÓN */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Nota:</strong> El índice de seguridad combina siniestros viales (70%) y reportes delictivos (30%). 
          Valores más altos indican mayor peligrosidad. El sistema actualiza los datos en tiempo real.
        </p>
      </div>
    </div>
  );
}