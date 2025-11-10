import React, { useEffect, useState } from 'react';
import api from '../services/axiosConfig';

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ id: null, nombre: '', email: '', rol: 'usuario', password: '' });

  const fetchUsuarios = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/usuarios');
      setUsuarios(res.data || []);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsuarios();
  }, []);

  const resetForm = () => setForm({ id: null, nombre: '', email: '', rol: 'usuario', password: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { nombre: form.nombre, email: form.email, rol: form.rol, ...(form.password ? { password: form.password } : {}) };
      if (form.id) {
        await api.put(`/usuarios/${form.id}`, payload);
      } else {
        await api.post('/usuarios', payload);
      }
      await fetchUsuarios();
      resetForm();
    } catch (err) {
      console.error(err);
      setError(err);
    }
  };

  const handleEdit = (u) => {
    setForm({ id: u.id, nombre: u.nombre || '', email: u.email || '', rol: u.rol || 'usuario', password: '' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!confirm('¿Eliminar usuario?')) return;
    try {
      await api.delete(`/usuarios/${id}`);
      await fetchUsuarios();
    } catch (err) {
      console.error(err);
      setError(err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Usuarios</h1>

      <section className="mb-6 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-2">{form.id ? 'Editar usuario' : 'Crear usuario'}</h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-2">
          <input type="text" placeholder="Nombre" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} required />
          <input type="email" placeholder="Email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} required />
          <select value={form.rol} onChange={e => setForm(f => ({ ...f, rol: e.target.value }))}>
            <option value="usuario">Usuario</option>
            <option value="editor">Editor</option>
            <option value="admin">Admin</option>
          </select>
          <input type="password" placeholder="Contraseña (solo al crear/actualizar)" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} />
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
                <th>ID</th><th>Nombre</th><th>Email</th><th>Rol</th><th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.length === 0 && <tr><td colSpan="5">No hay registros</td></tr>}
              {usuarios.map(u => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td>{u.nombre}</td>
                  <td>{u.email}</td>
                  <td>{u.rol}</td>
                  <td>
                    <button onClick={() => handleEdit(u)} className="mr-2">Editar</button>
                    <button onClick={() => handleDelete(u.id)}>Eliminar</button>
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