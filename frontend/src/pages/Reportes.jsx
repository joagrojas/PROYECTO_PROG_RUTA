/**
 * Dashboard principal con estadísticas y gráficos
 */
import { useState, useEffect } from 'react';
import { reportesService } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { AlertTriangle, TrendingUp, MapPin, Car, RefreshCw } from 'lucide-react';

const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];

export default function Dashboard() {
  const [resumen, setResumen] = useState(null);
  const [siniestrosPorZona, setSiniestrosPorZona] = useState([]);
  const [estadisticasPorTipo, setEstadisticasPorTipo] = useState([]);
  const [siniestrosPorDia, setSiniestrosPorDia] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Verificar que las funciones existen
  useEffect(() => {
    console.log('🔍 reportesService:', reportesService);
    console.log('🔍 getResumenGeneral:', reportesService?.getResumenGeneral);
    console.log('🔍 getSiniestrosPorZona:', reportesService?.getSiniestrosPorZona);
  }, []);

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('📊 Iniciando carga de datos...');

      // VERIFICAR SI LAS FUNCIONES EXISTEN
      if (typeof reportesService.getResumenGeneral !== 'function') {
        throw new Error('reportesService no está configurado correctamente');
      }

      // Cargar datos usando el endpoint unificado (más eficiente)
      console.log('🔄 Usando endpoint unificado...');
      const estadisticasCompletas = await reportesService.getEstadisticas();
      console.log('✅ Datos unificados recibidos:', estadisticasCompletas);

      // Si el endpoint unificado funciona, usamos esos datos
      if (estadisticasCompletas) {
        setResumen({
          total_siniestros: estadisticasCompletas.total_siniestros || 0,
          total_fallecidos: estadisticasCompletas.total_victimas || 0,
          total_heridos: 0, // Puedes ajustar según tu API
          siniestros_graves: estadisticasCompletas.por_gravedad?.[0]?.cantidad || 0
        });
        
        setSiniestrosPorZona(estadisticasCompletas.puntos_criticos || []);
        setEstadisticasPorTipo(estadisticasCompletas.por_tipo || []);
        setSiniestrosPorDia(estadisticasCompletas.por_dia_semana || []);
      } else {
        // Fallback: cargar datos individualmente
        console.log('🔄 Usando endpoints individuales...');
        const [resumenData, zonasData, tiposData, diasData] = await Promise.all([
          reportesService.getResumenGeneral(),
          reportesService.getSiniestrosPorZona(),
          reportesService.getEstadisticasPorTipo(),
          reportesService.getSiniestrosPorDiaSemana(),
        ]);

        setResumen(resumenData);
        setSiniestrosPorZona(zonasData);
        setEstadisticasPorTipo(tiposData);
        setSiniestrosPorDia(diasData);
      }
      
    } catch (error) {
      console.error('❌ Error al cargar datos:', error);
      setError(`Error: ${error.message}`);
      
      // Datos de ejemplo para desarrollo
      setResumen({
        total_siniestros: 156,
        total_fallecidos: 23,
        total_heridos: 89,
        siniestros_graves: 45
      });
      
      setSiniestrosPorZona([
        { zona: 'Centro', total_siniestros: 45, total_fallecidos: 8 },
        { zona: 'Norte', total_siniestros: 32, total_fallecidos: 5 },
        { zona: 'Sur', total_siniestros: 28, total_fallecidos: 4 },
        { zona: 'Este', total_siniestros: 35, total_fallecidos: 6 },
        { zona: 'Oeste', total_siniestros: 16, total_fallecidos: 0 }
      ]);
      
      setEstadisticasPorTipo([
        { tipo_siniestro: 'Colisión', cantidad: 67, fallecidos: 12, heridos: 45 },
        { tipo_siniestro: 'Atropello', cantidad: 34, fallecidos: 8, heridos: 22 },
        { tipo_siniestro: 'Vuelco', cantidad: 28, fallecidos: 3, heridos: 15 },
        { tipo_siniestro: 'Incendio', cantidad: 12, fallecidos: 0, heridos: 8 },
        { tipo_siniestro: 'Otros', cantidad: 15, fallecidos: 0, heridos: 9 }
      ]);
      
      setSiniestrosPorDia([
        { dia_semana: 'Lunes', cantidad: 22, fallecidos: 3 },
        { dia_semana: 'Martes', cantidad: 18, fallecidos: 2 },
        { dia_semana: 'Miércoles', cantidad: 25, fallecidos: 4 },
        { dia_semana: 'Jueves', cantidad: 28, fallecidos: 5 },
        { dia_semana: 'Viernes', cantidad: 35, fallecidos: 6 },
        { dia_semana: 'Sábado', cantidad: 18, fallecidos: 2 },
        { dia_semana: 'Domingo', cantidad: 10, fallecidos: 1 }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const recargarDatos = () => {
    cargarDatos();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Cargando estadísticas...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Vista general de siniestros viales</p>
        </div>
        <div className="flex gap-3">
          {error && (
            <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
              Modo Demo
            </span>
          )}
          <button
            onClick={recargarDatos}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Actualizar
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2" />
            <p className="text-yellow-800">{error}</p>
          </div>
        </div>
      )}

      {/* Tarjetas de resumen */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Siniestros</p>
              <p className="text-3xl font-bold text-gray-900 mt-1">
                {resumen?.total_siniestros || 0}
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <AlertTriangle className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Víctimas Fatales</p>
              <p className="text-3xl font-bold text-red-600 mt-1">
                {resumen?.total_fallecidos || 0}
              </p>
            </div>
            <div className="p-3 bg-red-100 rounded-full">
              <TrendingUp className="w-6 h-6 text-red-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Heridos</p>
              <p className="text-3xl font-bold text-orange-600 mt-1">
                {resumen?.total_heridos || 0}
              </p>
            </div>
            <div className="p-3 bg-orange-100 rounded-full">
              <Car className="w-6 h-6 text-orange-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Siniestros Graves</p>
              <p className="text-3xl font-bold text-red-900 mt-1">
                {resumen?.siniestros_graves || 0}
              </p>
            </div>
            <div className="p-3 bg-red-200 rounded-full">
              <MapPin className="w-6 h-6 text-red-900" />
            </div>
          </div>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Siniestros por Zona */}
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <h3 className="text-lg font-semibold mb-4">Siniestros por Zona</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={siniestrosPorZona}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="zona" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total_siniestros" fill="#3b82f6" name="Siniestros" />
              <Bar dataKey="total_fallecidos" fill="#ef4444" name="Fallecidos" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Estadísticas por Tipo */}
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <h3 className="text-lg font-semibold mb-4">Distribución por Tipo</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={estadisticasPorTipo}
                dataKey="cantidad"
                nameKey="tipo_siniestro"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ tipo_siniestro, cantidad }) => `${tipo_siniestro}: ${cantidad}`}
              >
                {estadisticasPorTipo.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Siniestros por Día de la Semana */}
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200 lg:col-span-2">
          <h3 className="text-lg font-semibold mb-4">Siniestros por Día de la Semana</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={siniestrosPorDia}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="dia_semana" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="cantidad" 
                stroke="#3b82f6" 
                strokeWidth={2}
                name="Total Siniestros"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tabla de tipos de siniestro */}
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <h3 className="text-lg font-semibold mb-4">Detalle por Tipo de Siniestro</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Tipo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Cantidad
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Fallecidos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Heridos
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {estadisticasPorTipo.map((tipo, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {tipo.tipo_siniestro}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {tipo.cantidad}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">
                    {tipo.fallecidos || 0}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-orange-600">
                    {tipo.heridos || 0}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}