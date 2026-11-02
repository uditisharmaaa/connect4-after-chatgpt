import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    
    # Print column letters
    print("  ", end="")
    for i in range(NUM_COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("| ", end="")
        for j in range(NUM_COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * NUM_COLS + "+")

def drop_checker(board, col, checker):
    for i in range(NUM_ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    
    # Check vertical
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    
    # Check diagonal (down-right)
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    
    # Check diagonal (down-left)
    for i in range(NUM_ROWS - 3):
        for j in range(3, NUM_COLS):
            if board[i][j] == checker and board[i+1][j-1] == checker and board[i+2][j-2] == checker and board[i+3][j-3] == checker:
                return True
    
    return False

def check_draw(board):
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            if board[i][j] == " ":
                return False
    return True

def get_player_input(board, player_checker):
    while True:
        print("Player " + player_checker + ", please enter a column: ", end="")
        user_input = input()
        
        if len(user_input) != 1:
            continue
        
        if not user_input.isupper() or not user_input.isalpha():
            continue
        
        col_num = ord(user_input) - 65
        
        if col_num < 0 or col_num >= NUM_COLS:
            continue
        
        if board[0][col_num] != " ":
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
        
        col = get_player_input(board, checker)
        drop_checker(board, col, checker)
        
        print_board(board)
        
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
