import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    column_labels = " ".join(chr(i) for i in range(ord('A'), ord('A') + len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def select_random_player(players):
    return random.choice(players)

def get_valid_input():
    while True:
        player_input = input().strip().upper()
        if len(player_input) == 1 and 'A' <= player_input <= chr(ord('A') + COLUMNS - 1):
            return player_input
        print("Invalid input. Please enter a valid column:")

def is_valid_move(board, column_index):
    return board[0][column_index] == " "

def make_move(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_for_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(cell != " " for cell in board[0])

def play_connect_4():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS
    current_player = select_random_player(players)
    print_board(board)
    print(f"Player {current_player}, please enter a column:")
    
    while True:
        column_letter = get_valid_input()
        column_index = ord(column_letter) - ord('A')
        
        if is_valid_move(board, column_index):
            make_move(board, column_index, current_player)
            print_board(board)
            
            if check_for_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_for_draw(board):
                print("The game is a draw!")
                break
            
            current_player = players[(players.index(current_player) + 1) % MAX_PLAYERS]
        else:
            print(f"Column full, Player {current_player} loses turn.")
        
        print(f"Player {current_player}, please enter a column:")

if __name__ == "__main__":
    play_connect_4()
