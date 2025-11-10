/**
 * NotFound.jsx - Página 404
 */
import { useNavigate } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="text-center">
        <h1 className="text-9xl font-bold text-primary-600">404</h1>
        <h2 className="text-3xl font-bold text-gray-900 mt-4">
          Página no encontrada
        </h2>
        <p className="text-gray-600 mt-2 mb-8">
          Lo sentimos, la página que buscas no existe.
        </p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => navigate(-1)}
            className="btn-secondary flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Volver
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn-primary flex items-center gap-2"
          >
            <Home className="h-4 w-4" />
            Ir al Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}