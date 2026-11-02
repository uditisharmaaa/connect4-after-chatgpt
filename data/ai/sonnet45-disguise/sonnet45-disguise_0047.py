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
    
    # print board
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_valid_input(board, player):
    while True:
        col_input = input("Player " + player + ", please enter a column: ")
        
        if len(col_input) != 1:
            print("Invalid input. Try again.")
            continue
        
        if col_input < 'A' or col_input > chr(65 + COLS - 1):
            print("Invalid input. Try again.")
            continue
        
        col = ord(col_input) - 65
        
        if board[0][col] != " ":
            print("Column is full. You lose your turn.")
            return -1
        
        return col

def place_checker(board, col, player):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = player
            return i
    return -1

def check_win(board, player):
    # horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                return True
    
    # vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                return True
    
    # diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == player and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player:
                return True
    
    # diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == player and board[i+1][j-1] == player and board[i+2][j-2] == player and board[i+3][j-3] == player:
                return True
    
    return False

def check_draw(board):
    for i in range(COLS):
        if board[0][i] == " ":
            return False
    return True

def main():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        player = players[current_player]
        col = get_valid_input(board, player)
        
        if col == -1:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        place_checker(board, col, player)
        print_board(board)
        
        if check_win(board, player):
            print("Player " + player + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

main()
