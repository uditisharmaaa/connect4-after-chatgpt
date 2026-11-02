import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print(" Connect 4")
    print("Players: ", " ".join(PLAYERS[:num_players]))
    print("  " + " ".join(COLUMNS_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_valid_column(board):
    while True:
        col = input("Choose a column (A-G): ").upper()
        if col not in COLUMNS_LABELS:
            print("Invalid column. Please choose a letter from A to G.")
            continue
        col_index = COLUMNS_LABELS.index(col)
        if board[0][col_index] != ' ':
            print("Column is full. Choose another one.")
            continue
        return col_index

def drop_piece(board, col, player):
    # Drop piece into the lowest empty spot in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal down-left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    # If top row has no empty spaces, it's a draw
    return all(cell != ' ' for cell in board[0])

def main():
    global num_players
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except:
            print("Invalid input, enter a number between 2 and 5.")

    board = create_board()
    current_player_index = random.randint(0, num_players - 1)

    while True:
        print_board(board)
        player = PLAYERS[current_player_index]
        print(f"Player {player}'s turn.")
        col = get_valid_column(board)
        row, col = drop_piece(board, col, player)

        if check_winner(board, player):
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
