import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col, board):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != ' ':
        return False
    return True

def place_checker(col, checker, board):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    
    # Check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    
    # Check diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == checker and board[i+1][j-1] == checker and board[i+2][j-2] == checker and board[i+3][j-3] == checker:
                return True
    
    return False

def check_draw(board):
    for j in range(COLS):
        if board[0][j] == ' ':
            return False
    return True

def get_player_input(player_checker):
    while True:
        user_input = input("Player " + player_checker + ", please enter a column: ")
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_letter = user_input.upper()
        col_index = ord(col_letter) - 65
        
        if col_index < 0 or col_index >= COLS:
            print("Invalid column. Please choose a valid column.")
            continue
        
        return col_index

def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        col = get_player_input(current_checker)
        
        if not is_valid_column(col, board):
            print("Column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        place_checker(col, current_checker, board)
        print_board(board)
        
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
