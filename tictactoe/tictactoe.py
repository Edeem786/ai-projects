"""
Tic Tac Toe Player
"""

import copy
import random

X = "X"
O = "O"
EMPTY = None


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
    not_empty = 0
    for row in board:
        for cell in row:
            if cell != EMPTY:
                not_empty += 1
    
    if not_empty % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_moves.add((i, j))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = copy.deepcopy(board)

    newboard[action[0]][action[1]] = player(board)
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontal win
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    
    # check vertical win
    for column in range(3):
        if board[0][column] ==  board[1][column] == board[2][column] != EMPTY:
            return board[0][column]
        
    # check diagonal win
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[1][1]
    if board[2][0] == board[1][1] == board[0][2] != EMPTY:
        return board[1][1]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = 2
        for action in actions(board):
            v = min(v, max_value(result(board,action)))
    return v

def max_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = -2
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        maxplayer = True
        v = -2
    else:
        maxplayer = False
        v = 2
    for action in (actions(board)):
        if maxplayer:
            min_result = min_value(result(board,action))
            if v < min_result:
                best_move = action
                v = min_result
        else:
            max_result = max_value(result(board, action))
            if v > max_result:
                best_move = action
                v = max_result

    return best_move        
