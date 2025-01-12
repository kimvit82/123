import requests

url = 'http://77.246.247.140/employees/'

def get_all():
    x = requests.get(url)

    all_employees = x.json()
    print("ВОТ СПИСОК ВСЕХ СОТРУДНИКОВ: ---->")
    if all_employees:
        for i in all_employees:
            print(i['first_name'], i['position'])
    else:
        print("В базе данных отсутствует записи сотрудников")
    print()

def get_by_id():
    id = input("Введите id сотрудника про которого хотите узнать: ")
    x = requests.get(f'{url}{id}/')

    employees = x.json()
    if employees:
        print(employees['first_name'], employees['position'])
    else:
        print("В базе данных отсутствует сотрудник с таким id")


def add_employee():
    first_name = input("Введите имя нового сотрудника: ")
    last_name = input("Введите фамилию нового сотрудника")
    email = input("Введите почту нового сотрудника: ")
    position = input("Введите позицию нового сотрудника: ")
    hire_date = input("Введите дату найма: ")
    salary = input("Введите зарплату нового сотрудника: ")
    is_active = True

    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'position': position,
        'hire_date': hire_date,
        'salary': salary,
        'is_active': is_active
    }

    otvet = requests.post(url, json=data)

    otvet = otvet.json()
    print(otvet)

def delete_by_id():
    id = input("Введите id сотрудника про которого хотите уволить: ")
    x = requests.delete(f'{url}{id}/')
    print(x)
    print(f"Сотрудник с {id} был удалён из базы данных")

def update_employee_patch():
    try:
        id = int(input("Введите id сотрудника, которого хотите обновить: "))
        fields_to_update = {}
        change_salary = input("Хотите обновить зарплату? (y/n): ").lower()
        if change_salary == 'y':
            fields_to_update['salary'] = input("Введите новую зарплату: ")
        response = requests.patch(f'{url}{id}/', json=fields_to_update)
        if response.status_code == 200:
            print("Данные сотрудника успешно обновлены:", response.json())
        else:
            print("Ошибка обновления данных.")
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса.")


def delete_all_employees():
        master_password = "password123"
        user_input = input("Введите пароль для удаления всех сотрудников: ")
        if user_input != master_password:
            print("Неверный ключевой пароль. Удаление отменено.")
            return
        response = requests.delete(url)
        if response.status_code == 200:
            print("Все сотрудники успешно удалены.")
        else:
            print("Ошибка при удалении")

a = -10000

while a != 5:
    if a == 1:
        get_all()
    elif a == 2:
        get_by_id()
    elif a == 3:
        add_employee()
    elif a == 4:
        delete_by_id()
    elif a == 6:
        update_employee_patch()
    elif a == 7:
        delete_all_employees()
    print("Если хотите посмотреть список всех сотрудников введите 1.")
    print("Если хотите посмотреть сотрудника по id, то введите 2.")
    print("Если хотите добавить нового сотрудника, введите 3.")
    print("Если хотите удалить сотрудника по id, введите 4.")
    print("Если хотите выйти из этого меню, введите 5.")
    print("Если хотите частично обновить данные сотрудника, введите 6.")
    print("Если хотите удалить всех сотрудников, введите 7.")

    a = int(input(": "))