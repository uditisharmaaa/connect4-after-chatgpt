import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Allowed players

def clear_screen():
    os.system('clear')  # Use 'cls' if on Windows

def create_board():
    # Create a board filled with spaces to represent empty slots
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2*COLS + 1))

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

def get_player_move(player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print(f"Invalid column. Please choose a column between A and G.")

def board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def make_move(board, col, symbol):
    # Drop the piece into the lowest available slot in the column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False  # Column is full

def check_winner(board, symbol):
    # Check horizontal, vertical, and two diagonal directions

    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Diagonal (\) check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Diagonal (/) check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {', '.join(players)}")
        print(f"Current turn: Player {players[current_player_idx]}")

        col = get_player_move(players[current_player_idx])
        if not make_move(board, col, players[current_player_idx]):
            print("That column is full. Try another column.")
            input("Press Enter to continue...")
            continue

        if check_winner(board, players[current_player_idx]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_idx]} wins! Congratulations!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

    print("Game over. Thanks for playing!")

if __name__ == "__main__":
    main()
