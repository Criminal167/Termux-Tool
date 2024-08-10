import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import os
import requests
from faker import Faker
import random
from datetime import datetime

fake = Faker('ru_RU')

def очистить_экран():
    os.system('clear')

def информация_о_телефоне(phone):
    try:
        parsed_phone = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(parsed_phone):
            print("\n[!] Ошибка -> Недействительный номер телефона\n")
            return
        
        country = geocoder.description_for_number(parsed_phone, "en")
        region = geocoder.description_for_number(parsed_phone, "ru")
        carrier_info = carrier.name_for_number(parsed_phone, "en")
        formatted_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        is_valid = phonenumbers.is_valid_number(parsed_phone)
        is_possible = phonenumbers.is_possible_number(parsed_phone)
        timezones = timezone.time_zones_for_number(parsed_phone)
        
        print(f"\n[+] Номер телефона -> {formatted_number}\n")
        print(f"[+] Страна -> {country}\n")
        print(f"[+] Регион -> {region}\n")
        print(f"[+] Оператор -> {carrier_info}\n")
        print(f"[+] Активен -> {is_possible}\n")
        print(f"[+] Валид -> {is_valid}\n")
        print(f"[+] Таймзона -> {', '.join(timezones)}\n")
    
    except phonenumbers.NumberParseException as e:
        print(f"\n[!] Ошибка -> Неверный формат номера: {e}\n")
    except Exception as e:
        print(f"\n[!] Произошла ошибка: {e}\n")

def информация_о_ip(ip_address):
    def заголовок(текст):
        print(f"\n[+] {текст}\n")

    def показать_данные(ключ, значение):
        if значение is None:
            значение = "N/A"
        print(f"{ключ:25} | {значение}")

    def получить_инфо(ip):
        сайты = [
            {"url": f"https://ip-api.io/json/{ip}", "name": "IP-API.io"},
            {"url": f"https://geolocation-db.com/json/{ip}", "name": "Geolocation-DB"},
            {"url": f"https://www.iplocate.io/api/lookup/{ip}", "name": "IPLocate.io"},
            {"url": f"https://ipwhois.app/json/{ip}", "name": "IPWhois.app"},
            {"url": f"https://freegeoip.app/json/{ip}", "name": "Freegeoip.app"},
            {"url": f"http://ip-api.com/json/{ip}", "name": "IP-API.com"},
        ]

        for сайт in сайты:
            заголовок(f"Данные с сайта: {сайт['name']}")
            try:
                ответ = requests.get(сайт['url'])
                ответ.raise_for_status()
                данные = ответ.json()

                if 'error' in данные:
                    print(f"Ошибка от {сайт['name']}: {данные['error']}")
                    continue

                for ключ, значение in данные.items():
                    показать_данные(ключ, значение)

                print("-"*40)

            except requests.exceptions.RequestException as e:
                print(f"Не удалось получить информацию от {сайт['name']}: {e}")
            print()

    def имя_хоста(ip):
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except socket.herror:
            return None

    def валидный_ip(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    if валидный_ip(ip_address):
        заголовок(f"Информация по IP-адресу: {ip_address}")
        hostname = имя_хоста(ip_address)
        if hostname:
            показать_данные("Имя хоста", hostname)
        else:
            print("Имя хоста: N/A")
        
        print()
        получить_инфо(ip_address)
    else:
        print("\n[!] Неверный формат IP-адреса\n")

def сгенерировать_инн():
    numbers = [random.randint(0, 9) for _ in range(10)]
    def контрольная_цифра(numbers, коэффициенты):
        return str((sum(x * y for x, y in zip(numbers, коэффициенты)) % 11) % 10)
    цифры = ''.join(map(str, numbers))
    return цифры + контрольная_цифра(numbers, [2, 4, 10, 3, 5, 9, 4, 6, 8]) + контрольная_цифра(numbers, [7, 2, 4, 10, 3, 5, 9, 4, 6, 8])

def сгенерировать_личность():
    пол = input("\n[?] Кого вы хотите сгенерировать (М/Д) -> ").strip().upper()
    
    if пол == 'М':
        имя = fake.name_male()
    elif пол == 'Д':
        имя = fake.name_female()
    else:
        print("\n[!] Неверный выбор пола\n")
        return
    
    адрес = fake.address()
    страна = fake.country()
    инн = сгенерировать_инн()
    снилс = fake.unique.random_number(digits=11, fix_len=True)
    паспорт = fake.unique.random_number(digits=10, fix_len=True)
    дата_рождения = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d.%m.%Y')
    
    print("\n  Сгенерированная личность  \n")
    print(f"ФИО: {имя}")
    print(f"Адрес: {адрес}")
    print(f"Страна: {страна}")
    print(f"ИНН: {инн}")
    print(f"СНИЛС: {снилс}")
    print(f"Паспорт: {паспорт}")
    print(f"Дата рождения: {дата_рождения}")

def сгенерировать_карту():
    номер_карты = fake.credit_card_number()
    срок_действия = fake.credit_card_expire()
    cvv = fake.credit_card_security_code()
    провайдер = fake.credit_card_provider()

    print("\n  Сгенерированная карта  \n")
    print(f"Номер карты: {номер_карты}")
    print(f"Срок действия: {срок_действия}")
    print(f"CVV: {cvv}")
    print(f"Провайдер: {провайдер}")

def пробить_карту(bin_number):
    url = f"https://lookup.binlist.net/{bin_number}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        print("\n  Информация о карте  \n")
        print(f"Банк: {data['bank']['name']}")
        print(f"Страна: {data['country']['name']}")
        print(f"Тип: {data['type']}")
        print(f"Бренд: {data['brand']}")
    else:
        print("\n[!] Не удалось получить информацию о карте\n")

def меню():
    while True:
        очистить_экран()
        print("\n             Меню   \n")
        print(" (1). Информация о номере телефона")
        print(" (2). Информация о IP-геолокации")
        print(" (3). Генерация личности")
        print(" (4). Генерация карты")
        print(" (5). Пробив карты по BIN")
        print(" (0). Выход\n")
        выбор = input("Введите номер пункта - ")
        if выбор == '1':
            телефон = input("\nВведите номер телефона - ")
            информация_о_телефоне(телефон)
            input("\nДля продолжения нажмите Enter")
        elif выбор == '2':
            ip = input("\nВведите IP-адрес - ")
            информация_о_ip(ip)
            input("\nДля продолжения нажмите Enter")
        elif выбор == '3':
            сгенерировать_личность()
            input("\nДля продолжения нажмите Enter")
        elif выбор == '4':
            сгенерировать_карту()
            input("\nДля продолжения нажмите Enter")
        elif выбор == '5':
            bin_number = input("\nВведите BIN номер карты - ")
            пробить_карту(bin_number)
            input("\nДля продолжения нажмите Enter")
        elif выбор == '0':
            print("\nСпасибо за использование программы\n")
            break
        else:
            print("\nНеверный выбор, попробуйте снова\n")

if __name__ == '__main__':
    меню()
