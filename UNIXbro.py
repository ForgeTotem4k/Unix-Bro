import subprocess
import re
from mistralai.client import MistralClient
from colorama import Fore, Back, Style, init

# Initialize Colorama (auto-resets colors after output)
init(autoreset=True)

client = MistralClient(api_key="your_mistralai_api_here")  # Replace with your key

def generate_command(user_request: str) -> str:
    """Converts user request into UNIX command using Mistral."""
    response = client.chat(
        model="mistral-small",
        messages=[{
            "role": "user",
            "content": f"""
            User wants: '{user_request}'. 
            Provide ONLY ONE UNIX command:
            - Separate multiple commands with && (AND), | (PIPE) or ; (SEQUENCE). use separate only when necessary
            - No backticks, quotes, or explanations - pure terminal command only
            - Any deviation will be considered an error
            - Examples:
              Request: "show files" → ls -l
              Request: "check youtube" → ping youtube.com
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
        # Green for success
        output = result.stdout or result.stderr or f"{Fore.GREEN}✓ Command executed"
        return output
    except Exception as e:
        # Red for errors
        return f"{Fore.RED}✗ Error: {e}"

def main():
    # Colorful header
    print(f"{Back.BLUE}{Fore.WHITE}🔮 UNIX-Bro by forge {Style.RESET_ALL}")
    print(f"{Fore.CYAN}Enter your request ({Fore.YELLOW}exit{Fore.CYAN} to quit){Style.RESET_ALL}")
    
    while True:
        user_input = input(f"\n{Fore.MAGENTA}➜ {Style.RESET_ALL}").strip()
        if user_input.lower() == "exit":
            print(f"{Fore.YELLOW}🚪 Exiting...{Style.RESET_ALL}")
            break
        
        command = generate_command(user_input)
        # Yellow for command display
        print(f"\n{Fore.YELLOW}⌨  Command: {Fore.CYAN}{command}{Style.RESET_ALL}")
        
        # Confirmation prompt
        confirm = input(f"{Fore.WHITE}Execute command? {Style.DIM}({Fore.GREEN}y{Style.RESET_ALL}{Style.DIM}/{Fore.RED}N{Style.RESET_ALL}{Style.DIM}){Style.RESET_ALL}: ").lower()
        if confirm == "y":
            result = execute_command(command)
            print(result)  # Colored output
        else:
            print(f"{Fore.RED}✗ Cancelled{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
