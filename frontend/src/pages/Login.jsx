/**
 * Página de Login
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { AlertCircle, Shield } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  const fillCredentials = (role) => {
    const credentials = {
      admin: { email: 'admin@rutasegura.com', password: 'admin123' },
      editor: { email: 'editor@rutasegura.com', password: 'editor123' },
      consultor: { email: 'consultor@rutasegura.com', password: 'consultor123' },
    };
    
    setEmail(credentials[role].email);
    setPassword(credentials[role].password);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-800 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Logo y título */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-full mb-4">
            <Shield className="w-8 h-8 text-primary-600" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">
            RutaSegura
          </h1>
          <p className="text-primary-100">
            Sistema de Gestión de Siniestros Viales
          </p>
        </div>

        {/* Formulario */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="usuario@ejemplo.com"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Contraseña
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="••••••••"
                required
              />
            </div>

            {error && (
              <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </button>
          </form>

          {/* Credenciales de prueba */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-3 text-center">
              Credenciales de prueba:
            </p>
            <div className="space-y-2">
              <button
                type="button"
                onClick={() => fillCredentials('admin')}
                className="w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
              >
                <span className="font-medium text-primary-600">Admin</span>
                <span className="text-gray-500 ml-2">
                  (Acceso completo)
                </span>
              </button>
              <button
                type="button"
                onClick={() => fillCredentials('editor')}
                className="w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
              >
                <span className="font-medium text-primary-600">Editor</span>
                <span className="text-gray-500 ml-2">
                  (Crear/Editar)
                </span>
              </button>
              <button
                type="button"
                onClick={() => fillCredentials('consultor')}
                className="w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
              >
                <span className="font-medium text-primary-600">Consultor</span>
                <span className="text-gray-500 ml-2">
                  (Solo lectura)
                </span>
              </button>
            </div>
          </div>
        </div>

        <p className="text-center text-primary-100 text-sm mt-6">
          Universidad - Programación II
        </p>
      </div>
    </div>
  );
}