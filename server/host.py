import socket
import threading
import json
import time
from shared.utils import print_banner

clients = []
player_data = {}
server_socket = None
room_password = ""
is_server_running = False

def broadcast(msg_dict, exclude_sock=None):
    data = json.dumps(msg_dict).encode('utf-8')
    for c in clients[:]:
        if c == exclude_sock:
            continue
        try:
            c.send(data)
        except:
            remove_player(c)

def remove_player(sock):
    if sock in clients:
        name = player_data.get(sock, {}).get("name", "Unknown")
        clients.remove(sock)
        if sock in player_data:
            del player_data[sock]
        sock.close()
        print(f"\n{name} left.")
        broadcast({"player": "SERVER", "msg": f"{name} left the room."})

def handle_client(sock, addr):
    global is_server_running
    try:
        if room_password:
            sock.send(json.dumps({"type": "auth_req", "msg": "Password: "}).encode('utf-8'))
            guess = sock.recv(1024).decode('utf-8')
            if guess != room_password:
                sock.send(json.dumps({"type": "error", "msg": "Wrong password!"}).encode('utf-8'))
                sock.close()
                return
        
        sock.send(json.dumps({"type": "name_req", "msg": "Username: "}).encode('utf-8'))
        name = sock.recv(1024).decode('utf-8')
        if not name:
            name = f"Guest{addr[1]}"
        
        player_data[sock] = {"name": name, "score": 0}
        clients.append(sock)
        
        print(f"\n{name} connected from {addr[0]}")
        broadcast({"player": "SERVER", "msg": f"{name} joined!"})

        while is_server_running:
            try:
                raw_data = sock.recv(1024)
                if not raw_data:
                    break
                
                msg = json.loads(raw_data.decode('utf-8'))
                broadcast(msg, exclude_sock=sock)
            except:
                break
    except:
        pass
    finally:
        remove_player(sock)

def start_listening(ip, port):
    global server_socket, is_server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((ip, port))
        server_socket.listen(5)
        is_server_running = True
        print(f"\nServer started on {ip}:{port}")
        
        while is_server_running:
            try:
                conn, addr = server_socket.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except:
                break
    except Exception as e:
        print(f"\nError: {e}")
        is_server_running = False

def list_players():
    print("\n--- Players ---")
    if not player_data:
        print("Empty.")
    else:
        for i, (s, info) in enumerate(player_data.items()):
            print(f"{i+1}. {info['name']} (Score: {info['score']})")

def kick():
    list_players()
    if not player_data: return
    try:
        num = int(input("Kick who (number): ")) - 1
        target = list(player_data.keys())[num]
        name = player_data[target]['name']
        target.send(json.dumps({"type": "error", "msg": "Kicked by host"}).encode('utf-8'))
        remove_player(target)
        print(f"Done, kicked {name}.")
    except:
        print("Invalid number.")

def close_room():
    global is_server_running
    print("Closing...")
    broadcast({"player": "SERVER", "msg": "Host closed the room."})
    is_server_running = False
    for c in clients:
        c.close()
    if server_socket:
        server_socket.close()

def run_host():
    global room_password
    print_banner()
    print(">>> HOST <<<")
    my_ip = input("IP (default 0.0.0.0): ") or "0.0.0.0"
    room_password = input("Password (blank for none): ")
    
    threading.Thread(target=start_listening, args=(my_ip, 55555), daemon=True).start()
    time.sleep(1)
    
    while is_server_running:
        print("\n[MENU] 1:Players 2:Kick 3:Start 4:Exit")
        choice = input("Select: ")
        
        if choice == "1":
            list_players()
        elif choice == "2":
            kick()
        elif choice == "3":
            print("Game logic coming soon...")
        elif choice == "4":
            close_room()
            break
        else:
            print("Unknown.")
