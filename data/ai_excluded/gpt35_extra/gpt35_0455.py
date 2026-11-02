import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_TO_WIN = 4

# Players and their checkers depending on number of players used
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Number of players for the submission (set to 2 as requested)
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for __ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print('  ' + '   '.join(headers))
    # Print board rows with dividing lines
    line = '+---' * cols + '+'
    for row in board:
        print(line)
        print('| ' + ' | '.join(row) + ' |')
    print(line)

def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    ch = input_str.upper()
    if ch not in string.ascii_uppercase[:cols]:
        return False
    return True

def column_index_from_letter(letter):
    return string.ascii_uppercase.index(letter.upper())

def get_available_row(board, col):
    # Return index of lowest empty row in given column, or None if full
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def place_checker(board, col, checker):
    row = get_available_row(board, col)
    if row is None:
        return False  # Column full
    board[row][col] = checker
    return row

def check_winner(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    # Check all directions - horizontal, vertical, two diagonals
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        total = 1  # Count current checker
        total += count_direction(dr, dc)
        total += count_direction(-dr, -dc)
        if total >= NUM_TO_WIN:
            return True
    return False

def board_is_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)
    print(f"Player {checkers[current_player_idx]} starts!")
    
    while True:
        current_checker = checkers[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        while True:
            player_input = input().strip()
            if not is_valid_column(player_input, COLUMNS):
                print(f"Invalid input. Please enter a letter between A and {string.ascii_uppercase[COLUMNS-1]}:")
                continue
            col = column_index_from_letter(player_input)
            if get_available_row(board, col) is None:
                # column full, loses turn
                # but instructions: "the turn is invalid and the player loses the turn"
                # So print no prompt, just lose turn
                # We break input loop to next player
                # Inform player their turn is lost due to full column
                print(f"Column {player_input.upper()} is full. Turn lost.")
                break
            # valid and not full
            placed_row = place_checker(board, col, current_checker)
            if placed_row is not False:
                break

        print_board(board)

        # If placed_row is False, it means the player lost turn by full column; no checker placed.
        # Else check for win and draw
        if placed_row is not False:
            if check_winner(board, placed_row, col, current_checker):
                print(f"Player {current_checker} won!")
                return
            if board_is_full(board):
                print("The game is a draw!")
                return

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
