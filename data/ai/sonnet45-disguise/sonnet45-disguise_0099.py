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
        print(chr(65 + i) + "   ", end="")
    print()
    
    # print rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
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
    # check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    
    # check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    
    # check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    # check diagonal down-left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == checker and board[row+1][col-1] == checker and board[row+2][col-2] == checker and board[row+3][col-3] == checker:
                return True
    
    return False

def check_draw(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    while True:
        move = input("Player " + player_checker + ", please enter a column: ")
        
        if len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        move = move.upper()
        col = ord(move) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Please enter a valid column.")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def main():
    board = create_board()
    
    # pick random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    # game loop
    while True:
        checker = CHECKERS[current_player]
        
        col = get_player_move(board, checker)
        
        place_checker(board, col, checker)
        print_board(board)
        
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

main()
