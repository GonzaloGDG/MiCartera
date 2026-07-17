
const API_BASE = 'http://localhost:5000/api';

const form          = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const usernameError = document.getElementById('usernameError');
const passwordError = document.getElementById('passwordError');
const loginError    = document.getElementById('loginError');
const btnLogin      = document.getElementById('btnLogin');
const btnSpinner    = document.getElementById('btnSpinner');
const toggleBtn     = document.getElementById('togglePassword');

// ── Toggle mostrar/ocultar contraseña ──────────────────
toggleBtn.addEventListener('click', () => {
  const isPassword = passwordInput.type === 'password';
  passwordInput.type = isPassword ? 'text' : 'password';
  toggleBtn.textContent = isPassword ? '🙈' : '👁️';
});

// ── Validación de campos ───────────────────────────────
function validateFields() {
  let valid = true;

  if (!usernameInput.value.trim()) {
    usernameError.textContent = 'El usuario es obligatorio';
    usernameInput.classList.add('input-error');
    valid = false;
  } else {
    usernameError.textContent = '';
    usernameInput.classList.remove('input-error');
  }

  if (!passwordInput.value.trim()) {
    passwordError.textContent = 'La contraseña es obligatoria';
    passwordInput.classList.add('input-error');
    valid = false;
  } else {
    passwordError.textContent = '';
    passwordInput.classList.remove('input-error');
  }

  return valid;
}

// ── Estado del botón ───────────────────────────────────
function setLoading(loading) {
  btnLogin.disabled = loading;
  btnLogin.querySelector('.btn-text').textContent = loading ? 'Verificando...' : 'Entrar';
  btnSpinner.style.display = loading ? 'inline' : 'none';
}

// ── Submit del formulario ──────────────────────────────
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  loginError.style.display = 'none';

  if (!validateFields()) return;

  setLoading(true);

  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: usernameInput.value.trim(),
        password: passwordInput.value.trim()
      })
    });

    const data = await response.json();

    if (data.ok) {
      // Guardar sesión en sessionStorage
      sessionStorage.setItem('usuario', JSON.stringify({
        nombre: data.nombre,
        rol: data.rol
      }));
      // Redirigir al dashboard
      window.location.href = 'index.html';
    } else {
      loginError.textContent = data.mensaje || 'Credenciales incorrectas';
      loginError.style.display = 'block';
      passwordInput.value = '';
      passwordInput.focus();
    }

  } catch (err) {
    loginError.textContent = '⚠️ No se pudo conectar con el servidor. ¿Está el backend activo?';
    loginError.style.display = 'block';
  } finally {
    setLoading(false);
  }
});

// ── Limpiar errores al escribir ────────────────────────
usernameInput.addEventListener('input', () => {
  usernameError.textContent = '';
  usernameInput.classList.remove('input-error');
  loginError.style.display = 'none';
});

passwordInput.addEventListener('input', () => {
  passwordError.textContent = '';
  passwordInput.classList.remove('input-error');
  loginError.style.display = 'none';
});
