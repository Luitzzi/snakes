<!-- [![Contributors][contributors-shield]][https://github.com/Luitzzi/snakes] -->
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
<br />

<!-- Banner and introduction -->
![Ultimate Snakes Banner](/assets/images/banner.png)
<br />
<br />
Welcome to the ULTIMATE SNAKES GAME - feature rich with modern AI-Technology

---

## Features
* **Beautiful self pixeled snake animations** <br />
    It wiggles, eats and bumps his head.
* **Train your own AI**<br /> 
    Special mode where you can train an AI using reinforcement learning
    with experience replay on your OWN computer!
* **Overview and replay over previous runs** <br />
    Look through all your old runs sorted by their score or playtime and replay the most interesting ones
* **Framework for Game-modes and Players** <br />
    Clear structure for game-modes and players allowing simple game extensions.

![Gif presenting a complete game](/assets/images/complete_game.gif)

## What did we learn?
* **Clean, structured and easily expandable Code** <br />
    Using OOP we implemented a well-defined structure of the different game aspects. <br />
    The GUI, Game and AI-logic is clearly separated. The different game-states are managed by the 
    class GameManager calling the methods corresponding to the current state. <br />
<br />
    * **Easy expandable game-modes and player-agents using the Strategy-Pattern** <br />
        Game-modes such as Singleplayer, Replay etc. all implement the 'Interface' Playable.
        Players are defined by a Strategy Interface as well and are dynamically created based on the user-input at runtime
        using the Factory Pattern. This ensures consistency and enables easy expansions. <br />
    <br />
    * **Well-defined event-handling using the EventManager class as an observer** <br />
        Classes dealing with events register their event-handler method at the EventManager. 
        Once the event occurs the EventManagers notifies all methods handling with the specific event.
        Following this Strategy the event-logic is mostly encapsulated inside the EventManager class and only the
        methods handling with the event are defined outside providing also a separation of concerns in this area. <br />
    <br />
* **Save game statistics and replay data in a sqlite3 database** <br />
    During the game the step data and food positions are saved inside two numpy arrays ensuring performance.
    Afterwards the whole arrays are combined in an BLOB and loaded inside the database with the remaining game stats.
    To replay a game the game-steps are executed on the playable 'Replay' and when the snake eats the index of the
    food position array is incremented. <br />
<br />
* **Good communication and project planing with GitHub Projects** <br />
    To try out GitHub projects and have a fast overview of the current state of the project we implemented a GitHub-Projects
    page seperated into different task stages. <br />
    Snapshot of the Kanban Board: [GitHub Projects page](assets/images/github_projects_snapshot.png)

## Install
1. Install Prerequisites into a virtual environment
   Makefile:
   ```shell
   make venv
   ```
   Full command:
   ```shell
   python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   ```
2. Install Modules from requirements.txt
   ```shell
   make install
   ```
3. Start the game
   ```shell
   make run
   ```

<br />

![Static Badge](https://img.shields.io/badge/Author-Luis_Gerlinger-blue)
![Static Badge](https://img.shields.io/badge/Author-Jakob_Neft-green)

   
