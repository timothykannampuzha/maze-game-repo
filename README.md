# Python Maze and Raiders of lost gems!

"Python Maze and Raiders of lost gems" is an exciting adventure game where you step into the shoes of a gem-hunting hero trapped inside a twisting 2D labyrinth. Your mission? Dodge smart enemies, outwit deadly traps, and collect shimmering treasures hidden deep within the maze walls. With every gem you grab, the stakes get higher and your score increases. Can you escape with all the gems and live to tell the tale, or will the maze claim you forever? Gear up, press play, and let the raid begin! 🏆💎🌀

# How to launch the game in your computer

1. Download the repository as a .zip file:
    * Find the green "Code" button on the repository's main page. 
    * Click on the "Code" button and then select "Download ZIP" from the dropdown menu.  
2. Extract the .zip file:
    * Locate the downloaded .zip file on your computer. 
    * Right-click on the .zip file and choose an option like "Extract All..." or "Extract Here" (the exact wording may vary depending on your operating system). 
    * Choose a location to extract the files, such as your Desktop or a dedicated folder for games.  
3.  Run the .exe file:
    * Once the .zip file is extracted, navigate to the extracted folder. 
    * Look for a file with the .exe extension, which is usually the game's executable file. 
    * Double-click the .exe file to launch the game.  


# Pseudocode for Python Maze and Raiders of lost gems

1. Import required modules: turtle, pygame, random, math, etc.
2. Initialize Pygame for sound and load sound effects.
3. Register custom images for the hero, enemies, gems, and walls.
4. Create the game screen and set title, size, background.
5. Define Wall, Hero, Gem, and Opponent classes with movement, collision, and appearance logic.
6. Create level map using characters (X, P, T, G, E) to design the maze.
7. Set up maze by placing walls, the player, gems, and enemies on screen based on the map.
8. Track walls, treasures, and enemies using lists.
9. Display HUD to show the number of gems collected.
10. Check for gem collisions — if collected, increase score, play sound, and update HUD.
11. Check for win condition — if all gems collected, show win message and end game.
12. Check for enemy collision — if touched by an enemy, play game-over sound and end game.
13. Move enemies toward the hero using shortest distance logic.
14. Detect key presses for movement (WASD and arrow keys).
15. Continuously move the hero if keys are held down.
16. Use timers to loop the game logic and enemy movement every few milliseconds.
17. Display win or loss messages at the center of the screen.
18. Stop movement and actions if game is over.
19. Run the main game loop to update screen, check collisions, and animate.
20. Finish game when player wins or loses; show final score in the console.


# Flow chart for Python Maze and Raider of lost gems
![Flow Chart - Maze Game](https://github.com/user-attachments/assets/995058f0-7bb7-479f-b99e-42e3b2e0adbc)



