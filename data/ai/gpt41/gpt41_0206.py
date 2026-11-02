import os
import random

# ------------------------ CONSTANTS ------------------------
ROWS = 6
COLUMNS = 7               # Changeable, up to 26
NUM_PLAYERS = 2           # Changeable, between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_CONDITION = 4         # Need 4 in a row to win

COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]
AVAILABLE_CHECKERS = CHECKERS[:NUM_PLAYERS]

# ------------------------ FUNCTIONS ------------------------

def clear_screen():
    os.system('clear')    # Clear the terminal screen for Linux/Mac

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+'*COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+'*COLUMNS)

def get_next_open_row(board, col):
    # Returns row index to place checker, or None if column is full
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def is_valid_column(col_input, board):
    if col_input not in COLUMN_LABELS:
        return False
    col = COLUMN_LABELS.index(col_input)
    if board[0][col] != ' ':
        return False
    return True

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def is_board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == ' ':
            return False
    return True

def check_winner(board, checker):
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[row][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_CONDITION + 1):
            if all(board[row + i][col] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - WIN_CONDITION + 1):
        for col in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negatively sloped diagonals
    for row in range(WIN_CONDITION - 1, ROWS):
        for col in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def get_player_input(player_checker, board):
    while True:
        col_input = input(f'Player {player_checker}, please enter a column: ').strip().upper()
        if col_input == '':
            print("Input cannot be empty.")
            continue
        if not is_valid_column(col_input, board):
            if col_input not in COLUMN_LABELS:
                print(f"Invalid column letter! Please choose one of: {', '.join(COLUMN_LABELS)}.")
            elif board[0][COLUMN_LABELS.index(col_input)] != ' ':
                print(f"Column {col_input} is full. Turn is lost.")
                return None
            continue
        return col_input

# ------------------------ MAIN GAME LOOP ------------------------

def main():
    board = create_board(ROWS, COLUMNS)
    first_player = random.randint(0, NUM_PLAYERS-1)
    player_order = [AVAILABLE_CHECKERS[(first_player + i)%NUM_PLAYERS] for i in range(NUM_PLAYERS)]

    game_over = False
    turn = 0

    clear_screen()
    print_board(board)

    while not game_over:
        current_player = player_order[turn % NUM_PLAYERS]
        col_input = get_player_input(current_player, board)
        if col_input is None:
            # Column full, turn lost (do not repeat this turn)
            turn += 1
            continue
        col = COLUMN_LABELS.index(col_input)
        row = get_next_open_row(board, col)
        if row is not None:
            drop_checker(board, row, col, current_player)
            clear_screen()
            print_board(board)

            if check_winner(board, current_player):
                print(f'Player {current_player} won!')
                game_over = True
            elif is_board_full(board):
                print('The game is a draw.')
                game_over = True
            else:
                turn += 1
        else:
            # Shouldn't happen, as we already checked for full column in is_valid_column
            print("This column is full. Turn is lost.")
            turn += 1

if __name__ == '__main__':
    main()
