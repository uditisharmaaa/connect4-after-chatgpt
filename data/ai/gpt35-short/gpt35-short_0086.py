import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("+" + "-+"*COLS)

def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2 to {len(PLAYERS)}): "))
            if 2 <= count <= len(PLAYERS):
                return count
            else:
                print("Invalid number of players.")
        except ValueError:
            print("Enter a number.")

def get_move(player):
    while True:
        move = input(f"Player {player}, select column (A-G): ").upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid column. Please choose A to G.")

def make_move(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False  # column full

def is_winner(board, player):
    # Check horizontally
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # Check vertically
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = PLAYERS[:player_count]
    board = create_board()

    current_index = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        player = players[current_index]
        col = get_move(player)

        if not make_move(board, col, player):
            print("Column full! Try again.")
            input("Press Enter to continue...")
            continue

        if is_winner(board, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_index = (current_index + 1) % player_count

if __name__ == "__main__":
    main()
