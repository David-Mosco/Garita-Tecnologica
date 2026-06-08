document.getElementById('loginForm').addEventListener('submit', async e => {
    e.preventDefault();

    const msg = document.getElementById('msg');
    msg.textContent = '';

    try {
        const data = await api('/auth/login', {
            method: 'POST',
            body: JSON.stringify({
                email: email.value,
                password: password.value
            })
        });

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('nombre', data.nombre);
        localStorage.setItem('rol', data.rol);
        localStorage.setItem('email', data.email);

        location.href = 'dashboard.html';
    } catch (err) {
        msg.textContent = err.message;
    }
});