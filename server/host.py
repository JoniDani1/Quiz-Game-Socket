import socket
import threading
import json
import time
from shared.utils import print_banner
from shared.codes import ip_to_code, get_lan_ip

clients = []
player_data = {}
server_socket = None
room_password = ""
is_server_running = False
current_answer = None
round_count = 0

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
        broadcast({"player": "SERVER", "msg": f"*** {name} left the room. ***"})

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
        
        welcome_msg = {
            "player": "SYSTEM",
            "msg": "\n" + "="*30 + "\n   WELCOME TO THE QUIZ!\n" + "="*30 + 
                   "\n- Type your answers in the chat.\n- First one to get it right wins!\n- Type /leave to quit.\n" + "="*30
        }
        sock.send(json.dumps(welcome_msg).encode('utf-8'))
        time.sleep(0.1)
        
        broadcast({"player": "SERVER", "msg": f"*** {name} joined the room! ***"})

        while is_server_running:
            try:
                raw_data = sock.recv(1024)
                if not raw_data:
                    break
                
                msg = json.loads(raw_data.decode('utf-8'))
                
                global current_answer, round_count
                txt = msg.get("msg", "")
                
                if current_answer and txt.lower() == current_answer.lower():
                    player_data[sock]["score"] += 1
                    winner = player_data[sock]["name"]
                    
                    win_msg = "\n" + "*"*40 + "\n"
                    win_msg += f"   CORRECT! {winner} got it! \n"
                    win_msg += f"   The answer was: {current_answer}\n"
                    win_msg += "*"*40
                    
                    scoreboard = "\n--- CURRENT SCORES ---\n"
                    for s in player_data:
                        p_info = player_data[s]
                        scoreboard += f"{p_info['name']}: {p_info['score']} pts\n"
                    
                    broadcast({"player": "SERVER", "msg": win_msg + scoreboard})
                    
                    current_answer = None
                    round_count += 1
                    
                    if round_count >= 10:
                        winner_name = "No one"
                        max_score = -1
                        for s_sock, info in player_data.items():
                            if info["score"] > max_score:
                                max_score = info["score"]
                                winner_name = info["name"]
                                
                        time.sleep(0.1)
                        broadcast({"player": "SERVER", "msg": f"\n=== GAME OVER! The champion is {winner_name} with {max_score} points! ==="})
                        round_count = 0
                        for s_sock in player_data:
                            player_data[s_sock]["score"] = 0
                else:
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
        print(f"Kicked {name}.")
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

def question_timer(ans):
    time.sleep(15)
    global current_answer, round_count
    if current_answer == ans:
        timeout_msg = "\n" + "!"*40 + "\n"
        timeout_msg += f"   TIME IS UP! No one got it.\n"
        timeout_msg += f"   The correct answer was: {ans}\n"
        timeout_msg += "!"*40
        broadcast({"player": "SERVER", "msg": timeout_msg})
        
        current_answer = None
        round_count += 1
        if round_count >= 10:
            winner_name = "No one"
            max_score = -1
            for s_sock, info in player_data.items():
                if info["score"] > max_score:
                    max_score = info["score"]
                    winner_name = info["name"]
            time.sleep(0.1)
            broadcast({"player": "SERVER", "msg": f"\n=== GAME OVER! The champion is {winner_name} with {max_score} points! ==="})
            round_count = 0
            for s_sock in player_data:
                player_data[s_sock]["score"] = 0

def run_host():
    global room_password
    print_banner()
    print(">>> HOST <<<")
    lan_ip = get_lan_ip()
    room_code = ip_to_code(lan_ip)
    
    room_password = input("Room Password (blank for none): ")
    
    print(f"\n--- ROOM CREATED ---")
    print(f"YOUR ROOM CODE: {room_code}")
    print(f"(Local IP: {lan_ip})")
    
    threading.Thread(target=start_listening, args=("0.0.0.0", 55555), daemon=True).start()
    time.sleep(1)
    
    while is_server_running:
        print("\n[MENU] 1:Players 2:Kick 3:Ask Question 4:Exit")
        choice = input("Select: ")
        
        if choice == "1":
            list_players()
        elif choice == "2":
            kick()
        elif choice == "3":
            q = input("Enter Question: ")
            if not q: continue
            a = input("Enter Answer: ")
            if not a: continue
            
            global current_answer
            current_answer = a.strip()
            
            q_msg = "\n" + "#"*40 + "\n"
            q_msg += f"   QUESTION {round_count+1}: {q.strip()}\n"
            q_msg += "   (You have 15 seconds!)\n"
            q_msg += "#"*40
            broadcast({"player": "SERVER", "msg": q_msg})
            
            threading.Thread(target=question_timer, args=(current_answer,), daemon=True).start()
        elif choice == "4":
            close_room()
            break
        else:
            print("Unknown.")
