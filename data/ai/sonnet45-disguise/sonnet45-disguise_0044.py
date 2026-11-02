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
    
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
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
        if board[0][j] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    while True:
        print("Player " + player_checker + ", please enter a column: ", end="")
        user_input = input()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_letter = user_input.upper()
        col = ord(col_letter) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Please enter a column between A and " + chr(64 + COLS) + ".")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. You lose your turn.")
            return -1
        
        return col

def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player_checker = players[current_player]
        
        col = get_player_move(board, player_checker)
        
        if col != -1:
            place_checker(board, col, player_checker)
            print_board(board)
            
            if check_win(board, player_checker):
                print("Player " + player_checker + " won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
