import socket
import json
import time
from shared.utils import print_banner

def listen_to_server(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("\nLost connection.")
                break
            
            res = json.loads(data.decode('utf-8'))
            
            if res.get("type") == "error":
                print(f"\nError: {res['msg']}")
                break
            else:
                p = res.get("player", "???")
                m = res.get("msg", "")
                print(f"\n[{p}] {m}")
        except:
            break
    s.close()

def run_player():
    import threading
    print_banner()
    print(">>> JOIN <<<")
    target_ip = input("Host IP: ")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((target_ip, 55555))
    except:
        print("Couldn't connect.")
        time.sleep(2)
        return

    name = ""
    try:
        while True:
            raw = sock.recv(1024)
            if not raw: return
            res = json.loads(raw.decode('utf-8'))
            
            if res.get("type") == "auth_req":
                pw = input(res["msg"])
                sock.send(pw.encode('utf-8'))
            elif res.get("type") == "name_req":
                name = input(res["msg"])
                sock.send(name.encode('utf-8'))
                break
            elif res.get("type") == "error":
                print(f"\n{res['msg']}")
                sock.close()
                time.sleep(2)
                return
    except:
        sock.close()
        return

    threading.Thread(target=listen_to_server, args=(sock,), daemon=True).start()
    
    print("\nConnected! Type /leave to quit.")

    while True:
        txt = input()
        if not txt: continue
        
        if txt.lower() == "/leave":
            print("Bye!")
            sock.close()
            break
        
        try:
            sock.send(json.dumps({"player": name, "msg": txt}).encode('utf-8'))
        except:
            break

    print("\nGoing back...")
    time.sleep(1)
