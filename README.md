# Quiz Game Socket

A terminal-based multiplayer quiz game built with Python sockets. This project uses a single unified script for both hosting and joining games. One player acts as the host (question asker), and up to 5 others join as contestants to answer questions and compete for points.

## How to Play

1.  **Start the Game**:
    ```bash
    python main.py
    ```
2.  **Choose Mode**:
    - **Host (H)**: Create a new room. The script will generate a **Room ID**. Share this ID with your friends.
    - **Join (J)**: Enter a Room ID to connect to a host.
3.  **The Game Loop**:
    - **Host**: Type a question and its answer using the format: `/ask Question|Answer`.
    - **Contestants**: See the question and type your answer in the chat.
    - **Timing**: You have a limited time to respond before the round expires.
    - **Winning**: After 10 rounds, the player with the highest score is crowned the champion.

## Authors
- [<img src="https://github.com/JoniDani1.png" width="25" height="25"> **Joni Dani**](https://github.com/JoniDani1)
- [<img src="https://github.com/yigit-guven.png" width="25" height="25"> **Yiğit Güven**](https://github.com/yigit-guven)
- **Dev Musk**

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).