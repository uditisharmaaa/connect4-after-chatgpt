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
        label = chr(65 + i)
        print(label + "   ", end="")
    print()
    
    # print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_input(column, board):
    if len(column) != 1:
        return False
    if not column.isalpha():
        return False
    if not column.isupper():
        return False
    
    col_num = ord(column) - 65
    if col_num < 0 or col_num >= COLS:
        return False
    
    return True

def is_column_full(column, board):
    col_num = ord(column) - 65
    if board[0][col_num] != " ":
        return True
    return False

def place_checker(column, checker, board):
    col_num = ord(column) - 65
    
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_num] == " ":
            board[i][col_num] = checker
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

def check_draw(board):
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == " ":
                return False
    return True

def main():
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
            column = input("Player " + current_checker + ", please enter a column: ")
            
            if not is_valid_input(column, board):
                print("Invalid input. Please try again.")
                continue
            
            if is_column_full(column, board):
                print("Column is full. You lose your turn.")
                break
            
            place_checker(column, current_checker, board)
            valid_move = True
        
        print_board(board)
        
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

main()
