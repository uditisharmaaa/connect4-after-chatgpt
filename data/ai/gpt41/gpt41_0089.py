import os
import random
import string

# ----------- CONSTANT VARIABLES -----------
NUM_ROWS = 6
NUM_COLS = 7           # Max 26
NUM_PLAYERS = 2        # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "
WIN_LENGTH = 4

# ----------- FUNCTIONS -----------

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print header letters
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    # Print separator
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def is_valid_column(input_str, board):
    if len(input_str) != 1 or input_str not in string.ascii_uppercase:
        return False
    col = string.ascii_uppercase.index(input_str)
    if col < 0 or col >= len(board[0]):
        return False
    # Check if column is full
    if board[0][col] != EMPTY_CELL:
        return False
    return True

def get_column_index(input_str):
    return string.ascii_uppercase.index(input_str)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == EMPTY_CELL:
            row[col] = checker
            return board.index(row), col  # return row and col where checker landed
    return None, None  # Column full

def check_win(board, row, col, checker):
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down right
        (1, -1),  # Diagonal down left
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while in_bounds(board, r, c) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while in_bounds(board, r, c) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def in_bounds(board, r, c):
    rows = len(board)
    cols = len(board[0])
    return 0 <= r < rows and 0 <= c < cols

def is_draw(board):
    for cell in board[0]:
        if cell == EMPTY_CELL:
            return False
    return True

# ----------- MAIN GAME LOOP -----------
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts!")
    input("Press Enter to begin...")

    while True:
        print_board(board)
        player_checker = CHECKERS[current_player]
        col_input = ""
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            if not is_valid_column(col_input, board):
                if len(col_input) != 1 or col_input not in string.ascii_uppercase[:NUM_COLS]:
                    print(f"Invalid input! Please enter a column letter (A-{string.ascii_uppercase[NUM_COLS-1]}).")
                elif board[0][get_column_index(col_input)] != EMPTY_CELL:
                    print("Column is full! You lose your turn.")
                    valid_input = True  # Player loses turn for full column
                    col_input = None
            else:
                valid_input = True

        # If input was invalid because of full column, move to next player
        if col_input is None:
            current_player = get_next_player_index(current_player, NUM_PLAYERS)
            continue

        col_index = get_column_index(col_input)
        row_index, col_index = drop_checker(board, col_index, player_checker)

        # Check if current player has won
        if check_win(board, row_index, col_index, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        # Next player's turn
        current_player = get_next_player_index(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    main()
