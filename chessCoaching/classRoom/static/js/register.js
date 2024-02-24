var password = document.getElementById('password');
var repeatPassword = document.getElementById('repeatPassword');
var passwordMismatch = document.getElementById('passwordMismatch');
var passwordMatch = document.getElementById('passwordMatch');

password.addEventListener('input', validatePasswords);
repeatPassword.addEventListener('input', validatePasswords);

function validatePasswords() {
    if (password.value !== repeatPassword.value) {
        passwordMismatch.style.display = 'inline';
        passwordMatch.style.display = 'none';
    } else {
        passwordMismatch.style.display = 'none';
        passwordMatch.style.display = 'inline';
    }
}

function togglePasswordVisibility() {
    var passwordField = document.getElementById("password");
    var repeatPasswordField = document.getElementById("repeatPassword");
    var passwordIcon = document.getElementById("showPasswordIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        repeatPasswordField.type = "text";
        passwordIcon.classList.remove("fa-eye");
        passwordIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        repeatPasswordField.type = "password";
        passwordIcon.classList.remove("fa-eye-slash");
        passwordIcon.classList.add("fa-eye");
    }
}

document.getElementById("togglePassword").addEventListener("click", togglePasswordVisibility);