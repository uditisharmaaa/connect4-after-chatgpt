import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(NUM_COLS))
    print(column_labels)
    print("+" + "---+" * NUM_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * NUM_COLS)

def get_valid_input(board):
    while True:
        column = input("Please enter a column: ").upper()
        if len(column) != 1 or not ('A' <= column <= chr(65 + NUM_COLS - 1)):
            print("Invalid column. Please enter a letter between A and", chr(65 + NUM_COLS - 1))
            continue
        col_index = ord(column) - 65
        if board[0][col_index] != " ":
            print("Column is full. Choose another column.")
            continue
        return col_index

def drop_checker(board, col, checker):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

def is_winner(board, row, col, checker):
    # Check directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        for step in range(1, 4):  # Forward direction
            r, c = row + dr * step, col + dc * step
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                count += 1
            else:
                break

        for step in range(1, 4):  # Backward direction
            r, c = row - dr * step, col - dc * step
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                count += 1
            else:
                break

        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(NUM_COLS))

def main():
    # Initialize game
    board = initialize_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player]} starts the game!")

    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn")
        col = get_valid_input(board)
        row, col = drop_checker(board, col, players[current_player])

        if is_winner(board, row, col, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
