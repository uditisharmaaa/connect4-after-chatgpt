import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a game board initialized with spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board to the terminal."""
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column headers A, B, C, etc.
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_valid_input(player):
    """Get a valid column input from the player."""
    while True:
        choice = input(f"Player {player}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()
        if choice in (chr(65 + i) for i in range(COLUMNS)):
            return ord(choice) - 65  # Convert letter to column index
        else:
            print("Invalid input. Please enter a column letter in the valid range.")

def place_checker(board, column, player):
    """Place the player's checker in the specified column if possible."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return True  # Successfully placed the checker
    return False  # Column is full

def check_winner(board):
    """Check for a winner in the board."""
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] != " ":
                if check_direction(board, r, c, 1, 0) or check_direction(board, r, c, 0, 1) or \
                   check_direction(board, r, c, 1, 1) or check_direction(board, r, c, 1, -1):
                    return board[r][c]  # Return the winner
    return None  # No winner found

def check_direction(board, row, col, d_row, d_col):
    """Check four in a row in a specific direction."""
    piece = board[row][col]
    count = 0
    for i in range(4):
        r = row + d_row * i
        c = col + d_col * i
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == piece:
            count += 1
            if count == 4:
                return True
        else:
            break
    return False

def check_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    players_count = len(PLAYERS)
    current_player_index = random.randint(0, players_count - 1)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        column = get_valid_input(current_player)

        if place_checker(board, column, current_player):
            print_board(board)

            if check_winner(board):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("It's a draw!")
                break

            current_player_index = (current_player_index + 1) % players_count
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    main()
