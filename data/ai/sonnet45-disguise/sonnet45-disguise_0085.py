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
    
    # print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_column_input(player):
    column = input("Player " + player + ", please enter a column: ")
    return column

def is_valid_column(column, board):
    if len(column) != 1:
        return False
    if not column.isupper():
        return False
    col_num = ord(column) - 65
    if col_num < 0 or col_num >= COLS:
        return False
    if board[0][col_num] != " ":
        return False
    return True

def place_checker(board, column, checker):
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
    for i in range(COLS):
        if board[0][i] == " ":
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
        current_player = players[current_player_index]
        
        valid_move = False
        while not valid_move:
            column = get_column_input(current_player)
            if is_valid_column(column, board):
                valid_move = True
                place_checker(board, column, current_player)
            else:
                print("Invalid input, try again.")
        
        print_board(board)
        
        if check_win(board, current_player):
            print("Player " + current_player + " won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
