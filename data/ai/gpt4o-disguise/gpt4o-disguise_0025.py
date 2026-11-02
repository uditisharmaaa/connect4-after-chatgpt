import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ["X", "O"]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the console (works for Unix/Linux)
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def drop_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False

def validate_input(input_str, valid_inputs):
    return input_str in valid_inputs

def check_win(board, symbol):
    # Horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == symbol and row[col + 1] == symbol and row[col + 2] == symbol and row[col + 3] == symbol:
                return True
    
    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == symbol and board[row + 1][col] == symbol and board[row + 2][col] == symbol and board[row + 3][col] == symbol:
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == symbol and board[row + 1][col + 1] == symbol and board[row + 2][col + 2] == symbol and board[row + 3][col + 3] == symbol:
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == symbol and board[row - 1][col + 1] == symbol and board[row - 2][col + 2] == symbol and board[row - 3][col + 3] == symbol:
                return True

    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(PLAYER_SYMBOLS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        player_input = input().strip().upper()
        
        if not validate_input(player_input, COLUMN_LABELS):
            print("Invalid input, try again.")
            continue
        
        column_index = COLUMN_LABELS.index(player_input)
        
        if not drop_checker(board, column_index, current_player):
            print("Column full, you lose your turn!")
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = PLAYER_SYMBOLS[(PLAYER_SYMBOLS.index(current_player) + 1) % len(PLAYER_SYMBOLS)]

if __name__ == "__main__":
    main()
