# Minesweeper

  This is a recreation of the well-known Microsoft Minesweeper game from the 90s. All the gameplay features available in the original version are possible in this Pygame recreation; flags can be placed, the chording mechanic can be performed, and the game ends when a mine is hit or all non-mine cells are clicked. The game also tracks a player's time taken to complete the board, prompting users to beat their personal bests!

   I aimed to practice and garner a deeper understanding of Python so, design-wise, it is minimalistic. The exception to this is the usage of custom fonts, and that of images of a mine and of a flag. All of these were directed towards a faithful and appropriately ambienced recreation of the original game; mine-sweeper font for the numbers in the board, Seven Segment for the mine counter, and the mine and flag images for the mines and the flags, coming directly from Microsoft's Minesweeper.

  ## project.py

  Handles all the logic required for the game to occur.

  1. A Pygame window is initialized with a "play" button.
  2. Click input is checked for player pressing play button.
  3. 10 mines are generated randomly using Python's random library, placed in random cells in a 9x9 board.
  4. A mine counter is displayed, showing the user how many mines are left, starting from 10.
  5. The game runs normally. If a mine is clicked, either directly or by chording, the game ends and a game over screen is displayed, along with the number of cells that the player safely uncovered. If a cell is right-clicked, and it is not uncovered, a flag can be placed and removed. If a player uncovers all of the safe mines, a win screen is displayed along with the time taken to complete the game, using Python's time library.

  ## test_project.py

  This file handles the testing for all the functions that return values; get_cell, get_size, and win_condition.


  ## Sources

  Gezoda. (2018, March). MINE-SWEEPER. Fontstruct. https://fontstruct.com/fontstructions/show/1501665/mine-sweeper
  
  Krafti Lab. (2018, July). Seven Segment. Dafont.com. https://www.dafont.com/seven-segment.font
  
  Johnson, C. (1990). Minesweeper (Online Version) [Video Game]. Microsoft.
