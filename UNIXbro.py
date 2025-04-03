import subprocess
import re
from mistralai.client import MistralClient
from colorama import Fore, Back, Style, init

# Инициализируем Colorama (автоматически сбрасывает цвета после вывода)
init(autoreset=True)

client = MistralClient(api_key="tQuGZnnnDS5h9xjuW6yjbNIbWpthUK1W")  # Замените на ваш ключ

def generate_command(user_request: str) -> str:
    """Преобразует запрос в UNIX-команду через Mistral."""
    response = client.chat(
        model="mistral-small",
        messages=[{
            "role": "user",
            "content": f"""
            Пользователь хочет: '{user_request}'. 
            Дай ТОЛЬКО одну UNIX-команду:
            - Без любых `, кавычек, пояснений, чистейшая команда для терминала. любое противоречие - считаеться ошибкой
            - Примеры:
              Запрос: "покажи файлы" → ls -l
              Запрос: "проверь ютуб" → ping youtube.com
            """
        }]
    )
    return response.choices[0].message.content.strip()

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
        
        command = generate_command(user_input)
        # Желтый цвет для показа команды
        print(f"\n{Fore.YELLOW}⌨  Команда: {Fore.CYAN}{command}{Style.RESET_ALL}")
        
        # Подтверждение с цветовым акцентом
        confirm = input(f"{Fore.WHITE}Выполнить команду? {Style.DIM}({Fore.GREEN}y{Style.RESET_ALL}{Style.DIM}/{Fore.RED}N{Style.RESET_ALL}{Style.DIM}){Style.RESET_ALL}: ").lower()
        if confirm == "y":
            result = execute_command(command)
            print(result)  # Результат уже цветной
        else:
            print(f"{Fore.RED}❌ Отменено{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
