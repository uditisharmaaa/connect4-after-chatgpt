import os
import random

# Constants for the board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Maximum of 5 players

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column(player):
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:
            return ord(column) - 65
        else:
            print("Invalid input. Please enter a valid column (A-G).")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
            
    # Check vertical win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
            
    # Check diagonal win (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            
    # Check diagonal win (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    total_players = len(PLAYERS)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]

        column = get_valid_column(current_player)

        if not place_checker(board, column, current_player):
            print("Column is full. Try again.")
            continue

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % total_players

if __name__ == "__main__":
    main()
