import os

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{CYAN}**********************************************")
    print("*                                            *")
    print("*        WELCOME TO QUIZ GAME SOCKET         *")
    print("*       A Computer Networks Project          *")
    print("*                                            *")
    print(f"**********************************************{RESET}")
