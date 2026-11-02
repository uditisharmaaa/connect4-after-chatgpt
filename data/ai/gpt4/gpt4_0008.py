import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates an empty game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Displays the current state of the game board."""
    # Print column labels
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_labels)
    print("+" + "---+" * len(board[0]))
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_column_index(column_letter):
    """Converts a column label (A, B, ...) to an index."""
    return ord(column_letter.upper()) - ord('A')

def is_valid_input(input_str, columns):
    """Checks if the user input is valid."""
    if len(input_str) != 1:
        return False
    if not input_str.isalpha():
        return False
    index = get_column_index(input_str)
    return 0 <= index < columns

def drop_checker(board, column, checker):
    """Drops a checker into the specified column."""
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][column] == " ":
            board[row_index][column] = checker
            return row_index, column
    return None  # Column is full

def is_winning_move(board, row, col, checker):
    """Checks if placing the checker at (row, col) results in a win."""
    def count_direction(row_step, col_step):
        """Counts checkers in a specific direction."""
        count = 0
        r, c = row + row_step, col + col_step
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += row_step
            c += col_step
        return count

    # Check all four directions: horizontal, vertical, diagonal1, diagonal2
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (1, 1),  # Down-Right
        (1, -1), # Down-Left
    ]

    for dr, dc in directions:
        count = 1 + count_direction(dr, dc) + count_direction(-dr, -dc)
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Checks if the board is full (no empty spaces)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    clear_screen()
    
    # Create the board
    board = create_board(ROWS, COLUMNS)

    # Initialize players
    num_players = 2  # Can be adjusted for up to MAX_PLAYERS
    player_checkers = PLAYERS[:num_players]

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)

    # Print the initial board
    print_board(board)

    # Game loop
    while True:
        clear_screen()
        
        # Display the board
        print_board(board)
        
        # Current player's turn
        current_player_checker = player_checkers[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        # Get and validate input
        while True:
            user_input = input().strip()
            if not is_valid_input(user_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter:")
                continue

            column_index = get_column_index(user_input)

            # Check if the column is full
            if board[0][column_index] != " ":
                print("Column is full. Please choose another column:")
                continue

            break

        # Place the checker
        placed_position = drop_checker(board, column_index, current_player_checker)

        # Check for a win
        if is_winning_move(board, *placed_position, current_player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break

        # Check for a draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
