import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(i + 65) for i in range(len(board[0])))
    print(column_labels)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * len(board[0]))

def get_valid_column_input(board):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Enter a single valid column letter.")
            continue
        column_index = ord(user_input) - 65
        if column_index < 0 or column_index >= len(board[0]):
            print("Invalid column. Please try again.")
            continue
        if board[0][column_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        return column_index

def place_checker(board, column, symbol):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return row

def check_winner(board, last_row, last_col, symbol):
    def check_direction(delta_row, delta_col):
        count = 1
        for dr, dc in [(-delta_row, -delta_col), (delta_row, delta_col)]:
            r, c = last_row + dr, last_col + dc
            while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
                count += 1
                if count == 4:
                    return True
                r += dr
                c += dc
        return False
    
    # Check all four directions
    return (
        check_direction(0, 1) or  # Horizontal
        check_direction(1, 0) or  # Vertical
        check_direction(1, 1) or  # Diagonal (\)
        check_direction(1, -1)    # Diagonal (/)
    )

def is_board_full(board):
    return all(cell != " " for cell in board[0])

def connect_4_game():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    players = random.sample(PLAYER_SYMBOLS[:MAX_PLAYERS], 2)
    current_player = 0

    print_board(board)
    print(f"Randomly selected players: {', '.join(players)}")
    print(f"Player {players[current_player]} starts!\n")

    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn.")
        column = get_valid_column_input(board)
        row = place_checker(board, column, players[current_player])

        # Check for win
        if check_winner(board, row, column, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("Game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % len(players)

# Main entry point
if __name__ == "__main__":
    connect_4_game()
