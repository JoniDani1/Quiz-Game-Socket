import socket
import threading
import json
import sys

# Configuration - Must match server.py
HOST = '127.0.0.1' 
PORT = 55555

# 1. Identity
username = input("Enter your username to join the game: ")

# 2. Connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    print(f"[SUCCESS] Connected to server as {username}.")
    print("Type your messages below. Type '/quit' to exit.\n" + "-"*40)
except ConnectionRefusedError:
    print("[ERROR] Server is offline. Run server.py first.")
    sys.exit()

# 3. The Listening Thread
def receive_messages():
    """Constantly listens for data from the server."""
    while True:
        try:
            # Wait for data
            data = client.recv(1024)
            if not data:
                print("\n[SERVER] Server closed the connection.")
                client.close()
                sys.exit()
            
            # Decode and load JSON
            message = json.loads(data.decode('utf-8'))
            
            sender = message.get("player", "Unknown")
            text = message.get("msg", "")
            
            # Print the message (unless it's our own message bouncing back)
            if sender != username:
                print(f"\n[{sender}] {text}")
                
        except Exception as e:
            print(f"\n[ERROR] Connection lost: {e}")
            client.close()
            sys.exit()

# 4. The Sending Thread
def send_messages():
    """Waits for you to type and sends it to the server."""
    while True:
        # Get user input
        text = input()
        
        # Check for quit command
        if text == '/quit':
            client.close()
            sys.exit()
            
        # Package into JSON
        message_dict = {
            "player": username,
            "msg": text
        }
        
        try:
            # Encode and send
            json_data = json.dumps(message_dict).encode('utf-8')
            client.send(json_data)
        except:
            print("[ERROR] Failed to send message. Server might be down.")
            sys.exit()

# 5. Start the Engine
# Daemon threads automatically die when the main program exits
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

send_thread = threading.Thread(target=send_messages, daemon=True)
send_thread.start()

# Keep the main thread alive while the background threads do the work
while True:
    try:
        pass
    except KeyboardInterrupt:
        client.close()
        sys.exit()