import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

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
    return board[0][col] == " "

def drop_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return i
    return -1

def check_win(board, row, col, checker):
    # Check horizontal
    count = 0
    for j in range(COLS):
        if board[row][j] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for i in range(ROWS):
        if board[i][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    i = start_row
    j = start_col
    while i >= 0 and j < COLS:
        if board[i][j] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        i -= 1
        j += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    i = start_row
    j = start_col
    while i < ROWS and j < COLS:
        if board[i][j] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        i += 1
        j += 1
    
    return False

def check_draw(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def get_player_input(board, player_checker):
    while True:
        player_input = input("Player " + player_checker + ", please enter a column: ")
        
        if len(player_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not player_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        player_input = player_input.upper()
        col = ord(player_input) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(64 + COLS) + ".")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def play_game():
    board = create_board()
    checkers = ["X", "O", "V", "H", "M"]
    players = []
    for i in range(NUM_PLAYERS):
        players.append(checkers[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = players[current_player]
        col = get_player_input(board, checker)
        row = drop_checker(board, col, checker)
        
        print_board(board)
        
        if check_win(board, row, col, checker):
            print("Player " + checker + " won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
