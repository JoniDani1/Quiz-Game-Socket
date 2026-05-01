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

## Authors
- [<img src="https://github.com/JoniDani1.png" width="25" height="25"> **Joni Dani**](https://github.com/JoniDani1)
- [<img src="https://github.com/yigit-guven.png" width="25" height="25"> **Yiğit Güven**](https://github.com/yigit-guven)
- **Dev Musk**

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).