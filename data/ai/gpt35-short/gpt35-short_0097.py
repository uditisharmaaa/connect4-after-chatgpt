import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Available player symbols

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))  # bottom border

def get_player_count():
    while True:
        count = input("Enter number of players (2-5): ")
        if count.isdigit():
            count = int(count)
            if 2 <= count <= 5:
                return count
        print("Invalid input. Please enter a number between 2 and 5.")

def get_valid_column(board):
    while True:
        col_input = input("Choose a column (A-G): ").upper()
        if col_input in COL_LABELS:
            col = COL_LABELS.index(col_input)
            # Check if the column is not full
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full. Try another one.")
        else:
            print("Invalid column. Please enter a letter from A to G.")

def make_move(board, col, player):
    # Place the player's symbol in the lowest empty row in the column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = PLAYERS[:player_count]
    # Choose random first player
    current_player_index = random.randint(0, player_count -1)
    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn")
        col = get_valid_column(board)
        row, col = make_move(board, col, players[current_player_index])

        if check_win(board, players[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_index]} wins! Congratulations!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    main()
