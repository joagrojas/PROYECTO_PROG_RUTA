import React, { useEffect, useState } from 'react';
import api from '../services/axiosConfig';

export default function Siniestros() {
  const [siniestros, setSiniestros] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({
    id: null,
    fecha: '',
    ubicacion: '',
    avenida_id: '',
    tipo_id: '',
    nivel_gravedad: 'media',
    descripcion: ''
  });

  const fetchSiniestros = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/siniestros');
      setSiniestros(res.data || []);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSiniestros();
  }, []);

  const resetForm = () => setForm({ id: null, fecha: '', ubicacion: '', avenida_id: '', tipo_id: '', nivel_gravedad: 'media', descripcion: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        fecha: form.fecha,
        ubicacion: form.ubicacion,
        avenida_id: form.avenida_id ? Number(form.avenida_id) : null,
        tipo_id: form.tipo_id ? Number(form.tipo_id) : null,
        nivel_gravedad: form.nivel_gravedad,
        descripcion: form.descripcion
      };
      if (form.id) {
        await api.put(`/siniestros/${form.id}`, payload);
      } else {
        await api.post('/siniestros', payload);
      }
      await fetchSiniestros();
      resetForm();
    } catch (err) {
      console.error(err);
      setError(err);
    }
  };

  const handleEdit = (s) => {
    setForm({
      id: s.id,
      fecha: s.fecha ? s.fecha.split('T')[0] : '',
      ubicacion: s.ubicacion || '',
      avenida_id: s.avenida_id ?? '',
      tipo_id: s.tipo_id ?? '',
      nivel_gravedad: s.nivel_gravedad || 'media',
      descripcion: s.descripcion || ''
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!confirm('¿Eliminar siniestro?')) return;
    try {
      await api.delete(`/siniestros/${id}`);
      await fetchSiniestros();
    } catch (err) {
      console.error(err);
      setError(err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Siniestros</h1>

      <section className="mb-6 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-2">{form.id ? 'Editar siniestro' : 'Crear siniestro'}</h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-2">
          <input type="date" value={form.fecha} onChange={e => setForm(f => ({ ...f, fecha: e.target.value }))} required />
          <input type="text" placeholder="Ubicación" value={form.ubicacion} onChange={e => setForm(f => ({ ...f, ubicacion: e.target.value }))} required />
          <input type="number" placeholder="Avenida ID" value={form.avenida_id} onChange={e => setForm(f => ({ ...f, avenida_id: e.target.value }))} />
          <input type="number" placeholder="Tipo Siniestro ID" value={form.tipo_id} onChange={e => setForm(f => ({ ...f, tipo_id: e.target.value }))} />
          <select value={form.nivel_gravedad} onChange={e => setForm(f => ({ ...f, nivel_gravedad: e.target.value }))}>
            <option value="alta">Alta</option>
            <option value="media">Media</option>
            <option value="baja">Baja</option>
          </select>
          <textarea placeholder="Descripción" value={form.descripcion} onChange={e => setForm(f => ({ ...f, descripcion: e.target.value }))} />
          <div className="flex gap-2">
            <button type="submit" className="btn btn-primary">{form.id ? 'Guardar' : 'Crear'}</button>
            <button type="button" className="btn" onClick={resetForm}>Limpiar</button>
          </div>
        </form>
        {error && <div className="text-red-600 mt-2">Error: {error.message || 'problema'}</div>}
      </section>

      <section className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Listado</h2>
        {loading ? (
          <div>Cargando...</div>
        ) : (
          <table className="w-full table-auto text-sm">
            <thead>
              <tr>
                <th>ID</th><th>Fecha</th><th>Ubicación</th><th>Gravedad</th><th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {siniestros.length === 0 && <tr><td colSpan="5">No hay registros</td></tr>}
              {siniestros.map(s => (
                <tr key={s.id}>
                  <td>{s.id}</td>
                  <td>{s.fecha ? s.fecha.split('T')[0] : ''}</td>
                  <td>{s.ubicacion}</td>
                  <td>{s.nivel_gravedad}</td>
                  <td>
                    <button onClick={() => handleEdit(s)} className="mr-2">Editar</button>
                    <button onClick={() => handleDelete(s.id)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}