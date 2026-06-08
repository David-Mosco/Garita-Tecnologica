mustLogin();

const nombre = localStorage.getItem('nombre') || 'Usuario';
const currentRole = localStorage.getItem('rol') || '';

document.getElementById('welcome').textContent =
    `Bienvenido, ${nombre} | Rol: ${currentRole.toUpperCase()}`;

const menuAdmin = document.getElementById('menuAdmin');
const menuVisita = document.getElementById('menuVisita');
const menuPrerregistro = document.getElementById('menuPrerregistro');
const menuHistorial = document.getElementById('menuHistorial');
const menuPlacas = document.getElementById('menuPlacas');

if (currentRole === 'admin') {
    if (menuAdmin) menuAdmin.style.display = 'block';
    if (menuVisita) menuVisita.style.display = 'none';
    if (menuPrerregistro) menuPrerregistro.style.display = 'none';
    if (menuHistorial) menuHistorial.style.display = 'none';
    if (menuPlacas) menuPlacas.style.display = 'none';
}

if (currentRole === 'agente') {
    if (menuAdmin) menuAdmin.style.display = 'none';
    if (menuVisita) menuVisita.style.display = 'block';
    if (menuPrerregistro) menuPrerregistro.style.display = 'none';
    if (menuHistorial) menuHistorial.style.display = 'block';
    if (menuPlacas) menuPlacas.style.display = 'block';
}

if (currentRole === 'vecino') {
    if (menuAdmin) menuAdmin.style.display = 'none';
    if (menuVisita) menuVisita.style.display = 'none';
    if (menuPrerregistro) menuPrerregistro.style.display = 'block';
    if (menuHistorial) menuHistorial.style.display = 'none';
    if (menuPlacas) menuPlacas.style.display = 'none';
}

(async () => {
    try {
        const d = await api('/visitas/dashboard');

        cards.innerHTML = `
      <div class="card">Visitas hoy<strong>${d.visitas_hoy}</strong></div>
      <div class="card">Dentro<strong>${d.visitas_dentro}</strong></div>
      <div class="card">Finalizadas<strong>${d.visitas_finalizadas}</strong></div>
      <div class="card">QR activos<strong>${d.prerregistros_activos}</strong></div>
      <div class="card">Normales<strong>${d.visitas_normales}</strong></div>
      <div class="card">Con QR<strong>${d.visitas_qr}</strong></div>
    `;
    } catch (e) {
        cards.innerHTML = '<div class="panel">Dashboard disponible para administrador o agente.</div>';
    }
})();