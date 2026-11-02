import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # You can modify this list as per the number of players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  A B C D E F G")
    for row in board:
        print("|" + "|".join(row) + "|")
    print(" " + "-" * (2 * COLUMNS - 1))

def get_player_choice(current_player):
    while True:
        choice = input(f"Player {PLAYER_SYMBOLS[current_player]}, choose a column (A-G): ").strip().upper()
        if choice in 'ABCDEFG' and len(choice) == 1:
            return ord(choice) - ord('A')  # Convert 'A'-'G' to 0-6
        print("Invalid input. Please choose a column between A-G.")

def make_move(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = PLAYER_SYMBOLS[player]
            return True
    return False

def is_winner(board, player):
    symbol = PLAYER_SYMBOLS[player]

    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Positive diagonal check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Negative diagonal check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    num_players = len(PLAYER_SYMBOLS)
    current_player = random.randint(0, num_players - 1)

    while True:
        print_board(board)
        column = get_player_choice(current_player)

        if not make_move(board, column, current_player):
            print(f"Column {chr(column + ord('A'))} is full. Try another column.")
            continue

        if is_winner(board, current_player):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
