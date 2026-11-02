import os
import random

# Constants for the game
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Possible players

def create_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear')
    print(" " + " ".join(COLUMN_LABELS))  # Print column labels
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (NUM_COLUMNS * 2 + 1))

def drop_piece(board, column, piece):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = piece
            return True
    return False

def is_valid_column(board, column):
    return board[0][column] == ' '

def check_win(board, piece):
    # Check horizontal locations for win
    for c in range(NUM_COLUMNS - 3):
        for r in range(NUM_ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLUMNS - 3):
        for r in range(NUM_ROWS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLUMNS - 3):
        for r in range(3, NUM_ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(NUM_COLUMNS))

def get_column_choice():
    while True:
        column = input(f"Choose a column ({COLUMN_LABELS}): ").upper()
        if len(column) == 1 and column in COLUMN_LABELS:
            return COLUMN_LABELS.index(column)
        print("Invalid input. Try again.")

def main():
    num_players = random.randint(2, 5)
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()
    game_over = False

    while not game_over:
        print_board(board)
        player_piece = players[current_player_index]
        print(f"Player {player_piece}'s turn.")

        column = get_column_choice()

        if is_valid_column(board, column):
            drop_piece(board, column, player_piece)

            if check_win(board, player_piece):
                game_over = True
                print_board(board)
                print(f"Player {player_piece} wins!")
            elif check_draw(board):
                game_over = True
                print_board(board)
                print("The game is a draw!")

            current_player_index = (current_player_index + 1) % num_players
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    main()
