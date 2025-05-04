import random
import requests
from time import sleep
import os, signal, sys
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.text import Text
from rich.style import Style
from fatool import termuxtoolfa

__CHANNEL_USERNAME__ = "FAtermux"
__GROUP_USERNAME__   = ""

def signal_handler(sig, frame):
    print("\n Пока Пока...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Убедимся, что индекс в пределах
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name = figlet_format('FATOOL', font='drpepper')
    
    # Разделяем текст на две части: "FA" и "TOOL"
    lines = brand_name.splitlines()
    fa_part = [line[:10] for line in lines]  # Первые два символа каждой строки
    tool_part = [line[10:] for line in lines]  # Остальные символы каждой строки

    # Создаем текстовый объект для "FA" (розовый) и "TOOL" (красный)
    colorful_text = Text()
    for fa, tool in zip(fa_part, tool_part):
        colorful_text.append(fa, style=Style(color="rgb(231,18,219)"))  # Розовый цвет для "FA"
        colorful_text.append(tool, style=Style(color="rgb(255,99,71)"))  # Красный цвет для "TOOL"
        colorful_text.append("\n")  # Переход на новую строку

    console.print(colorful_text, end=None)
    console.print("[bold purple]FATOOL[/bold purple]")
    console.print(f"[bold magenta]Telegram[/bold magenta]: [bold purple]@{__CHANNEL_USERNAME__}[/bold purple].")
    console.print("[bold purple]==================================================[/bold purple]")
    console.print("[bold red]! Примечание[/bold red]: [bold purple]Вам нужно выйти из игры перед использованием !. [/bold purple]", end="\n\n")

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')

        console.print("[bold][purple]================[/purple][[bold purple] ДАННЫЕ ИГРОКА [bold purple]][purple]================[/purple][/bold]")

        name = data.get('Name', 'НЕ ОПРЕДЕЛЕНО')
        local_id = data.get('localID', 'НЕ ОПРЕДЕЛЕНО')
        money = data.get('money', 'НЕ ОПРЕДЕЛЕНО')


        console.print(f"[bold purple]Имя   [/bold purple]: {name}.")
        console.print(f"[bold purple]Айди[/bold purple]: {local_id}.")
        console.print(f"[bold purple]Деньги  [/bold purple]: {money}.")

    else:
        console.print("[bold red]! ОШИБКА[/bold red]: похоже, ваш вход не был выполнен правильно !.")
        return
    
def load_key_data(cpm):
    data = cpm.get_key_data()
    console.print("[bold][magenta]==================================================[/magenta][/bold]")
    console.print(f"[bold purple]Ключ доступа [/bold purple]: { data.get('access_key') }.")
    console.print(f"[bold purple]Telegram ID[/bold purple]: { data.get('telegram_id') }.")
    console.print(f"[bold purple]статус[/bold purple]: { (data.get('coins') if not data.get('is_unlimited') else 'Безлимитный') }.")



def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(f"{tag} не может быть пустым или состоять только из пробелов. Пожалуйста, попробуйте снова.")
        else:
            return value

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

def black_gradient_string(customer_name):
    modified_string = ""
    black_color = "000000"  # Черный цвет
    for char in customer_name:
        modified_string += f"[{black_color}]{char}"
    return modified_string

def purple_gradient_string(customer_name):
    modified_string = ""
    purple_color = "800080"  # Фиолетовый цвет
    for char in customer_name:
        modified_string += f"[{purple_color}]{char}"
    return modified_string

def green_gradient_string(customer_name):
    modified_string = ""
    green_color = "008000"  # Зеленый цвет
    for char in customer_name:
        modified_string += f"[{green_color}]{char}"
    return modified_string

def red_gradient_string(customer_name):
    modified_string = ""
    red_color = "FF0000"  # Красный цвет
    for char in customer_name:
        modified_string += f"[{red_color}]{char}"
    return modified_string

def blue_gradient_string(customer_name):
    modified_string = ""
    blue_color = "0000FF"  # Синий цвет
    for char in customer_name:
        modified_string += f"[{blue_color}]{char}"
    return modified_string

def yellow_gradient_string(customer_name):
    modified_string = ""
    yellow_color = "FFFF00"  # Желтый цвет
    for char in customer_name:
        modified_string += f"[{yellow_color}]{char}"
    return modified_string

def orange_gradient_string(customer_name):
    modified_string = ""
    orange_color = "FFA500"  # Оранжевый цвет
    for char in customer_name:
        modified_string += f"[{orange_color}]{char}"
    return modified_string

def cyan_gradient_string(customer_name):
    modified_string = ""
    cyan_color = "00FFFF"  # Циан
    for char in customer_name:
        modified_string += f"[{cyan_color}]{char}"
    return modified_string

def magenta_gradient_string(customer_name):
    modified_string = ""
    magenta_color = "FF00FF"  # Магента
    for char in customer_name:
        modified_string += f"[{magenta_color}]{char}"
    return modified_string

def brown_gradient_string(customer_name):
    modified_string = ""
    brown_color = "A52A2A"  # Коричневый цвет
    for char in customer_name:
        modified_string += f"[{brown_color}]{char}"
    return modified_string

def pink_gradient_string(customer_name):
    modified_string = ""
    pink_color = "FFC0CB"  # Розовый цвет
    for char in customer_name:
        modified_string += f"[{pink_color}]{char}"
    return modified_string

def light_blue_gradient_string(customer_name):
    modified_string = ""
    light_blue_color = "ADD8E6"  # Светло-синий цвет
    for char in customer_name:
        modified_string += f"[{light_blue_color}]{char}"
    return modified_string

def dark_green_gradient_string(customer_name):
    modified_string = ""
    dark_green_color = "006400"  # Темно-зеленый цвет
    for char in customer_name:
        modified_string += f"[{dark_green_color}]{char}"
    return modified_string

def light_green_gradient_string(customer_name):
    modified_string = ""
    light_green_color = "90EE90"  # Светло-зеленый цвет
    for char in customer_name:
        modified_string += f"[{light_green_color}]{char}"
    return modified_string

def dark_blue_gradient_string(customer_name):
    modified_string = ""
    dark_blue_color = "00008B"  # Темно-синий цвет
    for char in customer_name:
        modified_string += f"[{dark_blue_color}]{char}"
    return modified_string

def dark_red_gradient_string(customer_name):
    modified_string = ""
    dark_red_color = "8B0000"  # Темно-красный цвет
    for char in customer_name:
        modified_string += f"[{dark_red_color}]{char}"
    return modified_string

def gold_gradient_string(customer_name):
    modified_string = ""
    gold_color = "FFD700"  # Золотой цвет
    for char in customer_name:
        modified_string += f"[{gold_color}]{char}"
    return modified_string

def silver_gradient_string(customer_name):
    modified_string = ""
    silver_color = "C0C0C0"  # Серебряный цвет
    for char in customer_name:
        modified_string += f"[{silver_color}]{char}"
    return modified_string

def gray_gradient_string(customer_name):
    modified_string = ""
    gray_color = "808080"  # Серый цвет
    for char in customer_name:
        modified_string += f"[{gray_color}]{char}"
    return modified_string

def violet_gradient_string(customer_name):
    modified_string = ""
    violet_color = "EE82EE"  # Фиолетовый цвет
    for char in customer_name:
        modified_string += f"[{violet_color}]{char}"
    return modified_string

def teal_gradient_string(customer_name):
    modified_string = ""
    teal_color = "008080"  # Бирюзовый цвет
    for char in customer_name:
        modified_string += f"[{teal_color}]{char}"
    return modified_string

def coral_gradient_string(customer_name):
    modified_string = ""
    coral_color = "FF7F50"  # Кораловый цвет
    for char in customer_name:
        modified_string += f"[{coral_color}]{char}"
    return modified_string
    
    for char in customer_name:
        modified_string += f'[{black_color}]{char}'
    
    return modified_string

if __name__ == "__main__":

    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold purple][?] Email аккаунта[/bold purple]", "Email", password=False)
        acc_password = prompt_valid_value("[bold purple][?] Пароль аккаунта[/bold purple]", "Пароль", password=False)
        acc_access_key = prompt_valid_value("[bold purple][?] Ключ доступа[/bold purple]", "Ключ доступа", password=False)
        console.print("[bold purple][%] Попытка входа[/bold purple]: ", end=None)
        cpm = termuxtoolfa(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[bold red]АККАУНТ НЕ НАЙДЕН[/bold red].")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[bold red]НЕВЕРНЫЙ ПАРОЛЬ[/bold red].")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[bold red]НЕВЕРНЫЙ КЛЮЧ ДОСТУПА[/bold red].")
                sleep(2)
                continue
            else:
                console.print("[bold red]ПОПРОБУЙТЕ СНОВА[/bold red].")
                console.print("[bold yellow]! Примечание[/bold yellow]: убедитесь, что вы заполнили все поля !.")
                sleep(2)
                continue
        else:
            console.print("[bold green]УСПЕШНО[/bold green].")
            sleep(2)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)

            base_color = (128, 0, 128)
            functions = [
                "Увеличение денег",
                "Увеличение монет",
                "Ранг King",
                "Смена ID",
                "Смена ID(разноцветный)",
                "Смена имени",
                "Смена имени (Радуга)",
                "Удаление аккаунта",
                "Регистрация аккаунта",
                "Удаление друзей",
                "Разблокировка платных машин",
                "Разблокировка двигателя w16",
                "Разблокировка всех клаксонов",
                "Отключение повреждений двигателя",
                "Безлимитное топливо",
                "Разблокировка дома 3",
                "Разблокировка дыма",
                "Изменение побед в гонках",
                "Изменение поражений в гонках",
                "Разблокировка всех машин",
                "Разблокировка мигалок на все авто",
                "Клонирование аккаунта",
                "1695 хп на авто",
                "Сброс пробега на авто",
                "Убрать передний бампер на авто",
                "Убрать задний бампер на авто"
            ]

            for i, func in enumerate(functions):
                r = max(base_color[0] - i * 5, 50)
                b = max(base_color[2] - i * 5, 50)
                color = f"rgb({r},0,{b})"
                console.print(f"[bold][purple]({i+1:02}):[/purple] [{color}]{func}[/{color}]")

            console.print("[bold][purple](0) :[/purple] [red]Выход[/red]", end="\n\n")

            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                      "11", "12", "13", "14", "15", "16", "17", "18", "19", 
                      "20", "21", "22", "23", "24", "25","26"]  
            
            service = IntPrompt.ask(f"[bold][?] Выберите функцию [red][1-{choices[-1]} или 0][/red][/bold]", 
                                  choices=choices, show_choices=False)
            if service == 0: # Выход
                console.print(f"")
            elif service == 1: # Увеличение денег
                console.print("[bold purple][!] Введите, сколько денег вы хотите.[/bold purple]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold purple][%] Сохранение ваших данных[/bold purple]: ", end=None)
                if amount > 0 and amount <= 50000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="")
                        if answ == "y": console.print(f"")
                        else: continue
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 2: # Увеличение монет
                console.print("[bold purple][!] Введите, сколько монет вы хотите.[/bold purple]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold purple][%] Сохранение ваших данных[/bold purple]: ", end=None)
                if amount > 0 and amount <= 200000:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"")
                        else: continue
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 3: # Ранг King
                console.print("[bold red][!] Примечание:[/bold red]: если ранг King не появляется в игре, закройте и откройте игру несколько раз.")
                console.print("[bold red][!] Примечание:[/bold red]: пожалуйста, не делайте ранг King на одном аккаунте дважды.", end="\n\n")
                sleep(2)
                console.print("[bold purple][%] Присвоение вам ранга King[/bold purple]: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 4: # Смена ID
                console.print("[bold purple][!] Введите ваш новый ID.[/bold purple]")
                new_id = Prompt.ask("[bold][?] ID[/bold]")
                console.print("[bold purple][%] Сохранение ваших данных[/bold purple]: ", end=None)
                if len(new_id) >= 2 and len(new_id) <= 50 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"")
                        else: continue
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимый ID.[/bold yellow]")
                    sleep(2)
                    continue

            # Смена ID (выбор цвета)
            elif service == 5:  
                console.print("[bold purple][!] Выберите цвет для вашего нового ID.[/bold purple]")
                color_choice = Prompt.ask("[bold][?] Выберите цвет", choices=[
                    "черный", "фиолетовый", "зеленый", "красный", 
                    "синий", "желтый", "оранжевый", "циан", 
                    "магента", "коричневый", "розовый", 
                    "светло-синий", "темно-зеленый", "светло-зеленый", 
                    "темно-синий", "темно-красный", "золотой", 
                    "серебряный", "серый", "бирюзовый", 
                    "коралловый"], default="черный")
                
                console.print("[bold purple][!] Введите ваш новый ID.[/bold purple]")
                new_id = Prompt.ask("[bold][?] ID[/bold]")
                console.print("[bold purple][%] Сохранение ваших данных[/bold purple]: ", end=None)
                
                if len(new_id) >= 2 and len(new_id) <= 200 and (' ' not in new_id):
                    color_functions = {
                        "черный": black_gradient_string,
                        "фиолетовый": purple_gradient_string,
                        "зеленый": green_gradient_string,
                        "красный": red_gradient_string,
                        "синий": blue_gradient_string,
                        "желтый": yellow_gradient_string,
                        "оранжевый": orange_gradient_string,
                        "циан": cyan_gradient_string,
                        "магента": magenta_gradient_string,
                        "коричневый": brown_gradient_string,
                        "розовый": pink_gradient_string,
                        "светло-синий": light_blue_gradient_string,
                        "темно-зеленый": dark_green_gradient_string,
                        "светло-зеленый": light_green_gradient_string,
                        "темно-синий": dark_blue_gradient_string,
                        "темно-красный": dark_red_gradient_string,
                        "золотой": gold_gradient_string,
                        "серебряный": silver_gradient_string,
                        "серый": gray_gradient_string,
                        "бирюзовый": teal_gradient_string,
                        "коралловый": coral_gradient_string
                    }

                    # Установка ID в зависимости от выбранного цвета
                    if color_choice in color_functions:
                        if cpm.set_player_localid(color_functions[color_choice](new_id)):
                            console.print("[bold green]УСПЕШНО.[/bold green]")
                        else:
                            console.print("[bold red]ОШИБКА.[/bold red]")
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Выбранный цвет недоступен.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимый ID.[/bold yellow]")
                    sleep(2)
                    continue

            elif service == 6: # Смена имени
                console.print("[bold purple][!] Введите ваше новое имя.[/bold purple]")
                new_name = Prompt.ask("[bold][?] Имя[/bold]")
                console.print("[bold purple][%] Сохранение ваших данных[/bold purple]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(new_name):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"")
                        else: continue
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 7: # Смена имени (Радуга)
                console.print("[bold purple][!] Введите ваше новое радужное имя.[/bold purple]")
                new_name = Prompt.ask("[bold][?] Имя[/bold]")
                console.print("[bold purple][%] Сохранение ваших данных[/bold purple]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"")
                        else: continue
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue

            elif service == 8: # Удаление аккаунта
                console.print("[bold purple][!] После удаления аккаунта восстановление невозможно !!.[/bold purple]")
                answ = Prompt.ask("[bold purple][?] Вы хотите удалить этот аккаунт?[/bold purple]", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    console.print("[bold purple][%] Удаление вашего аккаунта[/bold purple]: [bold green]УСПЕШНО.[/bold green].")
                    console.print("==================================")
                    console.print(f"")
                else: continue
            elif service == 9: # Регистрация аккаунта
                console.print("[bold purple][!] Регистрация нового аккаунта.[/bold purple]")
                acc2_email = prompt_valid_value("[bold][?] Email аккаунта[/bold]", "Email", password=False)
                acc2_password = prompt_valid_value("[bold][?] Пароль аккаунта[/bold]", "Пароль", password=False)
                console.print("[bold purple][%] Создание нового аккаунта[/bold purple]: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    console.print(f"[bold red]! ИНФОРМАЦИЯ[/bold red]: Чтобы использовать этот аккаунт")
                    console.print("вы должны войти в игру с этим аккаунтом.")
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Этот email уже существует !.[/bold yellow]")
                    sleep(2)
                    continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 10: # Удаление друзей
                console.print("[bold purple][%] Удаление ваших друзей[/bold purple]: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 11: # Разблокировка платных машин
                console.print("[bold yellow]! Примечание[/bold yellow]: эта функция занимает некоторое время, пожалуйста, не прерывайте процесс.", end=None)
                console.print("[bold purple][%] Разблокировка всех платных машин[/bold purple]: ", end=None)
                if cpm.unlock_paid_cars():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue

            elif service == 12: # Разблокировка двигателя w16
                console.print("[bold purple][%] Разблокировка двигателя w16[/bold purple]: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 13: # Разблокировка всех клаксонов
                console.print("[bold purple][%] Разблокировка всех клаксонов[/bold purple]: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 14: # Отключение повреждений двигателя
                console.print("[bold purple][%] Отключение повреждений двигателя[/bold purple]: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 15: # Безлимитное топливо
                console.print("[bold purple][%] Разблокировка безлимитного топлива[/bold purple]: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 16: # Разблокировка дома 3
                console.print("[bold purple][%] Разблокировка дома 3[/bold purple]: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 17: # Разблокировка дыма
                console.print("[bold purple][%] Разблокировка дыма[/bold purple]: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 18: # Изменение побед в гонках
                console.print("[bold purple][!] Введите, сколько побед в гонках вы хотите.[/bold purple]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold purple][%] Изменение ваших данных[/bold purple]: ", end=None)
                if amount > 0 and amount <= 10000000:
                    if cpm.set_player_wins(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"")
                        else: continue
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 19: # Изменение поражений в гонках
                console.print("[bold purple][!] Введите, сколько поражений в гонках вы хотите.[/bold purple]")
                amount = IntPrompt.ask("[bold][?] Сумма[/bold]")
                console.print("[bold purple][%] Изменение ваших данных[/bold purple]: ", end=None)
                if amount > 0 and amount <= 10000000:
                    if cpm.set_player_loses(amount):
                        console.print("[bold green]УСПЕШНО.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"")
                        else: continue
                    else:
                        console.print("[bold red]ОШИБКА.[/bold red]")
                        console.print("[bold yellow][!] Пожалуйста, попробуйте снова.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста, используйте допустимые значения.[/bold yellow]")
                    sleep(2)
                    continue

            elif service == 20: # Разблокировка всех машин
                console.print("[bold purple][%] Разблокировка машин[/bold purple]: ", end=None)
                if cpm.unlock_all_cars():
                    console.print("[bold green]SУСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста попробуйте заново[/bold yellow]")
                    sleep(2)
                    continue

            elif service == 21: # Разблокировка всех мигалок на машины
                console.print("[bold purple][%] Разблокировка мигалок на машины[/bold purple]: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти?[/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста попробуйте заново[/bold yellow]")
                    sleep(2)
                    continue

            elif service == 22: # Клонирование аккаунта
                console.print("[bold purple]Введите данные для клонирования [/bold purple]:")
                to_email = prompt_valid_value("[bold][?] Почта аккаунта[/bold]", "Почта", password=False)
                to_password = prompt_valid_value("[bold][?] Пароль аккаунта [/bold]", "Пароль", password=False)
                console.print("[bold purple][%] Клонируем ваш аккаунт [/bold purple]: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти? [/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold red]ОШИБКА.[/bold red]")
                    console.print("[bold yellow][!] Пожалуйста попробуйте заново [/bold yellow]")
                    sleep(2)
                    continue

            elif service == 23: #1695hp на машину
                console.print("[bold purple][!] Введите айди авто[/bold purple]")
                car_id = IntPrompt.ask("[bold][?] Айди машины[/bold]")
                console.print("[bold purple][%]ПРОГРЕСС[/bold purple]:",end=None)
                if cpm.hack_car_speed(car_id):
                    console.print("[bold green]УСПЕШНО[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти? [/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold green]УСПЕШНО[bold green]")
                    
                    sleep(2)
                    continue

            elif service == 24: #0 пробег на машину
                console.print("[bold purple][!] Введите айди авто[/bold purple]")
                car_id = IntPrompt.ask("[bold][?] Айди машины[/bold]")
                console.print("[bold purple][%]ПРОГРЕСС[/bold purple]:",end=None)
                if cpm.hack_car_miliage(car_id):
                    console.print("[bold green]УСПЕШНО[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти? [/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold green]УСПЕШНО[bold green]")

            elif service == 25: #убрать передний бампер
                console.print("[bold purple][!] Введите айди авто[/bold purple]")
                car_id = IntPrompt.ask("[bold][?] Айди машины[/bold]")
                console.print("[bold purple][%]ПРОГРЕСС[/bold purple]:",end=None)
                if cpm.hack_car_front(car_id):
                    console.print("[bold green]УСПЕШНО[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти? [/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold green]УСПЕШНО[bold green]")
                    
                    sleep(2)
                    continue

            elif service == 26: #убрать задний бампер
                console.print("[bold purple][!] Введите айди авто[/bold purple]")
                car_id = IntPrompt.ask("[bold][?] Айди машины[/bold]")
                console.print("[bold purple][%]ПРОГРЕСС[/bold purple]:",end=None)
                if cpm.hack_car_back(car_id):
                    console.print("[bold green]УСПЕШНО[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask("[bold purple][?] Вы хотите выйти? [/bold purple]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"")
                    else: continue
                else:
                    console.print("[bold green]УСПЕШНО[bold green]")
                    
                    sleep(2)
                    continue
                if answ == "n": 
                    break
            else: continue
            break
        break