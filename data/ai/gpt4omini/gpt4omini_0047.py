import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col_input):
    return col_input in [chr(65 + i) for i in range(COLS)]

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in board:
        if ''.join(row).find(player * 4) != -1:
            return True
    # Check vertical
    for col in range(COLS):
        if ''.join(board[row][col] for row in range(ROWS)).find(player * 4) != -1:
            return True
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    player_count = min(len(PLAYERS), 5)  # Maximum of 5 players
    current_player_index = random.randint(0, player_count - 1)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G): ", end="")
        col_input = input().strip().upper()

        if is_valid_input(col_input):
            column = ord(col_input) - 65
            if not drop_checker(board, column, current_player):
                print("Column is full! Try again.")
                continue
        else:
            print("Invalid input! Please enter a valid column (A-G).")
            continue
        
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    main()
