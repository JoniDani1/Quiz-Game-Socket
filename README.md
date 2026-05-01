# Quiz Game Socket

A terminal-based multiplayer quiz game built with Python sockets. This project uses a single unified script for both hosting and joining games. One player acts as the host (question asker), and up to 5 others join as contestants to answer questions and compete for points.

## How to Play

1.  **Start the Game**:
    ```bash
    python main.py
    ```
2.  **Choose Mode**:
    - **Host**: Create a new room. The script will generate a **Room Code** (e.g., `wPizcg`). Share this code with your friends.
    - **Join**: Enter the **Room Code** provided by the host to connect.
3.  **The Game Loop**:
    - **Host**: Use the menu to select "Ask Question". Enter the question and the answer in the separate prompts.
    - **Contestants**: See the question in the chat and type your answer. The first one to get it right wins the point!
    - **Commands**: Type `/leave` at any time to quit the room.
    - **Timing**: You have **15 seconds** to respond before the round expires.
    - **Winning**: After 10 rounds, the player with the highest score is crowned the champion, and scores are reset.

## Authors
- [<img src="https://github.com/JoniDani1.png" width="25" height="25"> **Joni Dani**](https://github.com/JoniDani1)
- [<img src="https://github.com/yigit-guven.png" width="25" height="25"> **Yiğit Güven**](https://github.com/yigit-guven)
- **Dev Musk**

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).