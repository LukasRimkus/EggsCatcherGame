# Eggs Catcher Game

A mini game which was built using Python and tkinter GUI library. The purpose of the game is to catch as many eggs as possible using a box which is controlled with keyboard (keys can be changes in the settings menu). It was created as a coursework assignment for the introductory course of Python programming, so OOP has not been much used here.

## Some more details

All the keyboard controls are saved in the list 'controls' and in the 'keyboard_buttons.txt' file. The pause can be turned on by default when you press the 'Escape' keyboard button.Also, there is included a 'boss key' which can be activated using the 'b' keyboard button (default).
All the buttons can be changed in the game 'settings' menu.There are three different keyboard combinations for cheats: 1) if you type in 'life', you receive an extra life2) if you type in 'slow', you slow a game a bit (at the beginning of the game the effect can be hardly noticeable; you can type in the codeseveral times to get a stronger effect on the pace of the game)3) 'Control_L+Shift_L+c' decrease the lives by one
As you progress, the game becomes more difficult. But per 20 new points you receive an extra life. The best five players are included in the leaderboard, the results are saved in the 'leaderboards.txt'file.
You can turn off the game even if you have not finished playing, as the game state is saved in the 'save_game_state.txt' file
In some computers the pace of game can be very slow or vice versa (tested that), in this case you would need to edit the value of the 'coefficient_of_falling' in the line 734 which determines the velocity of falling eggs.
Standard screen size is 1536x864.
