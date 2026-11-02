import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '-+' * COLS)

def valid_column_input(col_choice, board):
    col_choice = col_choice.upper()
    if col_choice not in COLUMN_LABELS:
        return False
    col_index = COLUMN_LABELS.index(col_choice)
    # Check if top cell in the column is empty (means column not full)
    return board[0][col_index] == ' '

def get_next_open_row(board, col):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def check_win(board, piece):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def get_player_count():
    while True:
        try:
            count = int(input("Enter number of players (2 - 5): "))
            if 2 <= count <= 5:
                return count
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_player_move(player):
    while True:
        move = input(f"Player {player}, select a column (A-G): ").strip()
        if len(move) == 1 and move.upper() in COLUMN_LABELS:
            return move.upper()
        print("Invalid input. Please enter a column letter A through G.")

def main():
    player_count = get_player_count()
    players = PLAYERS[:player_count]
    board = create_board()
    current_player_index = random.randint(0, player_count -1)

    while True:
        print_board(board)
        current_player = players[current_player_index]
        
        # Ask for valid move
        col_letter = get_player_move(current_player)
        col = COLUMN_LABELS.index(col_letter)

        # Check if column not full
        if not valid_column_input(col_letter, board):
            print(f"Column {col_letter} is full, try another one.")
            continue

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_player)

        # Check wins
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        # Check draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player turn
        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    main()
