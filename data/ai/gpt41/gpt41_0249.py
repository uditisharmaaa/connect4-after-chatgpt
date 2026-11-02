import os
import random

# ====== CONSTANTS ======
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # For labeling columns A-Z if needed
PLAYER_CHARS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Change to 2-5 (but set to 2 for submission)

EMPTY_CELL = " "


# ====== FUNCTIONS ======

def clear_screen():
    os.system('clear')  # Use 'cls' if running on Windows


def create_board(rows, columns):
    # Create a 2D list filled with empty characters
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    columns = len(board[0])
    # Print header letters
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(columns)])
    print(header)
    print('+' + '---+' * columns)
    for row in board:
        row_line = '| ' + ' | '.join(row) + ' |'
        print(row_line)
        print('+' + '---+' * columns)


def get_valid_column_input(board):
    columns = len(board[0])
    column_labels = [chr(ord('A') + i) for i in range(columns)]
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in column_labels:
            print("Invalid input. Please enter a column letter between {} and {}.".format(column_labels[0], column_labels[-1]))
            continue
        col_num = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col_num] != EMPTY_CELL:
            print("Column is full. You lose your turn!")
            return None  # Indicate that this is an invalid turn and the turn is lost
        return col_num


def place_checker(board, col, checker):
    # From bottom up, find the first empty cell in the column
    for row in reversed(board):
        if row[col] == EMPTY_CELL:
            row[col] = checker
            return board.index(row), col  # Return the location for win checking
    # Should not reach here since col fullness is checked above
    return None, None


def check_win(board, last_row, last_col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(dx, dy):
        count = 0
        x, y = last_row, last_col
        while True:
            x += dx
            y += dy
            if 0 <= x < rows and 0 <= y < cols and board[x][y] == checker:
                count += 1
            else:
                break
        return count

    # Check all four directions from the last placed checker
    directions = [ (0,1), (1,0), (1,1), (1,-1) ] # horiz, vert, diag1, diag2
    for dx, dy in directions:
        count = 1  # Start with the just placed piece
        count += count_dir(dx, dy)
        count += count_dir(-dx, -dy)
        if count >= 4:
            return True
    return False


def check_draw(board):
    # The board is draw if all top cells are filled (no EMPTY_CELL at top row)
    for cell in board[0]:
        if cell == EMPTY_CELL:
            return False
    return True


def main():
    # Set up players
    player_symbols = PLAYER_CHARS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)
    # Randomly select who starts
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    game_over = False
    winner = None

    while not game_over:
        print("Player {}, it's your turn!".format(player_symbols[current_player]))
        col = get_valid_column_input(board)
        if col is None:
            # Column is full, move to next player and continue
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, col_used = place_checker(board, col, player_symbols[current_player])

        clear_screen()
        print_board(board)
        # Check for win
        if check_win(board, row, col_used, player_symbols[current_player]):
            winner = player_symbols[current_player]
            print("Player {} won!".format(winner))
            game_over = True
            break
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == '__main__':
    main()
