const API = localStorage.getItem('api_url') || 'http://localhost:8000/api';

function token() {
  return localStorage.getItem('token');
}

function rol() {
  return (localStorage.getItem('rol') || '').toLowerCase();
}

function headers() {
  return {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token()
  };
}

async function api(path, options = {}) {
  const res = await fetch(API + path, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(token() ? headers() : { 'Content-Type': 'application/json' })
    }
  });

  if (!res.ok) {
    const e = await res.json().catch(() => ({ detail: 'Error' }));
    throw new Error(
      typeof e.detail === 'object'
        ? JSON.stringify(e.detail)
        : (e.detail || 'Error')
    );
  }

  return res.json();
}

function logout() {
  localStorage.clear();
  location.href = 'index.html';
}

function mustLogin() {
  if (!token()) {
    location.href = 'index.html';
  }
}

function mustRole(requiredRole) {
  mustLogin();

  if (rol() !== requiredRole.toLowerCase()) {
    alert('No tienes permiso para ingresar a esta sección. Rol actual: ' + rol());
    location.href = 'dashboard.html';
  }
}

function mustAnyRole(allowedRoles) {
  mustLogin();

  const allowed = allowedRoles.map(r => r.toLowerCase());

  if (!allowed.includes(rol())) {
    alert('No tienes permiso para ingresar a esta sección. Rol actual: ' + rol());
    location.href = 'dashboard.html';
  }
}