mustAnyRole(['admin', 'agente']);

normalForm.addEventListener('submit', async e => {
    e.preventDefault();
    result.textContent = 'Procesando...';

    try {
        const data = {
            visitante: {
                nombre: nombre.value.trim(),
                dpi_licencia: dpi.value.trim(),
                telefono: telefono.value.trim()
            },
            vehiculo: {
                placa: placa.value.trim(),
                marca: marca.value.trim(),
                color: color.value.trim()
            },
            codigo_vecino: codigo.value.trim(),
            motivo: motivo.value.trim()
        };

        const r = await api('/visitas/normal', {
            method: 'POST',
            body: JSON.stringify(data)
        });

        result.textContent = JSON.stringify(r, null, 2);
        normalForm.reset();

    } catch (err) {
        result.textContent = err.message;
    }
});

qrForm.addEventListener('submit', async e => {
    e.preventDefault();
    result.textContent = 'Procesando QR...';

    try {
        const tokenLimpio = token.value.trim();

        const r = await api('/visitas/qr', {
            method: 'POST',
            body: JSON.stringify({
                token_qr: tokenLimpio
            })
        });

        result.textContent = JSON.stringify(r, null, 2);
        qrForm.reset();

    } catch (err) {
        result.textContent = err.message;
    }
});