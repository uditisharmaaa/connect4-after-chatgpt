import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M'][:2]  # Limiting to 2 players as per submission requirements

def create_board(rows, columns):
    """Create the game board with specified rows and columns."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current game board to the terminal."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_next_open_row(board, col):
    """Return the next open row in the specified column."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def check_for_win(board, player, row, col):
    """Check if there's a win condition for the player starting from the specified row and column."""
    def check_direction(delta_row, delta_col):
        count = 1
        # Check in the positive direction
        r, c = row + delta_row, col + delta_col
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            count += 1
            r += delta_row
            c += delta_col

        # Check in the negative direction
        r, c = row - delta_row, col - delta_col
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            count += 1
            r -= delta_row
            c -= delta_col

        return count >= 4

    # Check all directions: horizontal, vertical, and both diagonals
    return (check_direction(0, 1) or  # Horizontal
            check_direction(1, 0) or  # Vertical
            check_direction(1, 1) or  # Diagonal \
            check_direction(1, -1))   # Diagonal /

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Initialize game board
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    # Randomly select the first player
    current_player_idx = random.choice(range(len(PLAYER_MARKERS)))
    game_over = False

    while not game_over:
        current_player = PLAYER_MARKERS[current_player_idx]
        print(f"Player {current_player}, please enter a column:")

        # Validate player input
        while True:
            user_input = input().strip().upper()
            if len(user_input) == 1 and 'A' <= user_input <= 'G':
                col = ord(user_input) - ord('A')
                if 0 <= col < COLUMNS and get_next_open_row(board, col) is not None:
                    break
                else:
                    print("Column is full or invalid, please choose a different column.")
            else:
                print("Invalid input, please enter a letter between A-G.")

        # Place the checker
        row = get_next_open_row(board, col)
        board[row][col] = current_player
        print_board(board)

        # Check for a win or draw
        if check_for_win(board, current_player, row, col):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Alternate players
            current_player_idx = (current_player_idx + 1) % 2

if __name__ == "__main__":
    main()
