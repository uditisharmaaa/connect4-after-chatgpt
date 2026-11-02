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
    
    # Print board
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_column_input(player_checker):
    column = input("Player " + player_checker + ", please enter a column: ")
    return column

def is_valid_input(column, board):
    if len(column) != 1:
        return False
    
    if not column.isalpha():
        return False
    
    column = column.upper()
    col_index = ord(column) - 65
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column, checker):
    column = column.upper()
    col_index = ord(column) - 65
    
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
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

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

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
        
        valid_move = False
        while not valid_move:
            column = get_column_input(current_checker)
            
            if is_valid_input(column, board):
                place_checker(board, column, current_checker)
                valid_move = True
            else:
                print("Invalid input. Try again.")
        
        print_board(board)
        
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
