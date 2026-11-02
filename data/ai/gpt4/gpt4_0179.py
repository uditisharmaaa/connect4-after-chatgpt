import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Player symbols for up to 5 players.

def clear_screen():
    os.system('clear')  # Clear the screen (works on Linux/Unix).

def create_board(rows, cols):
    """Create a game board with given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board."""
    cols_labels = "  " + "   ".join([chr(65 + i) for i in range(COLS)])
    print(cols_labels)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(choice, cols):
    """Check if the column choice is valid."""
    return len(choice) == 1 and choice.isalpha() and 'A' <= choice.upper() < chr(65 + cols)

def is_column_full(board, col):
    """Check if a column is completely filled."""
    return board[0][col] != " "

def drop_checker(board, col, player):
    """Drop a checker into the column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return row, col

def check_winner(board, row, col, player):
    """Check if the current player has won the game."""
    def check_direction(dx, dy):
        count = 0
        r, c = row + dy, col + dx
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dy
            c += dx
        return count

    # Check horizontal, vertical, and both diagonals.
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        total = 1 + check_direction(dx, dy) + check_direction(-dx, -dy)
        if total >= 4:
            return True
    return False

def check_draw(board):
    """Check if the game is a draw (board completely filled)."""
    return all(is_column_full(board, col) for col in range(COLS))

def main():
    # Initialize the game
    board = create_board(ROWS, COLS)
    num_players = 2  # Set this constant globally if more players are required.
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        # Get valid column input from user
        while True:
            choice = input("Your choice: ").strip().upper()
            if not is_valid_column(choice, COLS):
                print("Invalid column. Please choose a letter between A and G.")
            else:
                col = ord(choice) - 65
                if is_column_full(board, col):
                    print("Column is full. Please choose a different column.")
                else:
                    break

        # Place the checker
        row, col = drop_checker(board, col, current_player)
        clear_screen()
        print_board(board)

        # Check for a win
        if check_winner(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
