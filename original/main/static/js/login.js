// Переключение между формами
function showForm(type) {
    if (type === 'login') {
        document.getElementById('loginForm').style.display = 'block';
        document.getElementById('registerForm').style.display = 'none';
    } else {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('registerForm').style.display = 'block';
    }
}

// Ждем загрузки страницы
document.addEventListener('DOMContentLoaded', function() {

    // Маска для телефона
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let numbers = e.target.value.replace(/\D/g, '');
            if (numbers.length > 0) {
                let result = '+7';
                if (numbers.length > 1) {
                    result += ' (' + numbers.substring(1, 4);
                }
                if (numbers.length >= 4) {
                    result += ') ' + numbers.substring(4, 7);
                }
                if (numbers.length >= 7) {
                    result += '-' + numbers.substring(7, 9);
                }
                if (numbers.length >= 9) {
                    result += '-' + numbers.substring(9, 11);
                }
                e.target.value = result;
            }
        });
    }

    // Валидация при отправке
    const form = document.getElementById('regForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            let errors = false;

            // Имя
            const firstName = document.getElementById('firstName');
            const nameRegex = /^[А-Я][а-я]+$/;
            if (!nameRegex.test(firstName.value)) {
                document.getElementById('firstNameError').innerText = 'Только русские буквы, первая заглавная';
                errors = true;
            } else {
                document.getElementById('firstNameError').innerText = '';
            }

            // Фамилия
            const lastName = document.getElementById('lastName');
            if (!nameRegex.test(lastName.value)) {
                document.getElementById('lastNameError').innerText = 'Только русские буквы, первая заглавная';
                errors = true;
            } else {
                document.getElementById('lastNameError').innerText = '';
            }

            // Email
            const email = document.getElementById('email');
            if (!email.value.includes('@') || !email.value.includes('.')) {
                document.getElementById('emailError').innerText = 'Неверный email';
                errors = true;
            } else {
                document.getElementById('emailError').innerText = '';
            }

            // Телефон
            const phone = document.getElementById('phone');
            const phoneRegex = /^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/;
            if (!phoneRegex.test(phone.value)) {
                document.getElementById('phoneError').innerText = 'Формат: +7 (999) 999-99-99';
                errors = true;
            } else {
                document.getElementById('phoneError').innerText = '';
            }

            // Пароль
            const password = document.getElementById('password');
            if (password.value.length < 8) {
                document.getElementById('passwordError').innerText = 'Минимум 8 символов';
                errors = true;
            } else {
                document.getElementById('passwordError').innerText = '';
            }

            // Подтверждение пароля
            const password2 = document.getElementById('password2');
            if (password.value !== password2.value) {
                document.getElementById('password2Error').innerText = 'Пароли не совпадают';
                errors = true;
            } else {
                document.getElementById('password2Error').innerText = '';
            }

            if (errors) {
                e.preventDefault();
                alert('Есть ошибки в форме!');
            }
        });
    }
});