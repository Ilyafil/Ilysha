class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Client:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

class Order:
    def __init__(self, display_name, service_name, car_brand, car_model):
        self.display_name = display_name  # Имя для отображения
        self.service_name = service_name
        self.car_brand = car_brand
        self.car_model = car_model
        self.status = 'В ожидании'

class Service:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

class WorkshopApp:
    def __init__(self):
        # Предустановленные пользователи
        self.users = [
            User("админ", "52", "admin"),
            User("пользователь", "", "guest")
        ]

        # Предустановленные услуги
        self.services = [
            Service("Замена масла", 6000.00, "Замена моторного и трансмиссионного ."),
            Service("Замена тормозных колодок", 8000.00, "Замена тормозных колодок."),
            Service("Перебор поршневой двигателя", 100000.00, "Удаление пыли и грязи с двигателя."),
            Service("Замена шаровых подшипников", 5000.00, "Замена и установка(также вход в работу демонтаж)."),
            Service("Настройка подвески", 8000.00, "Сход/развал колес и настройка клиренса."),
            Service("Замена аккумулятора", 1200.00, "Замена аккумулятора."),
            Service("Ремонт радиатора", 20300.00, "В стоимость вхлдит очистка и восстановление искаженных ячеек"),
            Service("Восстановление лакокрасочного покрытия", 25000.00, "Восстановление лакокрасочного покрытия."),
            Service("Настройка системы охлаждения", 3000.00, "Настройка системы охлаждения."),
            Service("Прошивка ЭБУ", 18000.00, "Установка мозгов BOSH.")
        ]

        self.clients = []
        self.orders = []
        self.current_user = None

    def require_admin(self):
        if not self.is_admin():
            print("У вас нет прав для выполнения этой операции.")
            return False
        return True

    def get_float_input(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите число.")

    def get_int_input(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите целое число.")

    def login(self):
        while True:
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")

            for user in self.users:
                if user.username == username and user.password == password:
                    self.current_user = user
                    print(f"Добро пожаловать, {username}!")
                    return
            print("Неверное имя пользователя или пароль.")

    def add_service(self):
        if not self.require_admin():
            return

        name = input("Введите название услуги: ")
        price = self.get_float_input("Введите цену услуги: ")
        description = input("Введите описание услуги: ")

        self.services.append(Service(name, price, description))
        print("Услуга добавлена.")

    def delete_service(self):
        if not self.require_admin():
            return

        service_name = input("Введите название услуги для удаления: ")

        for service in self.services:
            if service.name == service_name:
                self.services.remove(service)
                print(f"Услуга '{service_name}' удалена.")
                return

        print(f"Услуга '{service_name}' не найдена.")

    def update_service(self):
        if not self.require_admin():
            return

        service_name = input("Введите название услуги для обновления: ")

        for service in self.services:
            if service.name == service_name:
                new_price = self.get_float_input("Введите новую цену услуги: ")
                new_description = input("Введите новое описание услуги: ")

                service.price = new_price
                service.description = new_description
                print(f"Услуга '{service_name}' обновлена.")
                return

        print(f"Услуга '{service_name}' не найдена.")

    def view_services(self):
        if not self.services:
            print("Нет доступных услуг.")
            return

        print("\nДоступные услуги:")
        for service in self.services:
            print(f"{service.name} - Цена: {service.price:.2f} руб., Описание: {service.description}")

    def search_service(self):
        search_term = input("Введите название услуги для поиска: ")

        found_services = list(filter(lambda s: search_term.lower() in s.name.lower(), self.services))

        if not found_services:
            print(f"Услуги с названием '{search_term}' не найдены.")
            return

        print("\nНайденные услуги:")
        for service in found_services:
            print(f"{service.name} - Цена: {service.price:.2f} руб., Описание: {service.description}")

    def sort_services(self):
        sort_by = input("Сортировать по (name/price): ").strip().lower()

        if sort_by == 'name':
            sorted_services = sorted(self.services, key=lambda s: s.name)
            print("\nУслуги отсортированы по названию:")
            for service in sorted_services:
                print(f"{service.name} - Цена: {service.price:.2f} руб., Описание: {service.description}")

        elif sort_by == 'price':
            order_choice = input("Сортировать по (1 - возрастанию / 2 - убыванию): ").strip()

            if order_choice == '1':
                sorted_services = sorted(self.services, key=lambda s: s.price)
                print("\nУслуги отсортированы по цене (возрастание):")
                for service in sorted_services:
                    print(f"{service.name} - Цена: {service.price:.2f} руб., Описание: {service.description}")

            elif order_choice == '2':
                sorted_services = sorted(self.services, key=lambda s: s.price, reverse=True)
                print("\nУслуги отсортированы по цене (убывание):")
                for service in sorted_services:
                    print(f"{service.name} - Цена: {service.price:.2f} руб., Описание: {service.description}")

            else:
                print("Неверный выбор.")

        else:
            print("Неверный критерий сортировки.")

    def filter_services_by_budget(self):
        min_price_input = input('Введите минимальную цену (или оставьте пустым для отсутствия ограничения): ').strip()
        max_price_input = input('Введите максимальную цену (или оставьте пустым для отсутствия ограничения): ').strip()

        filtered_services = self.services

        if min_price_input:
            try:
                min_price_limit = float(min_price_input)
                filtered_services = [s for s in filtered_services if s.price >= min_price_limit]
            except ValueError:
                print('Некорректный ввод минимальной цены.')
                return

        if max_price_input:
            try:
                max_price_limit = float(max_price_input)
                filtered_services = [s for s in filtered_services if s.price <= max_price_limit]
            except ValueError:
                print('Некорректный ввод максимальной цены.')
                return

        if filtered_services:
            print("\nДоступные услуги в рамках вашего бюджета:")
            for service in filtered_services:
                print(f"{service.name} - Цена: {service.price:.2f} руб., Описание: {service.description}")
        else:
            print('Нет доступных услуг в рамках вашего бюджета.')

    def order_service(self):
        if not self.current_user:
            print("Сначала нужно войти в систему.")
            return

        display_name = input("Как вас называть при оформлении заказа? ")  # Запрашиваем имя для отображения
        service_name = input("Введите название услуги для заказа: ")

        if not any(service.name == service_name for service in self.services):
            print(f"Услуга '{service_name}' не найдена.")
            return

        car_brand = input("Введите марку вашей машины: ")
        car_model = input("Введите модель вашей машины: ")

        order = Order(display_name, service_name, car_brand, car_model)  # Используем введенное имя для отображения в заказе
        self.orders.append(order)

        print(f"Заказ на услугу '{service_name}' для {car_brand} {car_model} успешно оформлен.")

    def view_orders(self):
        if not self.orders:
            print("Нет заказов.")
            return

        print("\nИстория заказов:")
        for order in self.orders:
            print(f"Имя клиента: {order.display_name}, Услуга: {order.service_name}, Марка: {order.car_brand}, Модель: {order.car_model}, Статус: {order.status}")

    def view_all_orders(self):
        if not self.orders:
            print("Нет заказов.")
            return

        print("\nВсе заказы:")
        for order in self.orders:
            print(f"Имя клиента: {order.display_name}, Услуга: {order.service_name}, Марка: {order.car_brand}, Модель: {order.car_model}, Статус: {order.status}")

    def delete_order(self):
        if not self.require_admin():
            return

        if not self.orders:
            print("Нет заказов для удаления.")
            return

        print("\nВсе заказы:")
        for index, order in enumerate(self.orders, start=1):
            print(f"{index}. Имя клиента: {order.display_name}, Услуга: {order.service_name}, Марка: {order.car_brand}, Модель: {order.car_model}, Статус: {order.status}")

        order_number = self.get_int_input("Введите номер заказа для удаления: ")

        if 1 <= order_number <= len(self.orders):
            del self.orders[order_number - 1]
            print("Заказ удален.")
        else:
            print("Неверный номер заказа.")

    def update_account(self):
        if not self.current_user:
            print("Сначала нужно войти в систему.")
            return

        new_password = input("Введите новый пароль: ")

        for user in self.users:
            if user.username == self.current_user.username:
                user.password = new_password
                print("Пароль обновлен.")
                return

    def is_admin(self):
        return self.current_user and self.current_user.role == 'admin'

    def add_client(self):
        if not self.require_admin():
            return

        name = input("Введите имя клиента: ")
        phone = input("Введите телефон клиента: ")

        client = Client(name, phone)
        self.clients.append(client)
        print("Клиент добавлен.")

    def run(self):
        while True:
            choice = input("\n1. Вход\n2. Выход\nВыберите действие (введите номер): ")

            if choice == '1':
                self.login()

                # Проверяем, что пользователь успешно вошел
                if self.current_user:
                    while True:
                        if self.is_admin():
                            action_choice = input(
                                "\n1. Добавить услугу\n2. Удалить услугу\n3. Обновить услугу\n4. Просмотреть услуги\n5. Сортировать услуги\n6. Просмотреть все заказы\n7. Удалить заказ\n8. Выйти\nВыберите действие (введите номер): ")

                            if action_choice == '1':
                                self.add_service()
                            elif action_choice == '2':
                                self.delete_service()
                            elif action_choice == '3':
                                self.update_service()
                            elif action_choice == '4':
                                self.view_services()
                            elif action_choice == '5':
                                self.sort_services()
                            elif action_choice == '6':
                                self.view_all_orders()
                            elif action_choice == '7':
                                self.delete_order()
                            elif action_choice == '8':
                                print("Вы вышли из системы.")
                                break
                            else:
                                print("Неверный выбор.")
                        else:  # Гость
                            action_choice = input(
                                "\n1. Просмотреть услуги\n2. Заказать услугу\n3. Поиск услуги\n4. Сортировать услуги\n5. Фильтровать услуги по бюджету\n6. Посмотреть историю заказов\n7. Выйти\nВыберите действие (введите номер): ")

                            if action_choice == '1':
                                self.view_services()
                            elif action_choice == '2':
                                self.order_service()
                            elif action_choice == '3':
                                self.search_service()
                            elif action_choice == '4':
                                self.sort_services()
                            elif action_choice == '5':
                                self.filter_services_by_budget()
                            elif action_choice == '6':
                                self.view_orders()
                            elif action_choice == '7':
                                print("Вы вышли из системы.")
                                break
                            else:
                                print("Неверный выбор.")

            elif choice == '2':
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор.")

if __name__ == "__main__":
    app = WorkshopApp()
    app.run()
                    