import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print("**********************************************")
    print("*                                            *")
    print("*        WELCOME TO QUIZ GAME SOCKET         *")
    print("*       A Computer Networks Project          *")
    print("*                                            *")
    print("**********************************************")
