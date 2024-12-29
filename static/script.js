// Прокрутка до секцій при натисканні на навігаційні посилання
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    const targetId = this.getAttribute('href').substring(1);
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Обробка форми контактів
document.querySelector('form').addEventListener('submit', function (e) {
  e.preventDefault();
  alert('Дякуємо за ваше повідомлення! Ми зв’яжемося з вами найближчим часом.');
});

// Обробка форми реєстрації
document.getElementById('signupForm')?.addEventListener('submit', function (e) {
  e.preventDefault(); // Запобігти стандартній поведінці

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  if (password !== confirmPassword) {
    alert('Паролі не збігаються!');
    return;
  }

  // Відправлення даних на сервер
  fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: name,
      email: email,
      password: password,
    }),
  })
    .then(response => {
      if (response.ok) {
        alert('Реєстрація успішна!');
        window.location.href = '/'; // Перехід на головну сторінку
      } else {
        alert('Помилка під час реєстрації.');
      }
    })
    .catch(error => console.error('Error:', error));
});

// Обробка форми авторизації
document.getElementById('loginForm')?.addEventListener('submit', function (e) {
  e.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  // Відправлення даних на сервер
  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  })
    .then(response => {
      if (response.ok) {
        alert('Авторизація успішна!');
        window.location.href = '/dashboard'; // Перехід до особистого кабінету
      } else {
        alert('Помилка авторизації.');
      }
    })
    .catch(error => console.error('Error:', error));
});