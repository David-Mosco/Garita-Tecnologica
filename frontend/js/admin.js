mustRole('ADMIN');

let viviendasData = [];
let vecinosData = [];

async function cargarViviendas() {
    try {
        viviendasData = await api('/admin/viviendas');
        pintarViviendas();
        llenarSelectViviendas();
    } catch (err) {
        result.textContent = err.message;
    }
}

function pintarViviendas() {
    const filtro = (filtroVivienda.value || '').toLowerCase();
    const orden = ordenVivienda.value;

    let lista = viviendasData.filter(v =>
        `${v.id} ${v.direccion} ${v.sector || ''} ${v.numero_casa || ''}`
            .toLowerCase()
            .includes(filtro)
    );

    lista.sort((a, b) => {
        if (orden === 'numero') return (a.numero_casa || '').localeCompare(b.numero_casa || '', undefined, { numeric: true });
        if (orden === 'direccion') return a.direccion.localeCompare(b.direccion);
        return (a.sector || '').localeCompare(b.sector || '') || (a.numero_casa || '').localeCompare(b.numero_casa || '', undefined, { numeric: true });
    });

    viviendas.innerHTML = lista.map(v => `
    <div class="panel">
      <b>ID ${v.id}</b> | ${v.direccion}<br>
      Sector: ${v.sector || 'Sin sector'} | Casa: ${v.numero_casa || 'Sin número'}<br>
      Estado: ${v.activa ? 'Activa' : 'Inactiva'}<br>
      <button onclick="eliminarVivienda(${v.id})">Desactivar vivienda</button>
    </div>
  `).join('');
}

function llenarSelectViviendas() {
    vn_vivienda.innerHTML = '<option value="">Seleccione una vivienda</option>';

    viviendasData
        .filter(v => v.activa)
        .sort((a, b) => (a.sector || '').localeCompare(b.sector || '') || (a.numero_casa || '').localeCompare(b.numero_casa || '', undefined, { numeric: true }))
        .forEach(v => {
            vn_vivienda.innerHTML += `
        <option value="${v.id}">
          ${v.sector || 'Sin sector'} - Casa ${v.numero_casa || 'S/N'} | ${v.direccion}
        </option>
      `;
        });
}

vivForm.addEventListener('submit', async e => {
    e.preventDefault();

    try {
        const r = await api('/admin/viviendas', {
            method: 'POST',
            body: JSON.stringify({
                direccion: direccion.value,
                sector: sector.value,
                numero_casa: numero.value
            })
        });

        result.textContent = JSON.stringify(r, null, 2);
        vivForm.reset();
        await cargarViviendas();

    } catch (err) {
        result.textContent = err.message;
    }
});

vecForm.addEventListener('submit', async e => {
    e.preventDefault();

    try {
        const r = await api('/admin/vecinos', {
            method: 'POST',
            body: JSON.stringify({
                nombre: vn_nombre.value,
                email: vn_email.value,
                telefono: vn_tel.value,
                vivienda_id: parseInt(vn_vivienda.value)
            })
        });

        result.textContent = JSON.stringify(r, null, 2);
        vecForm.reset();
        await cargarVecinos();

    } catch (err) {
        result.textContent = err.message;
    }
});

async function cargarVecinos() {
    try {
        vecinosData = await api('/admin/vecinos');
        pintarVecinos();
    } catch (e) {
        vecinos.textContent = e.message;
    }
}

function pintarVecinos() {
    const filtro = (filtroVecino.value || '').toLowerCase();

    const lista = vecinosData.filter(v =>
        `${v.nombre} ${v.email} ${v.codigo_unico} ${v.vivienda?.direccion || ''}`
            .toLowerCase()
            .includes(filtro)
    );

    vecinos.innerHTML = lista.map(v => `
    <div class="panel">
      <b>${v.nombre}</b> | ${v.email}<br>
      Código único del vecino: <b>${v.codigo_unico}</b><br>
      Vivienda: ${v.vivienda.direccion}<br>
      Estado: ${v.activo ? 'Activo' : 'Inactivo'}<br>
      <button onclick="eliminarVecino(${v.id})">Desactivar vecino</button>
    </div>
  `).join('');
}

async function eliminarVivienda(id) {
    if (!confirm('¿Seguro que deseas desactivar esta vivienda?')) return;

    try {
        await api(`/admin/viviendas/${id}`, { method: 'DELETE' });
        await cargarViviendas();
        result.textContent = 'Vivienda desactivada correctamente.';
    } catch (err) {
        result.textContent = err.message;
    }
}

async function eliminarVecino(id) {
    if (!confirm('¿Seguro que deseas desactivar este vecino?')) return;

    try {
        await api(`/admin/vecinos/${id}`, { method: 'DELETE' });
        await cargarVecinos();
        result.textContent = 'Vecino desactivado correctamente.';
    } catch (err) {
        result.textContent = err.message;
    }
}

filtroVivienda.addEventListener('input', pintarViviendas);
ordenVivienda.addEventListener('change', pintarViviendas);
filtroVecino.addEventListener('input', pintarVecinos);

cargarViviendas();
cargarVecinos();