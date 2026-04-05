import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const navClass = ({ isActive }: { isActive: boolean }) =>
  `text-sm font-medium px-4 py-2 rounded-full transition-all duration-200 ${
    isActive
      ? 'bg-blue-600/10 text-blue-600 shadow-sm border border-blue-100'
      : 'text-slate-600 hover:text-blue-600 hover:bg-slate-50'
  }`;

const Header: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <header className="sticky top-0 z-50 bg-white/80 glass shadow-soft border-b border-slate-200/50">
      <div className="container mx-auto px-6 h-20 flex justify-between items-center whitespace-nowrap">
        {/* Branding */}
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2.5 rounded-xl shadow-glow group-hover:scale-105 transition-transform duration-300">
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
                strokeWidth={2.5}
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </div>
          <span className="text-2xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-slate-900 to-slate-700 hidden sm:block">
            CardioGuard AI
          </span>
        </Link>

        {/* Navigation */}
        <div className="flex-1 flex justify-end items-center">
          {isAuthenticated ? (
            <nav className="flex items-center space-x-1 sm:space-x-3 overflow-x-auto no-scrollbar py-2">
              <NavLink to="/" end className={navClass}>
                Home
              </NavLink>
              <NavLink to="/history" className={navClass}>
                History
              </NavLink>
              <NavLink to="/settings" className={navClass}>
                Profile
              </NavLink>
              <div className="w-px h-6 bg-slate-200 mx-2 hidden sm:block"></div>
              <button
                type="button"
                onClick={handleLogout}
                className="text-sm font-semibold px-5 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 text-white transition-colors shadow-sm ml-2 hidden sm:block"
              >
                Log out
              </button>
              {/* Mobile Logout Icon */}
              <button
                type="button"
                onClick={handleLogout}
                className="p-2.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 sm:hidden ml-2"
                aria-label="Logout"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>
              </button>
            </nav>
          ) : (
            <Link
              to="/login"
              className="text-sm font-bold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 px-6 py-2.5 rounded-full transition-colors"
            >
              Sign In
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
