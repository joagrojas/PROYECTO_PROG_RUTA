import { useState } from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { 
  Menu, 
  X, 
  Home, 
  Car, 
  BarChart3, 
  Users, 
  LogOut,
  Shield,
  AlertTriangle,
  ShieldCheck
} from 'lucide-react';

export default function Layout(/* { children } */) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout, isAdmin } = useAuth();
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Siniestros', href: '/siniestros', icon: Car },
    { name: 'Reportes', href: '/reportes', icon: BarChart3 },
    { name: 'Reportes Delictivos', href: '/reportes-delito', icon: AlertTriangle },
    { name: 'Ruta Segura', href: '/ruta-segura', icon: ShieldCheck },
    ...(isAdmin() ? [{ name: 'Usuarios', href: '/usuarios', icon: Users }] : []),
  ];

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar para móviles */}
      <div className={`fixed inset-0 flex z-40 md:hidden ${sidebarOpen ? '' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6 text-white" />
            </button>
          </div>
          <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
            <div className="flex-shrink-0 flex items-center px-4">
              <Shield className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">RutaSegura</span>
            </div>
            <nav className="mt-5 px-2 space-y-1">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`group flex items-center px-2 py-2 text-base font-medium rounded-md ${
                      isActive(item.href)
                        ? 'bg-primary-100 text-primary-900'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon className="mr-4 h-6 w-6" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                  <span className="text-primary-600 font-medium">
                    {user?.nombre?.charAt(0) || 'U'}
                  </span>
                </div>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-700">{user?.nombre || 'Usuario'}</p>
                <p className="text-xs font-medium text-gray-500 capitalize">{user?.rol || 'Rol'}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sidebar para desktop */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex flex-col h-0 flex-1 border-r border-gray-200 bg-white">
            <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
              <div className="flex items-center flex-shrink-0 px-4">
                <Shield className="h-8 w-8 text-primary-600" />
                <span className="ml-2 text-xl font-bold text-gray-900">RutaSegura</span>
              </div>
              <nav className="mt-5 flex-1 px-2 bg-white space-y-1">
                {navigation.map((item) => {
                  const Icon = item.icon;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                        isActive(item.href)
                          ? 'bg-primary-100 text-primary-900'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <Icon className="mr-3 h-5 w-5" />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
            <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
              <div className="flex items-center w-full">
                <div className="flex-shrink-0">
                  <div className="h-9 w-9 rounded-full bg-primary-100 flex items-center justify-center">
                    <span className="text-primary-600 font-medium text-sm">
                      {user?.nombre?.charAt(0) || 'U'}
                    </span>
                  </div>
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm font-medium text-gray-700">{user?.nombre || 'Usuario'}</p>
                  <p className="text-xs font-medium text-gray-500 capitalize">{user?.rol || 'Rol'}</p>
                </div>
                <button
                  onClick={logout}
                  className="ml-3 p-1 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  title="Cerrar sesión"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        {/* DEBUG: mostrar ruta actual para confirmar render */}
        <div style={{ padding: 8, background: '#fff8d6', borderBottom: '1px solid #f0e68c', zIndex: 50 }}>
          <strong>DEBUG PATH:</strong> {location.pathname}
        </div>

        <main className="flex-1 p-6 overflow-auto">
          <Outlet /> {/* <-- renderiza las rutas hijas (Dashboard, Reportes, ...) */}
        </main>
      </div>
    </div>
  );
}