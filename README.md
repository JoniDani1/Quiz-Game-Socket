# Quiz Game Socket

A terminal-based multiplayer quiz game built with Python sockets. This project uses a single unified script for both hosting and joining games. One player acts as the host (question asker), and up to 5 others join as contestants to answer questions and compete for points.

## How to Play

1.  **Start the Game**:
    ```bash
    python main.py
    ```
2.  **Choose Mode**:
    - **Host**: Create a new room. The script will generate a **Room Code**. Share this code with your friends. You must select **"Start Game"** from the menu to lock the room and begin.
    - **Join**: Enter the **Room Code** provided by the host. If the game has already started, you will have to wait for the next match.
3.  **The Game Loop**:
    - **Host**: Once the game is started, use the "Ask Question" option. You must wait for each question to finish before asking the next one.
    - **Contestants**: Type your answers in the chat. The first one to get it right wins the point!
    - **Commands**: Type `/leave` to quit or `/players` to see the current leaderboard.
    - **Timing**: You have **15 seconds** to respond before the round expires.
    - **Winning**: After 10 rounds, the champion is crowned and scores are reset.

## How It Works

This project is built on a **Client-Server architecture** using Python's `socket` and `threading` libraries.

1.  **The Host (Server)**: When a player chooses to host, the application starts a TCP server on port `55555`. It generates a **Room Code** by encoding the host's local IP address into a 4-character string for easy sharing.
2.  **The Players (Clients)**: Players enter the Room Code, which the application decodes back into an IP address to establish a **TCP Socket** connection.
3.  **Multithreading**: The host uses the `threading` module to handle multiple players simultaneously. Every time a new player joins, a new thread is spawned to listen for that specific player's messages.
4.  **Data Transmission (JSON)**: All communication is serialized into **JSON strings**. This ensures that data like player scores, system messages, and questions are parsed reliably across the network.
5.  **The Game Loop**: The server **broadcasts** questions to all clients. It then monitors incoming messages; the first message that matches the answer triggers a point award and updates the leaderboard for all players.

### Room Code Logic (IP Encoding)

The "Room Code" isn't a random string; it's a **Base64-encoded representation** of the host's local IP address.

*   **IP to Code**: The 4 octets of an IP address (e.g., `192.163.1.10`) are converted into 4 bytes. These bytes are encoded using Base64, and special characters (like `+` or `/`) are sanitized to make the code cleaner.
*   **Code to IP**: When a player joins, the application reverses the process: it reverts the sanitation, adds padding, and decodes the Base64 string back into the 4 bytes that make up the original IP.

This allows players to connect using a short, readable string instead of typing out long, numerical IP addresses.

### Networking Principles

This game demonstrates several core networking concepts:

*   **LAN (Local Area Network)**: The game is designed to run on a local network. It uses **Private IP addresses** (like `192.168.x.x`), meaning players must be on the same WiFi or Ethernet connection to play.
*   **TCP (Transmission Control Protocol)**: Unlike UDP (User Datagram Protocol) which is fast but "lossy", this project uses **TCP**. TCP is a connection-oriented protocol that ensures data is delivered reliably and in the correct order.
*   **Ports**: The server uses **Port 55555**. In networking, an IP address gets you to the computer, but the Port gets you to the specific application.
*   **The Socket Lifecycle**:
    1.  **Bind**: The Host "claims" port 55555 (Dynamic/Private range) on its machine.
    2.  **Listen**: The Host waits for incoming connection requests.
    3.  **Accept**: When a player connects, the Host creates a dedicated connection for them.
    4.  **Communication**: Both the Host and Player can send and receive data at the same time using separate threads.

## Authors
- [<img src="https://github.com/JoniDani1.png" width="25" height="25"> **Joni Dani**](https://github.com/JoniDani1)
- [<img src="https://github.com/yigit-guven.png" width="25" height="25"> **Yiğit Güven**](https://github.com/yigit-guven)
- [<img src="https://github.com/thenextstark.png" width="25" height="25"> **Dev Dubey**](https://github.com/thenextstark)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).