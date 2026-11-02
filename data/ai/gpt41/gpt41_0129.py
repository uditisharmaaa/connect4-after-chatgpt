import os
import random

# ------------ Constants --------------
NUM_ROWS = 6             # Number of rows
NUM_COLS = 7             # Number of columns (max 26)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2          # Number of players

# ------------ Helper Functions --------------

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board():
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A')+i) for i in range(NUM_COLS)])
    print(header)
    print('+' + '---+' * NUM_COLS)
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * NUM_COLS)

def col_letter_to_index(letter):
    if len(letter) == 1 and 'A' <= letter <= chr(ord('A') + NUM_COLS - 1):
        return ord(letter) - ord('A')
    else:
        return -1

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, symbol):
    # Place checker in the lowest available row
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col
    return None  # Column full

def check_direction(board, row, col, dr, dc, symbol):
    count = 0
    r, c = row, col
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, symbol):
    # Check all 4 directions from the last move

    # Horizontal
    left = check_direction(board, row, col-1, 0, -1, symbol)
    right = check_direction(board, row, col+1, 0, 1, symbol)
    if 1 + left + right >= 4:
        return True

    # Vertical
    up = check_direction(board, row-1, col, -1, 0, symbol)
    down = check_direction(board, row+1, col, 1, 0, symbol)
    if 1 + up + down >= 4:
        return True

    # Diagonal /
    up_right = check_direction(board, row-1, col+1, -1, 1, symbol)
    down_left = check_direction(board, row+1, col-1, 1, -1, symbol)
    if 1 + up_right + down_left >= 4:
        return True

    # Diagonal \
    up_left = check_direction(board, row-1, col-1, -1, -1, symbol)
    down_right = check_direction(board, row+1, col+1, 1, 1, symbol)
    if 1 + up_left + down_right >= 4:
        return True

    return False

def is_board_full(board):
    # If any cell in first row is empty, board is not full
    return all(cell != ' ' for cell in board[0])

def validate_input(user_input):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return False
    if not ('A' <= user_input <= chr(ord('A') + NUM_COLS - 1)):
        return False
    return True

# ------------ Main Game Function --------------

def main():
    board = create_board()
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS-1)
    game_over = False

    while True:
        clear_screen()
        print_board(board)
        if is_board_full(board):
            print("It's a draw!")
            break
        symbol = player_symbols[current_player_index]
        print(f"Player {symbol}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            user_input = input().strip().upper()
            if not validate_input(user_input):
                print(f"Invalid input. Please enter a column letter A-{chr(ord('A')+NUM_COLS-1)}:")
                continue
            col = col_letter_to_index(user_input)
            if col == -1:
                print(f"Invalid column. Please enter a column letter A-{chr(ord('A')+NUM_COLS-1)}:")
                continue
            if is_column_full(board, col):
                print(f"Column {user_input} is full! You lose your turn.")
                valid_turn = True  # Skip player if column full
                break
            result = place_checker(board, col, symbol)
            if result is not None:
                row, _ = result
                if check_win(board, row, col, symbol):
                    clear_screen()
                    print_board(board)
                    print(f"Player {symbol} won!")
                    return
                valid_turn = True
            else:
                print(f"Column {user_input} is full! You lose your turn.")
                valid_turn = True  # Skip player if column full

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
