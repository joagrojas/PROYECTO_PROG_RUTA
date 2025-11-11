import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';         
import Login from './pages/Login';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Siniestros from './pages/Siniestros';
//import Reportes from './pages/Reportes';
import ReportesDelito from './pages/ReportesDelito';
import Usuarios from './pages/Usuarios';
import NotFound from './pages/NotFound';
import RutaSegura from './pages/RutaSegura';

// Componente para proteger rutas
function ProtectedRoute({ children, requireAdmin = false }) {
  const { user, loading } = useAuth();

  // CLAVE: Esperar a que termine de cargar
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // Si no hay usuario, redirigir a login
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Si requiere admin y no lo es, redirigir a dashboard
  if (requireAdmin && user.rol !== 'admin') {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ruta pública - Login */}
        <Route path="/login" element={<Login />} />

        {/* Rutas protegidas con Layout */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="siniestros" element={<Siniestros />} />
          
          <Route path="reportes-delito" element={<ReportesDelito />} />
          <Route path="/ruta-segura" element={<RutaSegura />} />  {/* ← NUEVA RUTA */}
          {/* Ruta solo para admin */}
          <Route
            path="usuarios"
            element={
              <ProtectedRoute requireAdmin={true}>
                <Usuarios />
              </ProtectedRoute>
            }
          />
        </Route>

        {/* 404 Not Found */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;