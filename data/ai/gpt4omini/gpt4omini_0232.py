import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can change this for more players (e.g., ['X', 'O', 'V', 'H', 'M'])

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def is_valid_input(col_input):
    return col_input in [chr(65 + i) for i in range(COLS)]

def get_column_index(col_input):
    return ord(col_input) - 65

def place_checker(board, col, checker):
    for row in reversed(board):  # Start from the bottom row
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    # Check horizontally
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertically
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonally (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonally (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    turn_count = 0

    while True:
        print_board(board)
        
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")

        while True:
            col_input = input().upper()
            if is_valid_input(col_input):
                col_index = get_column_index(col_input)
                if place_checker(board, col_index, current_player):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a valid column (A-G).")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        turn_count += 1
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
