import subprocess
import re
from mistralai.client import MistralClient
from colorama import Fore, Back, Style, init

# Инициализируем Colorama (автоматически сбрасывает цвета после вывода)
init(autoreset=True)

client = MistralClient(api_key="your_api_key")  # Замените на ваш ключ

def generate_commands(user_request: str) -> list:
    #Промт для нормальной генерации
    response = client.chat(
        model="mistral-small",
        messages=[{
            "role": "user",
            "content": f"""
            Пользователь хочет: '{user_request}'. 
            Дай список UNIX-команд (одну или несколько):
            - Пользователь САМ знает что за что отвечает. Поэтому никаких пояснений. пояснение в команде = ошибка, и подставление всей системы.
            - Каждая команда должна быть на отдельной строке
            - Без любых `, кавычек, пояснений, чистейшие команды для терминала
            - Примеры:
              Запрос: "покажи файлы и проверь ютуб" → 
                ls -l
                ping youtube.com
              Запрос: "создай папку и перейди в нее" → 
                mkdir new_folder
                cd new_folder
            """
        }]
    )
    # Разбиваем ответ на отдельные команды, удаляя пустые строки
    commands = [cmd.strip() for cmd in response.choices[0].message.content.split('\n') if cmd.strip()]
    return commands

def execute_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            text=True, 
            capture_output=True,
            timeout=10,
            executable="/bin/bash"
        )
        # Зеленый цвет для успешного выполнения
        output = result.stdout or result.stderr or f"{Fore.GREEN}✅ Команда выполнена"
        return output
    except Exception as e:
        # Красный цвет для ошибок
        return f"{Fore.RED}❌ Ошибка: {e}"

def main():
    # Яркое цветное приветствие
    print(f"{Back.BLUE}{Fore.WHITE}🔮 UNIX-Bro by forge {Style.RESET_ALL}")
    print(f"{Fore.CYAN}Пишите что сделать ({Fore.YELLOW}exit{Fore.CYAN} — выход){Style.RESET_ALL}")
    
    while True:
        user_input = input(f"\n{Fore.MAGENTA}➜ {Style.RESET_ALL}").strip()
        if user_input.lower() == "exit":
            print(f"{Fore.YELLOW}🚪 Выход из терминала...{Style.RESET_ALL}")
            break
        
        commands = generate_commands(user_input)
        
        # Выводим список команд с нумерацией
        print(f"\n{Fore.YELLOW}⌨  Найдены команды:{Style.RESET_ALL}")
        for i, cmd in enumerate(commands, 1):
            print(f"{Fore.CYAN}{i}. {cmd}{Style.RESET_ALL}")
        
        # Варианты подтверждения
        print(f"\n{Fore.WHITE}Выберите действие:{Style.RESET_ALL}")
        print(f"{Style.DIM}({Fore.GREEN}a{Style.RESET_ALL}{Style.DIM}) Выполнить все{Style.RESET_ALL}")
        print(f"{Style.DIM}({Fore.GREEN}1-{len(commands)}{Style.RESET_ALL}{Style.DIM}) Выполнить конкретную{Style.RESET_ALL}")
        print(f"{Style.DIM}({Fore.RED}n{Style.RESET_ALL}{Style.DIM}) Отменить{Style.RESET_ALL}")
        
        choice = input(f"{Fore.MAGENTA}➜ {Style.RESET_ALL}").lower()
        
        if choice == 'a':
            # Выполняем все команды последовательно
            for cmd in commands:
                print(f"\n{Fore.YELLOW}⌨  Выполняется: {Fore.CYAN}{cmd}{Style.RESET_ALL}")
                result = execute_command(cmd)
                print(result)
        elif choice.isdigit() and 1 <= int(choice) <= len(commands):
            # Выполняем конкретную команду
            cmd = commands[int(choice)-1]
            print(f"\n{Fore.YELLOW}⌨  Выполняется: {Fore.CYAN}{cmd}{Style.RESET_ALL}")
            result = execute_command(cmd)
            print(result)
        else:
            print(f"{Fore.RED}❌ Отменено{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
