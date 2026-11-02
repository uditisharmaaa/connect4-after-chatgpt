import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]  # Allows up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(chr(i) for i in range(ord('A'), ord('A') + COLUMNS)))
    print('+' + '---+' * COLUMNS)
    
    # Print rows
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def is_valid_input(column):
    return column.isalpha() and 'A' <= column < chr(ord('A') + COLUMNS)

def get_column_index(column):
    return ord(column) - ord('A')

def is_column_full(board, col_idx):
    return board[0][col_idx] != ' '

def place_checker(board, col_idx, checker):
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return

def is_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
                
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        column = input().strip().upper()

        if not (is_valid_input(column)):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_idx = get_column_index(column)

        if is_column_full(board, col_idx):
            print("Column is full. Please choose another column.")
            continue

        place_checker(board, col_idx, current_checker)
        print_board(board)

        if is_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch players
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
