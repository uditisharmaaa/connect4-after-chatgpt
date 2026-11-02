import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    column_labels = '  '.join([chr(i) for i in range(ord('A'), ord('A') + COLUMNS)])
    print(f"  {column_labels}")
    print('+---' * COLUMNS + '+')
    for row in board:
        print("| " + " | ".join(row) + " |")
        print('+---' * COLUMNS + '+')

def get_column_choice():
    while True:
        choice = input("Please enter a column (A-G): ").strip().upper()
        if len(choice) == 1 and 'A' <= choice <= chr(ord('A') + COLUMNS - 1):
            return ord(choice) - ord('A')
        print("Invalid input. Try again.")

def place_checker(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False

def check_for_win(board, player_symbol):
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == player_symbol for cell in row[col:col + 4]):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Diagonal checks (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Diagonal checks (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    print_board(board)

    num_players = 2  # Can be set from 2 to MAX_PLAYERS
    player_symbols = PLAYERS_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    while True:
        current_symbol = player_symbols[current_player_index]
        print_board(board)
        print(f"Player {current_symbol}, please enter a column:")
        
        column = get_column_choice()
        
        if not place_checker(board, column, current_symbol):
            print("Column is full, turn skipped.")
        else:
            if check_for_win(board, current_symbol):
                print_board(board)
                print(f"Player {current_symbol} won!")
                break
            elif check_for_draw(board):
                print_board(board)
                print("Game is a draw!")
                break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
