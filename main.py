import random
import requests
from time import sleep
import os, signal, sys
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from fatool import termuxtoolfa

__CHANNEL_USERNAME__ = "FAtermux & astron_om"
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
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
            console.print("[bold][purple]================[/purple][[bold purple] ДАННЫЕ ИГРОКА [bold purple]][purple]================[/purple][/bold]")
            console.print(f"[bold purple]Имя   [/bold purple]: { (data.get('Name') if 'Name' in data else 'НЕ ОПРЕДЕЛЕНО') }.")
            console.print(f"[bold purple]Айди[/bold purple]: { (data.get('localID') if 'localID' in data else 'НЕ ОПРЕДЕЛЕНО') }.")
            console.print(f"[bold purple]Деньги  [/bold purple]: { (data.get('money') if 'money' in data else 'НЕ ОПРЕДЕЛЕНО') }.")
            console.print(f"[bold purple]Монеты  [/bold purple]: { (data.get('coin') if 'coin' in data else 'НЕ ОПРЕДЕЛЕНО') }.")
        else:
            console.print("[bold red]! ОШИБКА[/bold red]: новые аккаунты должны хотя бы один раз войти в игру !.")
            exit(1)
    else:
        console.print("[bold red]! ОШИБКА[/bold red]: похоже, ваш вход не был выполнен правильно !.")
        exit(1)
    
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

if __name__ == "__main__":

    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold purple][?] Email аккаунта[/bold purple]", "Email", password=False)
        acc_password = prompt_valid_value("[bold purple][?] Пароль аккаунта[/bold purple]", "Пароль", password=False)
        acc_access_key = prompt_valid_value("[bold purple][?] Ключ доступа[/bold purple]", "Ключ доступа", password=False)
        console.print("[bold purple][%] Попытка входа[/bold purple]: ", end=None)
        cpm = CarParkTool(acc_access_key)
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

            # Начальный фиолетовый цвет (RGB: 128, 0, 128)
            base_color = (128, 0, 128)

            # Список функций
            functions = [
                "Увеличение денег ",
                "Увеличение монет ",
                "Ранг King ",
                "Смена ID ",
                "Смена имени ",
                "Смена имени (Радуга) ",
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
                "Изменение поражений в гонках"
                
            ]

            # Вывод функций с градиентным цветом
            for i, func in enumerate(functions):
                # Уменьшаем значение красного и синего компонентов для затемнения
                r = max(base_color[0] - i * 5, 0)  # Уменьшаем красный
                b = max(base_color[2] - i * 5, 0)  # Уменьшаем синий
                color = f"rgb({r},0,{b})"  # Фиолетовый цвет с затемнением
                console.print(f"[bold][purple]({i+1:02}):[/purple] [{color}]{func}[/{color}]")

            console.print("[bold][purple](0) :[/purple] [red]Выход[/red]", end="\n\n")

            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
            service = IntPrompt.ask(f"[bold][?] Выберите функцию [red][1-{choices[-1]} или 0][/red][/bold]", choices=choices, show_choices=False)
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
            elif service == 5: # Смена имени
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
            elif service == 6: # Смена имени (Радуга)
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

            elif service == 7: # Удаление аккаунта
                console.print("[bold purple][!] После удаления аккаунта восстановление невозможно !!.[/bold purple]")
                answ = Prompt.ask("[bold purple][?] Вы хотите удалить этот аккаунт?[/bold purple]", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    console.print("[bold purple][%] Удаление вашего аккаунта[/bold purple]: [bold green]УСПЕШНО.[/bold green].")
                    console.print("==================================")
                    console.print(f"")
                else: continue
            elif service == 8: # Регистрация аккаунта
                console.print("[bold purple][!] Регистрация нового аккаунта.[/bold purple]")
                acc2_email = prompt_valid_value("[bold][?] Email аккаунта[/bold]", "Email", password=False)
                acc2_password = prompt_valid_value("[bold][?] Пароль аккаунта[/bold]", "Пароль", password=False)
                console.print("[bold purple][%] Создание нового аккаунта[/bold purple]: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold green]УСПЕШНО.[/bold green]")
                    console.print("==================================")
                    console.print(f"[bold red]! ИНФОРМАЦИЯ[/bold red]: Чтобы использовать этот аккаунт с CarParkTool")
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
            elif service == 9: # Удаление друзей
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
            elif service == 10: # Разблокировка платных машин
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

            elif service == 11: # Разблокировка двигателя w16
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
            elif service == 12: # Разблокировка всех клаксонов
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
            elif service == 13: # Отключение повреждений двигателя
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
            elif service == 14: # Безлимитное топливо
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
            elif service == 15: # Разблокировка дома 3
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
            elif service == 16: # Разблокировка дыма
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
            elif service == 17: # Изменение побед в гонках
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
            elif service == 18: # Изменение поражений в гонках
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
            break
        break