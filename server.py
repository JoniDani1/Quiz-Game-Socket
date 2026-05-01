import socket
import threading
import json

# Configuration
HOST = '127.0.0.1' # Localhost for testing. Change to your local IPv4 for LAN.
PORT = 55555

# Server Initialization
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = [] # List to track connected client sockets

game_state = {
    "question": None,
    "answer": None,
    "active": False
}
scores = {}

def broadcast(message_dict):
    """Encodes a Python dictionary into JSON and sends it to ALL clients."""
    json_data = json.dumps(message_dict).encode('utf-8')
    for client in clients:
        try:
            client.send(json_data)
        except:
            # If a send fails, the client likely disconnected abruptly.
            remove(client)

def remove(client):
    """Safely removes a client from the active pool."""
    if client in clients:
        clients.remove(client)
        client.close()

def handle_client(client, address):
    """The thread that runs for EVERY connected player."""
    print(f"[SERVER LOG] Connection established with {address}")
    
    while True:
        try:
            # 1. Wait for incoming data
            data = client.recv(1024)
            if not data:
                break # Client disconnected gracefully
            
            # 2. Decode bytes to string, then parse JSON to dictionary
            message = json.loads(data.decode('utf-8'))
            print(f"[TRAFFIC] Received from {address}: {message}")
            
            sender = message.get("player", "Unknown")
            text = message.get("msg", "")
            
            # Register player in the score tracker if they are new
            if sender not in scores:
                scores[sender] = 0

            # --- THE STATE MACHINE LOGIC ---
            if text.startswith("/ask "):
                # Host command format: /ask Question|Answer
                # Example: /ask Who is my best friend?|Yigit
                try:
                    q_and_a = text[5:].split("|")
                    game_state["question"] = q_and_a[0].strip()
                    game_state["answer"] = q_and_a[1].strip().lower()
                    game_state["active"] = True # Open the floor for answers!
                    
                    broadcast({"player": "SERVER", "msg": f"\n=== [NEW QUESTION] {game_state['question']} ==="})
                except Exception:
                    # If the host messed up the format, tell only them
                    error_msg = json.dumps({"player": "SERVER", "msg": "Error. Use format: /ask Question|Answer"}).encode('utf-8')
                    client.send(error_msg)
                    
            elif game_state["active"]:
                # The floor is open, check answers
                if text.strip().lower() == game_state["answer"]:
                    game_state["active"] = False # Lock the round so nobody else can answer!
                    scores[sender] += 1
                    
                    # ... previous code ...
                    win_msg = f"*** {sender.upper()} WAS FIRST! *** The answer was {game_state['answer'].upper()}. ({sender}'s total score: {scores[sender]})"
                    broadcast({"player": "SERVER", "msg": win_msg})
                    
                    # --- ADD THIS WIN CONDITION ---
                    if scores[sender] >= 3:
                        match_win_msg = f"\n========================================\nGAME OVER! {sender.upper()} WINS THE MATCH!\n========================================\nScores have been reset. Host can /ask to start a new game."
                        broadcast({"player": "SERVER", "msg": match_win_msg})
                        scores.clear() # Resets the dictionary for the next game
                else:
                    # Wrong guess, just broadcast it like a normal message
                    broadcast(message)
            else:
                # No active question, act like a normal lobby
                broadcast(message)
            
        except json.JSONDecodeError:
            print(f"[SERVER ERROR] Dropped malformed packet from {address}")
            break
        except Exception as e:
            print(f"[SERVER ERROR] Exception with {address}: {e}")
            break
            
    remove(client)
    print(f"[SERVER LOG] Connection closed with {address}")

def start_server():
    """Main listening loop."""
    print(f"[SERVER START] Listening on {HOST}:{PORT}...")
    while True:
        # Blocks until a new client connects
        client, address = server.accept()
        clients.append(client)
        
        # Spawn a new thread so the server doesn't freeze waiting for this client
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()
        print(f"[SERVER LOG] Active players: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()