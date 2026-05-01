import sys
from shared.utils import print_banner
from server.host import run_host
from client.player import run_player

def main():
    while True:
        print_banner()
        print("1. Host a Game")
        print("2. Join a Game")
        print("3. Exit")
        choice = input("\nSelect option: ")
        
        if choice == "1":
            run_host()
        elif choice == "2":
            run_player()
        elif choice == "3":
            print("Bye bye!")
            sys.exit()
        else:
            print("Wrong choice, try again.")

if __name__ == "__main__":
    main()
