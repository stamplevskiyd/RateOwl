import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

export default function Navbar() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow px-4 py-2 flex items-center justify-between sticky top-0 z-50">
      <Link to="/" className="text-xl font-bold text-blue-600">
        ReviewsApp
      </Link>
      {token && (
        <button onClick={handleLogout} className="text-sm text-red-500">
          Logout
        </button>
      )}
    </nav>
  );
}
