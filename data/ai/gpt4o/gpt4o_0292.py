import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:len(board[0])]
    print('  ' + '   '.join(column_labels))
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def get_next_player(current_player, total_players):
    return (current_player + 1) % total_players

def column_to_index(column):
    return ord(column.upper()) - ord('A')

def make_move(board, column, checker):
    index = column_to_index(column)
    for row in reversed(board):
        if row[index] == ' ':
            row[index] = checker
            return True
    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def check_winner(board, checker):
    # check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_valid_input(input_str, num_columns):
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str.upper() <= chr(ord('A') + num_columns - 1)

def play_game(rows, columns, num_players):
    board = initialize_board(rows, columns)
    current_player = random.randint(0, num_players - 1)
    checkers = CHECKERS[:num_players]

    while True:
        print_board(board)
        current_checker = checkers[current_player]

        move_made = False
        while not move_made:
            player_input = input(f"Player {current_checker}, please enter a column: ").strip()
            if not is_valid_input(player_input, columns) or not make_move(board, player_input, current_checker):
                print("Invalid move. Try again.")
                continue
            move_made = True

        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if is_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = get_next_player(current_player, num_players)

if __name__ == "__main__":
    play_game(ROWS, COLUMNS, PLAYERS)
