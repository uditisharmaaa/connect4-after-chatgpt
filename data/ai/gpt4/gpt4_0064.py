import os
import random

# Constants for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    col_headers = "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(f"  {col_headers}")
    print("+---" * len(board[0]) + "+")
    # Print board rows
    for row in board:
        row_content = " | ".join(row)
        print(f"| {row_content} |")
        print("+---" * len(row) + "+")

def is_valid_move(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == " "

def place_checker(board, checker, col):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col+4] == [checker] * 4:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize variables
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Game loop
    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn!")

        # Prompt for user input
        while True:
            try:
                col_letter = input("Please enter a column (A-G): ").strip().upper()
                col = ord(col_letter) - ord('A')
                if not is_valid_move(board, col):
                    raise ValueError("Invalid column or column is full.")
                break
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")

        # Place the checker
        place_checker(board, current_player, col)

        # Check for a winner
        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
