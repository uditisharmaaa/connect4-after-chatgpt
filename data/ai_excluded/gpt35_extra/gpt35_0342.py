import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players as per assignment
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = '  '
    for col in range(COLUMNS):
        header += chr(ord('A') + col) + '   '
    print(header)
    
    # Print board rows
    for r in range(ROWS):
        print('+' + '---+' * COLUMNS)
        row_str = '|'
        for c in range(COLUMNS):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
    print('+' + '---+' * COLUMNS)

def get_valid_column_input(player_checker):
    valid_columns = [chr(ord('A') + i) for i in range(COLUMNS)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # Invalid length input
            continue
        if col_input not in valid_columns:
            continue
        return col_input

def place_checker(board, col_char, player_checker):
    col_index = ord(col_char) - ord('A')
    # Place checker in the lowest available row on this column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player_checker
            return True  # Successful placement
    return False  # Column full

def check_win(board, player_checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal down-right
    for r in range(ROWS - WIN_CONDITION + 1):
        for c in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal up-right
    for r in range(WIN_CONDITION - 1, ROWS):
        for c in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]  # Use appropriate number of players/checkers
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_index]
        col_char = get_valid_column_input(player_checker)
        placed = place_checker(board, col_char, player_checker)

        if not placed:  # Column full, player loses turn
            # According to assignment: no re-try, turn lost if column full
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
