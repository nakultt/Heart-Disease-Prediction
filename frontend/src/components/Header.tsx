import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const navClass = ({ isActive }: { isActive: boolean }) =>
  `text-sm px-2 py-1 rounded ${isActive ? 'bg-slate-800 text-white' : 'text-slate-300 hover:text-white'}`;

const Header: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <header className="bg-slate-900 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4 flex flex-col gap-3 md:flex-row md:justify-between md:items-center">
        <div className="flex items-center space-x-3">
          <div className="bg-red-500 p-2 rounded-full">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </div>
          <Link to="/" className="text-xl font-bold tracking-tight hover:text-slate-100">
            CardioGuard AI
          </Link>
        </div>
        {isAuthenticated ? (
          <nav className="flex flex-wrap items-center gap-1 md:gap-2">
            <NavLink to="/" end className={navClass}>
              Home
            </NavLink>
            <NavLink to="/clinical" className={navClass}>
              Clinical
            </NavLink>
            <NavLink to="/demographics" className={navClass}>
              Demographics
            </NavLink>
            <NavLink to="/stress" className={navClass}>
              Stress
            </NavLink>
            <NavLink to="/history" className={navClass}>
              History
            </NavLink>
            <NavLink to="/settings" className={navClass}>
              Settings
            </NavLink>
            <button
              type="button"
              onClick={handleLogout}
              className="text-sm px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white ml-1"
            >
              Log out
            </button>
          </nav>
        ) : (
          <span className="text-sm text-slate-400">Sign in to continue</span>
        )}
      </div>
    </header>
  );
};

export default Header;
