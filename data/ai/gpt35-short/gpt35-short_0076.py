import os
import random

ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A','B','C','D','E','F','G']
PLAYERS_MARKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print('  ' + ' '.join(COLUMNS_LABELS))
    # Print rows from top (row 0) to bottom (row 5)
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('-' * (2*COLS + 3))

def get_valid_column_input(player_marker):
    while True:
        col_input = input(f"Player {player_marker}, choose a column (A-G): ").upper()
        if col_input in COLUMNS_LABELS:
            col_idx = COLUMNS_LABELS.index(col_input)
            return col_idx
        else:
            print("Invalid input. Please enter a letter A to G corresponding to a column.")

def is_column_full(board, col):
    return board[0][col] != ' '

def drop_piece(board, col, player_marker):
    # Drop piece to the lowest empty row in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_marker
            return row, col
    # Should never reach here if called with valid input
    return None

def check_win(board, row, col, player_marker):
    # Check horizontal, vertical, diagonal up and diagonal down
    
    def count_consecutive(r_step, c_step):
        count = 1
        # Check one direction
        r, c = row + r_step, col + c_step
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_marker:
            count += 1
            r += r_step
            c += c_step
        # Check opposite direction
        r, c = row - r_step, col - c_step
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_marker:
            count += 1
            r -= r_step
            c -= c_step
        return count

    # Horizontal check (0,1)
    if count_consecutive(0,1) >= 4:
        return True
    # Vertical check (1,0)
    if count_consecutive(1,0) >= 4:
        return True
    # Diagonal up (1,1)
    if count_consecutive(1,1) >= 4:
        return True
    # Diagonal down (1,-1)
    if count_consecutive(1,-1) >= 4:
        return True

    return False

def check_draw(board):
    # If top row has no empty space, board is full
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()

    print("Welcome to Connect 4!")
    # Ask number of players (2-5)
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Number of players must be between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

    players = PLAYERS_MARKERS[:num_players]
    # Pick random first player index
    current_player_idx = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)

        player_marker = players[current_player_idx]

        # Get player's move
        col = get_valid_column_input(player_marker)

        # Check if column is full
        if is_column_full(board, col):
            print("That column is full. Please pick another column.")
            input("Press Enter to continue...")
            continue

        # Drop piece
        row, col = drop_piece(board, col, player_marker)

        # Check for win
        if check_win(board, row, col, player_marker):
            clear_screen()
            print_board(board)
            print(f"Player {player_marker} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full and no player has connected four.")
            break

        # Advance to next player
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
