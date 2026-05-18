import React, { useEffect, useState } from 'react';
import { Sun, Moon } from 'lucide-react';
import '../styles/ThemeToggle.css';

export const ThemeToggle = () => {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return (
    <button 
      onClick={toggleTheme} 
      className="btn-theme-toggle"
      title={theme === 'dark' ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
    >
      {theme === 'dark' ? <Sun size={18} className="icon-sun" /> : <Moon size={18} className="icon-moon" />}
      <span>{theme === 'dark' ? 'Claro' : 'Oscuro'}</span>
    </button>
  );
};
