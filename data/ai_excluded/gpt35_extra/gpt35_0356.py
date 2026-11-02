import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4

PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column headers
    header = '  '
    for col in range(columns):
        header += f' {chr(ord("A") + col)}  '
    print(header)

    separator = '+' + '---+' * columns
    for row in range(len(board)):
        print(separator)
        row_str = '|'
        for col in range(columns):
            row_str += f' {board[row][col]} |'
        print(row_str)
    print(separator)

def get_valid_column_input(board, player_checker):
    columns = len(board[0])
    while True:
        inp = input(f'Player {player_checker}, please enter a column: ').strip()
        if len(inp) != 1 or not inp.isalpha():
            # Invalid input
            continue
        col_char = inp.upper()
        col_index = ord(col_char) - ord('A')
        if col_index < 0 or col_index >= columns:
            continue
        # Check if column full
        if board[0][col_index] != ' ':
            # Column full, player loses the turn
            return None
        return col_index

def place_checker(board, col_index, checker):
    # Place checker in lowest available space in col_index
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index
    # Should not reach here if checked before
    return None, None

def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(columns):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(columns):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_LENGTH:
                    return True
            else:
                count = 0

    # Check diagonal down-right (/)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(columns - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Check diagonal up-right (\)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(columns - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    return False

def check_draw(board):
    # Draw if no empty spaces in top row (means board full)
    return all(cell != ' ' for cell in board[0])

def main():
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = PLAYERS_CHECKERS[:num_players]

    board = create_board(rows, columns)
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_index]
        col_index = get_valid_column_input(board, player_checker)

        if col_index is None:
            # Column full, lose turn
            # Just move to next player
            current_player_index = (current_player_index + 1) % num_players
            print_board(board)
            continue

        place_checker(board, col_index, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f'Player {player_checker} won!')
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    main()
