import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    
    # print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i), end="   ")
    print()
    
    # print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def drop_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return True
    return False

def check_win(board, checker):
    # check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    
    # check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    
    # check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    
    # check diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == checker and board[i+1][j-1] == checker and board[i+2][j-2] == checker and board[i+3][j-3] == checker:
                return True
    
    return False

def is_board_full(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def get_column_input():
    col_input = input()
    return col_input

def validate_input(col_input):
    if len(col_input) != 1:
        return False
    if col_input < 'A' or col_input > chr(65 + COLS - 1):
        return False
    return True

def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        current_checker = players[current_player_idx]
        print("Player " + current_checker + ", please enter a column:")
        
        valid_move = False
        while not valid_move:
            col_input = get_column_input()
            
            if not validate_input(col_input):
                print("Invalid input. Please enter a valid column letter:")
                continue
            
            col_num = ord(col_input) - 65
            
            if drop_checker(board, col_num, current_checker):
                valid_move = True
            else:
                print("Column is full. You lose your turn.")
                valid_move = True
        
        print_board(board)
        
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

play_game()
