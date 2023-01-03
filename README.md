# Othello-py


Implementation of the minimax algorithm with alpha-beta pruning for an Othello (Reversi) game. 
The minimax algorithm is a decision-making strategy used in two-player games (such as Othello, chess, tic-tac-toe, etc.) to determine the best move. 
The algorithm considers all possible moves and the resulting board positions, and then chooses the move that maximizes the score if it is the current player's turn, 
or minimizes the score if it is the opponent's turn.

Alpha-beta pruning is a technique used to improve the efficiency of the minimax algorithm by eliminating certain branches of the search tree. 
This is done by keeping track of two values, alpha and beta, which represent the minimum and maximum scores that the current player is assured of. 
If, at any point during the search, the value of alpha becomes greater than the value of beta, 
the search can be stopped because the current player can do no better than the minimum score (alpha) and 
the opponent can do no worse than the maximum score (beta). This allows the search to be terminated early, reducing the number of nodes that need to 
be evaluated and improving the performance of the algorithm.

Website used for testing: https://playingcards.io/s9n8zf

Pyautogui will read the board and returnd the actuall spots for each player and the code will calculate the best move for the selected player in this case it is "W".

![image](https://user-images.githubusercontent.com/76017518/210290595-2f5301aa-ae10-4b6d-bf5d-dda0aaa3d7fb.png)
