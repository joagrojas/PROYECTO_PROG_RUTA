/**
 * Dashboard principal con estadísticas y gráficos
 */
import { useState, useEffect } from 'react';
// Corregir el import según tu estructura de archivos
import { getResumen, getSiniestrosPorZona, getEstadisticasPorTipo, getSiniestrosPorDia } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { AlertTriangle, TrendingUp, MapPin, Car } from 'lucide-react';

const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];

export default function Dashboard() {
  const [resumen, setResumen] = useState(null);
  const [siniestrosPorZona, setSiniestrosPorZona] = useState([]);
  const [estadisticasPorTipo, setEstadisticasPorTipo] = useState([]);
  const [siniestrosPorDia, setSiniestrosPorDia] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    setLoading(true);
    setError(null);
    try {
        // Resumen general
        const resumenResp = await getResumen();
        setResumen(resumenResp?.data ?? {});

        // Siniestros por zona 
        const respZona = await getSiniestrosPorZona();
        const zonasData = respZona?.data?.map(item => ({
            ...item,
            total: Number(item.total)
        })) ?? [];
        setSiniestrosPorZona(zonasData);

        // Estadísticas por tipo
        const respTipo = await getEstadisticasPorTipo();
        const tiposData = respTipo?.data?.map(item => ({
            tipo_siniestro: item.tipo,
            cantidad: Number(item.total),
            gravedad: Number(item.gravedad_media)
        })) ?? [];
        setEstadisticasPorTipo(tiposData);

        // Siniestros por día
        const respDia = await getSiniestrosPorDia();
        const diasData = respDia?.data?.map((item, index) => ({
            dia_semana: item.dia_semana ?? `Día ${index + 1}`,
            total: Number(item.total)
        })) ?? [];
        setSiniestrosPorDia(diasData);

    } catch (err) {
        console.error("Error cargando datos:", err);
        setError(err?.message ?? "Error al cargar datos");
    } finally {
        setLoading(false);
    }
  };

  // Función para recargar datos
  const recargarDatos = () => {
    cargarDatos();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando estadísticas...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Error al cargar datos</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={recargarDatos}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Reintentar
          </button>
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
        <button
          onClick={recargarDatos}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Actualizar Datos
        </button>
      </div>

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
              {/* Corregido: usar 'total' que es el campo que devuelve el backend */}
              <Bar dataKey="total" fill="#3b82f6" name="Total Siniestros" />
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
                label={(entry) => entry.tipo_siniestro}
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
              {/* Corregido: usar 'total' en lugar de 'cantidad' */}
              <Line 
                type="monotone" 
                dataKey="total" 
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
                  Gravedad Promedio
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
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 font-medium">
                    {tipo.gravedad ? tipo.gravedad.toFixed(2) : 'N/A'}
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