import os
import random
import string

# ====== CONSTANTS =======
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Changeable up to 5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
CONNECT_N = 4  # How many in a row to win

# ========================

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print header letters
    headers = ["  " + string.ascii_uppercase[i] + " " for i in range(cols)]
    print(''.join(headers))
    # Print board rows
    for r in range(len(board)):
        print('+' + '---+' * cols)
        row_str = ''
        for cell in board[r]:
            row_str += f'| {cell} '
        row_str += '|'
        print(row_str)
    print('+' + '---+' * cols)

def get_player_column_input(board, player_checker):
    cols = len(board[0])
    valid_letters = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Please enter a single letter corresponding to a column.")
            continue
        if user_input not in valid_letters:
            print(f"Invalid column. Choose from {', '.join(valid_letters)}.")
            continue
        col = valid_letters.index(user_input)
        # Check if column is full
        if board[0][col] != ' ':
            print("That column is full. Your turn is skipped.")
            return None
        return col

def place_checker(board, col, checker):
    # Place checker in the lowest empty row in column col
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Column full

def is_winning_move(board, row, col, checker):
    directions = [
        (0,1), # horizontal
        (1,0), # vertical
        (1,1), # diagonal down-right
        (1,-1) # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= CONNECT_N:
            return True
    return False

def is_board_full(board):
    # If top row (row 0) has any empty cells, board is not full
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    # Pick a random starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    winner = None

    while True:
        checker = PLAYER_CHECKERS[current_player_idx]
        col = get_player_column_input(board, checker)
        clear_screen()
        if col is not None:
            # Place checker and get position
            row_col = place_checker(board, col, checker)
            print_board(board)
            if row_col:
                row, col = row_col
                if is_winning_move(board, row, col, checker):
                    print(f"Player {checker} won!")
                    break
                elif is_board_full(board):
                    print("Game is a draw!")
                    break
            # Else, column was full: as per spec, skip the turn.
        else:
            print_board(board)
            # Turn was skipped due to full column

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
