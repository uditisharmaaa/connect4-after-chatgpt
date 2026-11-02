import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')  # Use 'cls' instead of 'clear' on Windows

def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")
    
def is_valid_input(col):
    return col.isalpha() and col.upper() in [chr(65 + i) for i in range(COLS)]

def find_row(board, col_idx):
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            return row_idx
    return -1

def check_winner(board, player):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check horizontally
                if col <= COLS - 4 and all(board[row][col+i] == player for i in range(4)):
                    return True
                # Check vertically
                if row <= ROWS - 4 and all(board[row+i][col] == player for i in range(4)):
                    return True
                # Check diagonally "\"
                if col <= COLS - 4 and row <= ROWS - 4 and all(board[row+i][col+i] == player for i in range(4)):
                    return True
                # Check diagonally "/"
                if col <= COLS - 4 and row >= 3 and all(board[row-i][col+i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    board = init_board()
    current_player_index = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        current_player = CHECKERS[current_player_index]
        
        print(f"Player {current_player}, please enter a column:")
        col_input = input().strip()
        
        if not is_valid_input(col_input):
            print("Invalid input! Please try again.")
            continue
        
        col_idx = ord(col_input.upper()) - 65
        row_idx = find_row(board, col_idx)
        
        if row_idx == -1:
            print("Column full! You lose your turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        
        board[row_idx][col_idx] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS

play_game()
