import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this to 3, 4, or 5 for more players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_str):
    return len(input_str) == 1 and 'A' <= input_str <= chr(65 + COLUMNS - 1)

def get_next_open_row(board, col_index):
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            return row_index
    return None

def place_checker(board, col_index, player_symbol):
    row_index = get_next_open_row(board, col_index)
    if row_index is not None:
        board[row_index][col_index] = player_symbol
    return row_index

def check_winner(board, player_symbol):
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True
    
    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    
    # Check positively sloped diagonals for win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Check negatively sloped diagonals for win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def main():
    board = create_board(ROWS, COLUMNS)
    print_board(board)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        current_player_symbol = PLAYER_SYMBOLS[current_player_index]
        print(f"Player {current_player_symbol}, please enter a column:")
        
        user_input = input().strip().upper()
        
        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(user_input) - 65
        if get_next_open_row(board, col_index) is None:
            print("Column is full. You lose your turn.")
        else:
            place_checker(board, col_index, current_player_symbol)
            print_board(board)
            
            if check_winner(board, current_player_symbol):
                print(f"Player {current_player_symbol} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
