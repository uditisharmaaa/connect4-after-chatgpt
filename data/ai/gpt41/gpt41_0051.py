import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2  # can be changed for testing (between 2 and 5)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(columns)]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * columns)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * columns)

def get_player_symbols(num_players):
    return PLAYER_SYMBOLS[:num_players]

def get_available_row(board, col):
    # Returns index of the lowest available row in the given column, else None
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def is_valid_column(input_str, columns):
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    if letter not in string.ascii_uppercase[:columns]:
        return False
    return True

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def check_win(board, player, win_count=4):
    rows = len(board)
    columns = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(columns - win_count + 1):
            if all(board[r][c + i] == player for i in range(win_count)):
                return True

    # Vertical
    for c in range(columns):
        for r in range(rows - win_count + 1):
            if all(board[r + i][c] == player for i in range(win_count)):
                return True

    # Diagonal down-right
    for r in range(rows - win_count + 1):
        for c in range(columns - win_count + 1):
            if all(board[r + i][c + i] == player for i in range(win_count)):
                return True

    # Diagonal down-left
    for r in range(rows - win_count + 1):
        for c in range(win_count - 1, columns):
            if all(board[r + i][c - i] == player for i in range(win_count)):
                return True

    return False

def main():
    columns = COLUMNS
    rows = ROWS
    num_players = NUM_PLAYERS
    player_symbols = get_player_symbols(num_players)
    board = create_board(rows, columns)
    current_player_index = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board, columns)
    print(f'Player {player_symbols[current_player_index]}, you start!')

    while True:
        player = player_symbols[current_player_index]
        valid_turn = False
        while not valid_turn:
            print()
            move = input(f'Player {player}, please enter a column: ').strip().upper()
            if not is_valid_column(move, columns):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col = ord(move) - ord('A')
            if col < 0 or col >= columns:
                print("Invalid column. Please try again.")
                continue
            row = get_available_row(board, col)
            if row is None:
                print("Column is full. You lose your turn.")
                valid_turn = True  # Lose turn as column is full
                break
            else:
                board[row][col] = player
                valid_turn = True

        clear_screen()
        print_board(board, columns)

        if row is not None:
            if check_win(board, player):
                print(f'Player {player} won!')
                break

        if board_full(board):
            print('Game ended in a draw!')
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    main()
