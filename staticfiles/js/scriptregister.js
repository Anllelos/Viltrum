document.getElementById('id_password1').addEventListener('input', function() {
    const password = this.value;
    const length = document.getElementById('length');
    const number = document.getElementById('number');
    const uppercase = document.getElementById('uppercase');
    const lowercase = document.getElementById('lowercase');
    const special = document.getElementById('special');

    length.className = password.length >= 8 ? 'valid' : 'invalid';
    number.className = /\d/.test(password) ? 'valid' : 'invalid';
    uppercase.className = /[A-Z]/.test(password) ? 'valid' : 'invalid';
    lowercase.className = /[a-z]/.test(password) ? 'valid' : 'invalid';
    special.className = /[^A-Za-z0-9]/.test(password) ? 'valid' : 'invalid';
});
