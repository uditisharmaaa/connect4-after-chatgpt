import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A','B','C','D','E','F','G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    # Create a board full of spaces.
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Print each row
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_player_count():
    while True:
        try:
            num = int(input("Enter number of players (2-5): "))
            if 2 <= num <= 5:
                return num
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Enter an integer between 2 and 5.")

def choose_starting_player(num_players):
    # Randomly choose a player index from players
    return random.randint(0, num_players - 1)

def column_to_index(col_char):
    col_char = col_char.upper()
    if col_char in COLUMN_LABELS:
        return COLUMN_LABELS.index(col_char)
    else:
        return -1

def is_valid_move(board, col):
    # Check if column has space
    return board[0][col] == ' '

def drop_token(board, col, token):
    # Drop token from bottom up
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col  # Return last move position
    # Should never reach here if is_valid_move is checked prior
    return None, None

def check_win(board, row, col, token):
    # Check horizontally, vertically, and two diagonals for 4 in a row

    def count_in_direction(r_step, c_step):
        count = 1  # Count the placed token itself
        # Check in the positive direction
        r, c = row + r_step, col + c_step
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += r_step
            c += c_step
        # Check in the negative direction
        r, c = row - r_step, col - c_step
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= r_step
            c -= c_step
        return count

    # Horizontal
    if count_in_direction(0, 1) >= 4:
        return True
    # Vertical
    if count_in_direction(1, 0) >= 4:
        return True
    # Diagonal /
    if count_in_direction(1, -1) >= 4:
        return True
    # Diagonal \
    if count_in_direction(1, 1) >= 4:
        return True

    return False

def check_draw(board):
    # Board is full if top row has no spaces
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")

    num_players = get_player_count()
    players = PLAYER_TOKENS[:num_players]

    board = create_board()
    current_player_index = choose_starting_player(num_players)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")

        # Get player input and validate
        while True:
            move = input(f"Choose a column ({', '.join(COLUMN_LABELS)}): ").strip()
            col = column_to_index(move)
            if col == -1:
                print("Invalid column. Try again.")
                continue
            if not is_valid_move(board, col):
                print("Column is full. Try a different column.")
                continue
            break

        # Drop token
        row, col = drop_token(board, col, players[current_player_index])

        # Check for win
        if check_win(board, row, col, players[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_index]} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
