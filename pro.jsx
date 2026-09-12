import React, { useState } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  AlertTriangle, 
  CheckCircle2, 
  Copy, 
  Check, 
  ChevronRight,
  ExternalLink 
} from 'lucide-react';

export default function SecurityReport({ data }) {
  // Datos de fallback por si no se pasan props aún
  const report = data || {
    url: "https://ejemplo-victima.com",
    security_score: 65,
    vulnerabilities: [
      {
        id: "x-frame-options",
        title: "Falta cabecera X-Frame-Options",
        severity: "high", // high, medium, low, pass
        description: "El sitio no previene ser cargado dentro de un <iframe>, haciéndolo vulnerable a ataques de Clickjacking.",
        fix: "X-Frame-Options: DENY"
      },
      {
        id: "csp",
        title: "Content Security Policy (CSP) Ausente",
        severity: "high",
        description: "No hay restricciones sobre los orígenes desde los cuales el navegador puede cargar recursos.",
        fix: "Content-Security-Policy: default-src 'self';"
      },
      {
        id: "hsts",
        title: "Strict-Transport-Security no configurado",
        severity: "medium",
        description: "El sitio no fuerza el uso de conexiones HTTPS seguras para futuras visitas.",
        fix: "Strict-Transport-Security: max-age=31536000; includeSubDomains"
      },
      {
        id: "x-content-type",
        title: "X-Content-Type-Options correcto",
        severity: "pass",
        description: "Previene que el navegador realice MIME-sniffing sobre las respuestas.",
        fix: "X-Content-Type-Options: nosniff"
      }
    ]
  };

  const [copiedId, setCopiedId] = useState(null);

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Helper para determinar colores según la calificación (Score)
  const getScoreColor = (score) => {
    if (score >= 80) return { text: 'text-emerald-400', border: 'border-emerald-500/30', bg: 'bg-emerald-500/10' };
    if (score >= 50) return { text: 'text-amber-400', border: 'border-amber-500/30', bg: 'bg-amber-500/10' };
    return { text: 'text-rose-500', border: 'border-rose-500/30', bg: 'bg-rose-500/10' };
  };

  const scoreStyle = getScoreColor(report.security_score);

  // Helper para insignias de severidad
  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'high':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">Alta</span>;
      case 'medium':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">Media</span>;
      case 'low':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">Baja</span>;
      case 'pass':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Pasó</span>;
      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-slate-900 text-slate-100 rounded-2xl border border-slate-800 shadow-2xl space-y-8 font-sans">
      
      {/* HEADER CON RESUMEN Y SCORE */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-slate-400 text-sm mb-1">
            <span>Resultados de escaneo</span>
            <ChevronRight className="w-4 h-4 text-slate-600" />
            <a href={report.url} target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline flex items-center gap-1 font-mono">
              {report.url} <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            Cabeceras de Seguridad HTTP
          </h2>
        </div>

        {/* Circular/Gauge Score Box */}
        <div className={`flex items-center gap-4 px-6 py-4 rounded-xl border ${scoreStyle.border} ${scoreStyle.bg}`}>
          {report.security_score >= 80 ? (
            <ShieldCheck className={`w-10 h-10 ${scoreStyle.text}`} />
          ) : (
            <ShieldAlert className={`w-10 h-10 ${scoreStyle.text}`} />
          )}
          <div>
            <div className="text-xs uppercase tracking-wider font-semibold text-slate-400">Security Score</div>
            <div className={`text-3xl font-black font-mono ${scoreStyle.text}`}>
              {report.security_score} <span className="text-base font-normal text-slate-500">/ 100</span>
            </div>
          </div>
        </div>
      </div>

      {/* SECCIÓN DE VULNERABILIDADES */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
          Análisis de Hallazgos ({report.vulnerabilities.length})
        </h3>

        <div className="grid gap-4">
          {report.vulnerabilities.map((vuln) => (
            <div 
              key={vuln.id}
              className="p-5 rounded-xl bg-slate-950/60 border border-slate-800 hover:border-slate-700 transition-all space-y-3"
            >
              {/* Header de la vulnerabilidad */}
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-3">
                  {vuln.severity === 'pass' ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
                  ) : (
                    <AlertTriangle className={`w-5 h-5 mt-0.5 shrink-0 ${vuln.severity === 'high' ? 'text-rose-500' : 'text-amber-500'}`} />
                  )}
                  <div>
                    <h4 className="font-medium text-slate-100">{vuln.title}</h4>
                    <p className="text-sm text-slate-400 mt-1 leading-relaxed">
                      {vuln.description}
                    </p>
                  </div>
                </div>
                <div>
                  {getSeverityBadge(vuln.severity)}
                </div>
              </div>

              {/* Bloque de código con la solución sugerida */}
              {vuln.fix && (
                <div className="mt-3 pt-3 border-t border-slate-900 flex items-center justify-between gap-2 bg-slate-900/80 rounded-lg px-3 py-2 font-mono text-xs text-slate-300">
                  <div className="truncate">
                    <span className="text-slate-500 select-none me-2">Header sugerido:</span>
                    <span className="text-indigo-300">{vuln.fix}</span>
                  </div>
                  <button
                    onClick={() => handleCopy(vuln.id, vuln.fix)}
                    className="p-1.5 hover:bg-slate-800 rounded-md text-slate-400 hover:text-white transition-colors shrink-0"
                    title="Copiar cabecera"
                  >
                    {copiedId === vuln.id ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
