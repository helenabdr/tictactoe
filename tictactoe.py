"""
Tic Tac Toe Player
"""

"""
https://towardsdatascience.com/tic-tac-toe-creating-unbeatable-ai-with-minimax-algorithm-8af9e52c1e7d

https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
"""

#to do 
#Alpha-beta pruning

import math
import copy
import random
import numpy as np

X = "X"
O = "O"
EMPTY = None
current_player = O
aux = False

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    global current_player, X, O
    occurrence_X = []
    occurrence_O = []
    
    #Stored in a list how many occurrences of every player there are in board.
    for i in board:
        occurrence_X.append(i.count(X))
        occurrence_O.append(i.count(O))

    if current_player == X and (np.sum(occurrence_X) == np.sum(occurrence_O) + 1):
        current_player = O
    elif current_player == O and (np.sum(occurrence_X) == np.sum(occurrence_O)):
        current_player = X
    else:
        pass
    
    return current_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    list_actions = []
    
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                list_actions.insert(0, (i,j)) #stack
                print(list_actions)
            else:
                pass
                #print("Occupied cell!")
    
    return list_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    board_state = copy.deepcopy(board)

    i = action[0]
    j = action[1]

    try: 
        if(i<3 and j<3):
            if board_state[i][j] == EMPTY:
                board_state[i][j] = player(board)
            elif board_state[i][j] != EMPTY:
                board_state[i][j] = EMPTY
            else:
                pass
    except:
        print('Invalid position!')
        raise

    return board_state

def winner(board):
    """
    Returns the winner of the game, if there is one.
    
    Returns None, if game is in progress or ended in a tie.
    """
    win = EMPTY
    

    #horizontal
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != EMPTY:
            if row[0] == X:
                win = X
            else:
                win = O
    
    #vertical
    for column in range(len(board)):
        check = []
        for row in board:
            check.append(row[column])
        if check.count(check[0]) == len(check) and check[0] != EMPTY:
            if check[0] == X:
                win = X
            else:
                win = O
                
    #main diagonal
    check = []         
    for row, column in zip(board, range(len(board))):
        check.append(row[column])
    if check.count(check[0]) == len(check) and check[0] != EMPTY:
        if check[0] == X:
            win = X
        else:
            win = O
    
    #reverse diagonal
    check = []
    for row, column in zip(board, reversed(range(len(board)))):
        check.append(row[column])
    if check.count(check[0]) == len(check) and check[0] != EMPTY:
        if check[0] == X:
            win = X
        else:
            win = O
        
    return win

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if (winner(board) != EMPTY):
        return True
    else:
        if tie(board):
            return True
        else:
            #print("In progress!")
            return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        score = 1
    elif winner(board) == O:
        score = -1
    else:
        score = 0
            
    return score

# def minimax(board):

#     best_move = (None, None)

#     if terminal(board):
#         score = utility(board)
#         return (score, best_move)

#     #MAXimazing: X
#     if player(board) == X:
#         best_score = -math.inf

#         list_actions = actions(board)
#         for action in list_actions:
#             board = result(board, action)
#             print(board)
#             score = minimax(board)[0]
#             board = result(board, action)

#             best_score = max(score, best_score)
#             if(score >= best_score):
#                 best_score = score
#                 best_move = action
            
#     #MINimazing: O 
#     elif (player(board) == O):
#         best_score = math.inf
        
#         list_actions = actions(board)
#         for action in list_actions:
#             board = result(board, action)
#             print(board)
#             score = minimax(board)[0]
#             board = result(board, action)

#             best_score = min(score, best_score)
#             if(score <= best_score):
#                 best_score = score
#                 best_move = action

#     return (best_score, best_move)

def minimax(board):

    """
        Returns the best move for AI
    """

    if player(board) == X:
        return maximize(board)[1]

    elif player(board) == O:
        return minimize(board)[1] 

#MAXimizing: X
def maximize(board):

    best_score = -math.inf
    best_move = (None, None)
    if terminal(board):
        score = utility(board)
        return (score, best_move)

    list_actions = actions(board)
    for action in list_actions:
        board = result(board, action)
        score = minimize(board)[0]
        board = result(board, action) #Clear de board

        best_score = max(score, best_score)
        if(score >= best_score):
            best_score = score
            best_move = action
    
    return (best_score, best_move)

#MINimizing: O
def minimize(board):
        
    best_score = math.inf
    best_move = (None, None)

    if terminal(board):
        score = utility(board)
        return (score, best_move)
        
    list_actions = actions(board)
    for action in list_actions:
        board = result(board, action)
        score = maximize(board)[0]
        board = result(board, action)
        best_score = min(score, best_score)
        if(score <= best_score):
            best_score = score
            best_move = action

    return (best_score, best_move)

def tie(board):
    """
    Returns if board's state resulting in a draw
    """
    
    tie_row_one = all(i != EMPTY for i in board[0])
    tie_row_two = all(i != EMPTY for i in board[1])
    tie_row_three = all(i != EMPTY for i in board[2])
        
    if tie_row_one and tie_row_two and tie_row_three:
        return True
    else:
        pass
    