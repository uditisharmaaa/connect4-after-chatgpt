import os
import random

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
    
    # print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def get_checker(player_num):
    checkers = ["X", "O", "V", "H", "M"]
    return checkers[player_num]

def drop_checker(board, col, checker):
    # find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
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
    
    # check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    
    # check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    
    return False

def check_draw(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def get_player_input(current_player):
    checker = get_checker(current_player)
    user_input = input("Player " + checker + ", please enter a column: ")
    return user_input

def validate_input(user_input):
    if len(user_input) != 1:
        return False
    if user_input < 'A' or user_input > chr(64 + COLS):
        return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        checker = get_checker(current_player)
        
        valid_move = False
        while not valid_move:
            user_input = get_player_input(current_player)
            
            if not validate_input(user_input):
                print("Invalid input. Please try again.")
                continue
            
            col = ord(user_input) - 65
            
            if drop_checker(board, col, checker):
                valid_move = True
            else:
                print("Column is full. You lose your turn.")
                valid_move = True
        
        print_board(board)
        
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

main()
