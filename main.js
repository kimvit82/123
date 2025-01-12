function submit() {
    let name = prompt("Введите ваше имя:");
    let age = prompt("Введите ваш возраст:");
    if (age >= 18) {
        alert(2024 - age);
    } else {
        alert("ДОСТУП ЗАПРЕЩЕН");
    }
}