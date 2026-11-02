import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this to the desired number of players (2 to 5)

def clear_screen():
    os.system('clear')  # Use 'cls' on Windows

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))  # Column headers (A, B, C...)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(column, board):
    return column.isalpha() and len(column) == 1 and 0 <= (ord(column.upper()) - 65) < COLS and board[0][ord(column.upper()) - 65] == " "

def get_column_index(column):
    return ord(column.upper()) - 65

def drop_checker(column_index, board, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return row, column_index

def is_winner(board, player):
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonally (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Initialize game
    board = create_board(ROWS, COLS)
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")
        column = input("Please enter a column: ").strip()

        if is_valid_column(column, board):
            col_index = get_column_index(column)
            drop_checker(col_index, board, players[current_player_index])

            # Check for win or draw
            if is_winner(board, players[current_player_index]):
                clear_screen()
                print_board(board)
                print(f"Player {players[current_player_index]} won!")
                game_over = True
            elif is_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Switch to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
