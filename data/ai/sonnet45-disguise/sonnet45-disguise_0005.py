import random
import os

# Global constants
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
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_column_input(player):
    col_input = input("Player " + player + ", please enter a column: ")
    return col_input

def is_valid_column(col_input, board):
    if len(col_input) != 1:
        return False
    
    if not col_input.isupper():
        return False
    
    col_num = ord(col_input) - 65
    
    if col_num < 0 or col_num >= COLS:
        return False
    
    if board[0][col_num] != " ":
        return False
    
    return True

def place_checker(board, col_input, player):
    col_num = ord(col_input) - 65
    
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_num] == " ":
            board[i][col_num] = player
            return True
    
    return False

def check_win(board, player):
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                return True
    
    # Check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == player and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player:
                return True
    
    # Check diagonal (down-left)
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
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_player = players[current_player_index]
        
        valid_move = False
        while not valid_move:
            col_input = get_column_input(current_player)
            
            if is_valid_column(col_input, board):
                valid_move = True
                place_checker(board, col_input, current_player)
            else:
                print("Invalid input. Try again.")
        
        print_board(board)
        
        if check_win(board, current_player):
            print("Player " + current_player + " won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

main()
