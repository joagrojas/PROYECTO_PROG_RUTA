import React, { useEffect, useState } from 'react';
import api from '../services/axiosConfig';

export default function Siniestros() {
  const [siniestros, setSiniestros] = useState([]);
  const [avenidas, setAvenidas] = useState([]);
  const [tiposSiniestro, setTiposSiniestro] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({
    id: null,
    fecha: '',
    hora: '',
    avenida_id: '',
    tipo_id: '',
    nivel_gravedad: 'media',
    victimas_fatales: 0,
    heridos: 0,
    num_vehiculos: 0,
    observaciones: ''
  });

  // Cargar datos iniciales
  useEffect(() => {
    cargarDatosIniciales();
  }, []);

  const cargarDatosIniciales = async () => {
    try {
      setLoading(true);
      // Cargar siniestros, avenidas y tipos en paralelo
      const [resSiniestros, resAvenidas, resTipos] = await Promise.all([
        api.get('/siniestros/'),
        api.get('/avenidas/'),
        api.get('/tipos-siniestro/')
      ]);
      
      setSiniestros(resSiniestros.data || []);
      setAvenidas(resAvenidas.data || []);
      setTiposSiniestro(resTipos.data || []);
    } catch (err) {
      console.error('Error al cargar datos:', err);
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSiniestros = async () => {
    try {
      const res = await api.get('/siniestros/');
      setSiniestros(res.data || []);
    } catch (err) {
      console.error('Error al cargar siniestros:', err);
      setError(err);
    }
  };

  const resetForm = () => {
    setForm({
      id: null,
      fecha: '',
      hora: '',
      avenida_id: '',
      tipo_id: '',
      nivel_gravedad: 'media',
      victimas_fatales: 0,
      heridos: 0,
      num_vehiculos: 0,
      observaciones: ''
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    
    try {
      // Construir payload con los campos correctos
      const payload = {
        fecha: form.fecha || null,
        hora: form.hora || null,
        avenida_id: Number(form.avenida_id),
        tipo_id: Number(form.tipo_id),
        nivel_gravedad: form.nivel_gravedad,
        victimas_fatales: Number(form.victimas_fatales) || 0,
        heridos: Number(form.heridos) || 0,
        num_vehiculos: Number(form.num_vehiculos) || 0,
        observaciones: form.observaciones || null
      };

      console.log('Enviando payload:', payload);

      if (form.id) {
        // Actualizar
        await api.put(`/siniestros/${form.id}`, payload);
      } else {
        // Crear
        await api.post('/siniestros/', payload);
      }
      
      await fetchSiniestros();
      resetForm();
    } catch (err) {
      console.error('Error al guardar siniestro:', err);
      setError(err.response?.data?.detail || err.message || 'Error al guardar');
      alert(`Error: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleEdit = (s) => {
    setForm({
      id: s.id,
      fecha: s.fecha ? (s.fecha.includes('T') ? s.fecha.split('T')[0] : s.fecha) : '',
      hora: s.hora || '',
      avenida_id: s.avenida_id || '',
      tipo_id: s.tipo_id || '',
      nivel_gravedad: s.nivel_gravedad || 'media',
      victimas_fatales: s.victimas_fatales || 0,
      heridos: s.heridos || 0,
      num_vehiculos: s.num_vehiculos || 0,
      observaciones: s.observaciones || ''
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!confirm('¿Eliminar siniestro?')) return;
    try {
      await api.delete(`/siniestros/${id}`);
      await fetchSiniestros();
    } catch (err) {
      console.error('Error al eliminar:', err);
      setError(err);
      alert('Error al eliminar el siniestro');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Gestión de Siniestros</h1>

      {/* Formulario */}
      <section className="mb-6 bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-4">
          {form.id ? 'Editar Siniestro' : 'Crear Nuevo Siniestro'}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Fecha */}
            <div>
              <label className="block text-sm font-medium mb-1">Fecha *</label>
              <input
                type="date"
                value={form.fecha}
                onChange={e => setForm(f => ({ ...f, fecha: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
                required
              />
            </div>

            {/* Hora */}
            <div>
              <label className="block text-sm font-medium mb-1">Hora</label>
              <input
                type="time"
                value={form.hora}
                onChange={e => setForm(f => ({ ...f, hora: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            {/* Avenida */}
            <div>
              <label className="block text-sm font-medium mb-1">Avenida *</label>
              <select
                value={form.avenida_id}
                onChange={e => setForm(f => ({ ...f, avenida_id: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
                required
              >
                <option value="">Seleccionar avenida</option>
                {avenidas.map(av => (
                  <option key={av.id} value={av.id}>{av.nombre}</option>
                ))}
              </select>
            </div>

            {/* Tipo de Siniestro */}
            <div>
              <label className="block text-sm font-medium mb-1">Tipo de Siniestro *</label>
              <select
                value={form.tipo_id}
                onChange={e => setForm(f => ({ ...f, tipo_id: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
                required
              >
                <option value="">Seleccionar tipo</option>
                {tiposSiniestro.map(tipo => (
                  <option key={tipo.id} value={tipo.id}>{tipo.nombre}</option>
                ))}
              </select>
            </div>

            {/* Nivel de Gravedad */}
            <div>
              <label className="block text-sm font-medium mb-1">Nivel de Gravedad *</label>
              <select
                value={form.nivel_gravedad}
                onChange={e => setForm(f => ({ ...f, nivel_gravedad: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
                required
              >
                <option value="baja">Baja</option>
                <option value="media">Media</option>
                <option value="alta">Alta</option>
              </select>
            </div>

            {/* Víctimas Fatales */}
            <div>
              <label className="block text-sm font-medium mb-1">Víctimas Fatales</label>
              <input
                type="number"
                min="0"
                value={form.victimas_fatales}
                onChange={e => setForm(f => ({ ...f, victimas_fatales: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            {/* Heridos */}
            <div>
              <label className="block text-sm font-medium mb-1">Heridos</label>
              <input
                type="number"
                min="0"
                value={form.heridos}
                onChange={e => setForm(f => ({ ...f, heridos: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            {/* Número de Vehículos */}
            <div>
              <label className="block text-sm font-medium mb-1">Vehículos Involucrados</label>
              <input
                type="number"
                min="0"
                value={form.num_vehiculos}
                onChange={e => setForm(f => ({ ...f, num_vehiculos: e.target.value }))}
                className="w-full px-3 py-2 border rounded"
              />
            </div>
          </div>

          {/* Observaciones */}
          <div>
            <label className="block text-sm font-medium mb-1">Observaciones</label>
            <textarea
              value={form.observaciones}
              onChange={e => setForm(f => ({ ...f, observaciones: e.target.value }))}
              className="w-full px-3 py-2 border rounded"
              rows="3"
              placeholder="Detalles adicionales del siniestro..."
            />
          </div>

          {/* Botones */}
          <div className="flex gap-3">
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {form.id ? 'Actualizar' : 'Crear'}
            </button>
            <button
              type="button"
              onClick={resetForm}
              className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              Limpiar
            </button>
          </div>
        </form>
        
        {error && (
          <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {typeof error === 'string' ? error : error.message || 'Error desconocido'}
          </div>
        )}
      </section>

      {/* Listado */}
      <section className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-4">Listado de Siniestros</h2>
        {loading ? (
          <div className="text-center py-4">Cargando...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hora</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ubicación</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gravedad</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {siniestros.length === 0 ? (
                  <tr>
                    <td colSpan="7" className="px-4 py-4 text-center text-gray-500">
                      No hay siniestros registrados
                    </td>
                  </tr>
                ) : (
                  siniestros.map(s => (
                    <tr key={s.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 whitespace-nowrap text-sm">{s.id}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {s.fecha ? (s.fecha.includes('T') ? s.fecha.split('T')[0] : s.fecha) : '-'}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {s.hora || '-'}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {s.avenida_nombre || `Avenida ID ${s.avenida_id}`}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {s.tipo_nombre || `Tipo ID ${s.tipo_id}`}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          s.nivel_gravedad === 'alta' ? 'bg-red-100 text-red-800' :
                          s.nivel_gravedad === 'media' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {s.nivel_gravedad || '-'}
                        </span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        <button
                          onClick={() => handleEdit(s)}
                          className="text-blue-600 hover:text-blue-800 mr-3"
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => handleDelete(s.id)}
                          className="text-red-600 hover:text-red-800"
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}