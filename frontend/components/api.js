window.API_BASE = 'http://localhost:8000/api';

window.mensajeErrorApi = (datos, mensajePredeterminado) =>
  datos?.detail || datos?.mensaje || mensajePredeterminado;
