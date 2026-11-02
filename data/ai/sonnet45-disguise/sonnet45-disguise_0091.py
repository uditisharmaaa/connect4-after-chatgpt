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
        letter = chr(65 + i)
        print(letter + "   ", end="")
    print()
    
    # Print each row
    for row in board:
        print("+---" * COLS + "+")
        print("| ", end="")
        for cell in row:
            print(cell + " | ", end="")
        print()
    print("+---" * COLS + "+")

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == checker and board[row+1][col-1] == checker and board[row+2][col-2] == checker and board[row+3][col-3] == checker:
                return True
    
    return False

def is_board_full(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_valid_input():
    while True:
        user_input = input()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter: ", end="")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter: ", end="")
            continue
        
        user_input = user_input.upper()
        col_num = ord(user_input) - 65
        
        if col_num < 0 or col_num >= COLS:
            print("Invalid input. Please enter a valid column: ", end="")
            continue
        
        return col_num

def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = players[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        col = get_valid_input()
        
        success = drop_checker(board, col, checker)
        
        if not success:
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
