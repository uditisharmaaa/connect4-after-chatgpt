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
        print("| ", end="")
        for cell in row:
            print(cell + " | ", end="")
        print()
    print("+---" * COLS + "+")

def drop_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
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

def get_player_move(board, player_checker):
    while True:
        move = input("Player " + player_checker + ", please enter a column: ")
        
        # Check if input is valid
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        move = move.upper()
        col_num = ord(move) - 65
        
        if col_num < 0 or col_num >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(64 + COLS) + ".")
            continue
        
        # Check if column is full
        if board[0][col_num] != " ":
            print("Column is full. You lose your turn.")
            return -1
        
        return col_num

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
            drop_checker(board, col, player_checker)
        
        print_board(board)
        
        if col != -1 and check_win(board, player_checker):
            print("Player " + player_checker + " won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
