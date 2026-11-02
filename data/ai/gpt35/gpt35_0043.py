import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # print column headers
    headers = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    return 0 <= col < cols

def get_next_open_row(board, col):
    # returns the lowest unoccupied row index in column col or None if full
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def place_checker(board, col, checker):
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = checker
        return row
    return None

def board_full(board):
    for col in range(len(board[0])):
        if get_next_open_row(board, col) is not None:
            return False
    return True

def check_win(board, checker, row, col):
    rows = len(board)
    cols = len(board[0])

    def count_in_direction(delta_r, delta_c):
        count = 1
        # check forward direction
        r, c = row + delta_r, col + delta_c
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += delta_r
            c += delta_c
        # check backward direction
        r, c = row - delta_r, col - delta_c
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= delta_r
            c -= delta_c
        return count

    # Horizontal check (row fixed, col varies)
    if count_in_direction(0, 1) >= WIN_COUNT:
        return True
    # Vertical check (col fixed, row varies)
    if count_in_direction(1, 0) >= WIN_COUNT:
        return True
    # Diagonal down-right / up-left
    if count_in_direction(1, 1) >= WIN_COUNT:
        return True
    # Diagonal up-right / down-left
    if count_in_direction(-1, 1) >= WIN_COUNT:
        return True

    return False

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYER_COUNT]

    current_player_index = random.randint(0, PLAYER_COUNT - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_index]
        prompt = f'Player {current_checker}, please enter a column: '

        # Input validation loop
        while True:
            col_input = input(prompt).strip()
            if not is_valid_column(col_input, COLS):
                # invalid character or out of bounds
                continue
            col = ord(col_input) - ord('A')
            # check if column is full
            if get_next_open_row(board, col) is None:
                # Column full - player loses turn (do not ask again)
                break
            # valid input and column not full
            break

        # If column full, player loses turn; skip placing checker
        if get_next_open_row(board, col) is None:
            # Next player
            current_player_index = (current_player_index + 1) % PLAYER_COUNT
            continue

        row = place_checker(board, col, current_checker)

        if check_win(board, current_checker, row, col):
            print_board(board)
            print(f'Player {current_checker} won!')
            break

        if board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # next player's turn
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == '__main__':
    main()
