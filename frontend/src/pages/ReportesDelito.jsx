/**
 * Página de Reportes Delictivos
 * Permite visualizar, crear, editar y eliminar reportes de delitos
 */
import { useState, useEffect } from 'react';
import { reportesDelitoService, avenidasService } from '../services/api';
import { Shield, Plus, Edit, Trash2, AlertCircle, Filter } from 'lucide-react';

export default function ReportesDelito() {
  // Estados
  const [reportes, setReportes] = useState([]);
  const [avenidas, setAvenidas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingReporte, setEditingReporte] = useState(null);
  
  // Filtros
  const [filtros, setFiltros] = useState({
    tipo_delito: '',
    nivel_peligrosidad: '',
    avenida_id: ''
  });

  // Formulario
  const [formData, setFormData] = useState({
    fecha: '',
    hora: '',
    avenida_id: '',
    tipo_delito: 'robo',
    nivel_peligrosidad: 'media',
    descripcion: '',
    usuario_id: 1 // Por ahora hardcodeado, idealmente vendría del contexto de auth
  });

  // Cargar datos iniciales
  useEffect(() => {
    cargarDatos();
    cargarAvenidas();
  }, [filtros]);

  const cargarDatos = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (filtros.tipo_delito) params.tipo_delito = filtros.tipo_delito;
      if (filtros.nivel_peligrosidad) params.nivel_peligrosidad = filtros.nivel_peligrosidad;
      if (filtros.avenida_id) params.avenida_id = filtros.avenida_id;

      const data = await reportesDelitoService.getAll(params);
      setReportes(data);
    } catch (err) {
      console.error('Error al cargar reportes:', err);
      setError('Error al cargar los reportes delictivos');
    } finally {
      setLoading(false);
    }
  };

  const cargarAvenidas = async () => {
    try {
      const data = await avenidasService.getAll();
      setAvenidas(data);
    } catch (err) {
      console.error('Error al cargar avenidas:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingReporte) {
        await reportesDelitoService.update(editingReporte.id, formData);
      } else {
        await reportesDelitoService.create(formData);
      }
      setShowModal(false);
      resetForm();
      cargarDatos();
    } catch (err) {
      console.error('Error al guardar:', err);
      alert('Error al guardar el reporte');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este reporte?')) {
      try {
        await reportesDelitoService.delete(id);
        cargarDatos();
      } catch (err) {
        console.error('Error al eliminar:', err);
        alert('Error al eliminar el reporte');
      }
    }
  };

  const handleEdit = (reporte) => {
    setEditingReporte(reporte);
    setFormData({
      fecha: reporte.fecha,
      hora: reporte.hora,
      avenida_id: reporte.avenida_id,
      tipo_delito: reporte.tipo_delito,
      nivel_peligrosidad: reporte.nivel_peligrosidad,
      descripcion: reporte.descripcion || '',
      usuario_id: reporte.usuario_id
    });
    setShowModal(true);
  };

  const resetForm = () => {
    setFormData({
      fecha: '',
      hora: '',
      avenida_id: '',
      tipo_delito: 'robo',
      nivel_peligrosidad: 'media',
      descripcion: '',
      usuario_id: 1
    });
    setEditingReporte(null);
  };

  const handleNuevoReporte = () => {
    resetForm();
    setShowModal(true);
  };

  // Función para obtener color según peligrosidad
  const getPeligrosidadColor = (nivel) => {
    switch (nivel) {
      case 'alta':
        return 'bg-red-100 text-red-800';
      case 'media':
        return 'bg-yellow-100 text-yellow-800';
      case 'baja':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTipoDelitoIcon = (tipo) => {
    switch (tipo) {
      case 'robo':
        return '🚨';
      case 'asalto':
        return '⚠️';
      case 'hurto':
        return '👛';
      case 'vandalismo':
        return '🔨';
      default:
        return '📋';
    }
  };

  if (loading && reportes.length === 0) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando reportes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
            <Shield className="w-8 h-8 text-blue-600" />
            Reportes Delictivos
          </h1>
          <p className="text-gray-600 mt-1">Gestión de reportes de seguridad ciudadana</p>
        </div>
        <button
          onClick={handleNuevoReporte}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Nuevo Reporte
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <Filter className="w-5 h-5 text-gray-600" />
          <h3 className="text-lg font-semibold">Filtros</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tipo de Delito
            </label>
            <select
              value={filtros.tipo_delito}
              onChange={(e) => setFiltros({ ...filtros, tipo_delito: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todos</option>
              <option value="robo">Robo</option>
              <option value="asalto">Asalto</option>
              <option value="hurto">Hurto</option>
              <option value="vandalismo">Vandalismo</option>
              <option value="otro">Otro</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nivel de Peligrosidad
            </label>
            <select
              value={filtros.nivel_peligrosidad}
              onChange={(e) => setFiltros({ ...filtros, nivel_peligrosidad: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todos</option>
              <option value="alta">Alta</option>
              <option value="media">Media</option>
              <option value="baja">Baja</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Avenida
            </label>
            <select
              value={filtros.avenida_id}
              onChange={(e) => setFiltros({ ...filtros, avenida_id: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todas</option>
              {avenidas.map((avenida) => (
                <option key={avenida.id} value={avenida.id}>
                  {avenida.nombre}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-red-600" />
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Tabla de Reportes */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Fecha/Hora
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Tipo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Avenida
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Peligrosidad
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Descripción
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {reportes.map((reporte) => (
                <tr key={reporte.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div>{new Date(reporte.fecha).toLocaleDateString('es-AR')}</div>
                    <div className="text-gray-500">{reporte.hora}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className="flex items-center gap-2">
                      <span>{getTipoDelitoIcon(reporte.tipo_delito)}</span>
                      <span className="capitalize">{reporte.tipo_delito}</span>
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {reporte.avenida_nombre}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPeligrosidadColor(reporte.nivel_peligrosidad)}`}>
                      {reporte.nivel_peligrosidad.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                    {reporte.descripcion || 'Sin descripción'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleEdit(reporte)}
                        className="text-blue-600 hover:text-blue-800 transition-colors"
                        title="Editar"
                      >
                        <Edit className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => handleDelete(reporte.id)}
                        className="text-red-600 hover:text-red-800 transition-colors"
                        title="Eliminar"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {reportes.length === 0 && !loading && (
          <div className="text-center py-12">
            <Shield className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No hay reportes delictivos
            </h3>
            <p className="text-gray-600 mb-4">
              Comienza agregando un nuevo reporte de seguridad
            </p>
            <button
              onClick={handleNuevoReporte}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Agregar Primer Reporte
            </button>
          </div>
        )}
      </div>

      {/* Modal de Formulario */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">
              {editingReporte ? 'Editar Reporte' : 'Nuevo Reporte Delictivo'}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fecha *
                  </label>
                  <input
                    type="date"
                    value={formData.fecha}
                    onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Hora *
                  </label>
                  <input
                    type="time"
                    value={formData.hora}
                    onChange={(e) => setFormData({ ...formData, hora: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Avenida *
                  </label>
                  <select
                    value={formData.avenida_id}
                    onChange={(e) => setFormData({ ...formData, avenida_id: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2"
                    required
                  >
                    <option value="">Seleccionar...</option>
                    {avenidas.map((avenida) => (
                      <option key={avenida.id} value={avenida.id}>
                        {avenida.nombre}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tipo de Delito *
                  </label>
                  <select
                    value={formData.tipo_delito}
                    onChange={(e) => setFormData({ ...formData, tipo_delito: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2"
                    required
                  >
                    <option value="robo">Robo</option>
                    <option value="asalto">Asalto</option>
                    <option value="hurto">Hurto</option>
                    <option value="vandalismo">Vandalismo</option>
                    <option value="otro">Otro</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nivel de Peligrosidad *
                  </label>
                  <select
                    value={formData.nivel_peligrosidad}
                    onChange={(e) => setFormData({ ...formData, nivel_peligrosidad: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2"
                    required
                  >
                    <option value="alta">Alta</option>
                    <option value="media">Media</option>
                    <option value="baja">Baja</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Descripción
                </label>
                <textarea
                  value={formData.descripcion}
                  onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                  rows="3"
                  placeholder="Descripción detallada del incidente..."
                />
              </div>

              <div className="flex justify-end gap-2 mt-6">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    resetForm();
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editingReporte ? 'Actualizar' : 'Crear'} Reporte
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}