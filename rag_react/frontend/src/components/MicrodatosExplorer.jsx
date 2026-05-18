import React, { useState, useEffect } from 'react';
import { Database, Download, Table, RefreshCw, Eye, EyeOff } from 'lucide-react';
import { apiService } from '../services/api';
import '../styles/Microdatos.css';

export const MicrodatosExplorer = ({ filtrosActivos }) => {
  const [dataExport, setDataExport] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');
  const [mostrarTabla, setMostrarTabla] = useState(false);

  // Recargar los datos automáticamente si el usuario cambia los filtros mientras la tabla está visible
  useEffect(() => {
    if (mostrarTabla || dataExport) {
      const actualizarDatosFiltrados = async () => {
        setCargando(true);
        setError('');
        try {
          const res = await apiService.exportarMicrodatos(filtrosActivos);
          setDataExport(res);
        } catch (err) {
          setError('Error al actualizar los microdatos con los filtros actuales.');
        } finally {
          setCargando(false);
        }
      };
      actualizarDatosFiltrados();
    }
  }, [filtrosActivos]);

  const cargarDatos = async () => {
    setCargando(true);
    setError('');
    try {
      const res = await apiService.exportarMicrodatos(filtrosActivos);
      setDataExport(res);
      setMostrarTabla(true);
    } catch (err) {
      setError('Error al obtener microdatos desde el backend.');
    } finally {
      setCargando(false);
    }
  };

  const handleDownloadCsv = async () => {
    setCargando(true);
    setError('');
    try {
      // Siempre solicitamos la exportación fresca con los filtros activos en este instante
      const res = await apiService.exportarMicrodatos(filtrosActivos);
      setDataExport(res);
      const rawCsv = res.csv_raw;

      // Disparar descarga en el navegador
      const blob = new Blob([rawCsv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `tenderos_tolima_filtrado_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      setError('Error descargando el archivo CSV filtrado.');
    } finally {
      setCargando(false);
    }
  };

  const toggleTabla = () => {
    if (!dataExport && !mostrarTabla) {
      cargarDatos();
    } else {
      setMostrarTabla(!mostrarTabla);
    }
  };

  return (
    <div className="glass-card microdatos-container">
      <div className="microdatos-header">
        <div className="microdatos-title-box">
          <Database size={28} style={{ color: 'var(--accent-light)' }} />
          <div>
            <h3 className="microdatos-title">Explorador de Microdatos y Exportación</h3>
            <p className="microdatos-subtitle">Visualiza la tabla de registros en crudo de la submuestra activa y descárgala en CSV</p>
          </div>
        </div>

        <div className="microdatos-actions">
          <button onClick={toggleTabla} disabled={cargando} className="btn-toggle-table">
            {cargando ? (
              <RefreshCw size={18} className="spin" />
            ) : mostrarTabla ? (
              <>
                <EyeOff size={18} /> Ocultar Tabla
              </>
            ) : (
              <>
                <Eye size={18} /> Ver Tabla
              </>
            )}
          </button>
          <button onClick={handleDownloadCsv} disabled={cargando} className="btn-download-csv">
            <Download size={18} />
            <span>Descargar CSV</span>
          </button>
        </div>
      </div>

      {error && <div style={{ color: '#ef4444', marginTop: '16px', fontSize: '0.9rem' }}>{error}</div>}

      {mostrarTabla && dataExport && (
        <div className="table-wrapper">
          <table className="micro-table">
            <thead>
              <tr>
                {dataExport.columnas.map((col) => (
                  <th key={col} className="micro-th">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {dataExport.preview.map((row, idx) => (
                <tr key={idx} className="micro-tr">
                  {dataExport.columnas.map((col) => (
                    <td key={col} className="micro-td">
                      {typeof row[col] === 'number' ? Number(row[col]).toFixed(2) : String(row[col] ?? 'N/A')}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <div className="table-footer-info">
            Mostrando primeros {dataExport.preview.length} registros para vista rápida. El archivo CSV contiene el 100% de la submuestra ({dataExport.total_filas} registros filtrados).
          </div>
        </div>
      )}
    </div>
  );
};
