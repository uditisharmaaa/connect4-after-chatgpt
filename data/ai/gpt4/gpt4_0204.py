import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def initialize_board(rows, cols):
    """Initializes the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board to the console."""
    clear_screen()
    col_labels = '   '.join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    for row in board:
        print("+---" * len(board[0]) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def get_valid_input(board):
    """Gets and validates the column input from the player."""
    while True:
        player_input = input("Please enter a column: ").strip().upper()
        if len(player_input) != 1 or not player_input.isalpha():
            print("Invalid input! Please enter a valid column letter.")
            continue
        col_index = ord(player_input) - 65
        if col_index < 0 or col_index >= len(board[0]):
            print("Invalid column! Please choose a column within the bounds of the board.")
            continue
        if board[0][col_index] != ' ':
            print("Column is full! Choose a different column.")
            continue
        return col_index

def drop_checker(board, col_index, symbol):
    """Drops the checker into the specified column."""
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = symbol
            break

def check_win_direction(board, start_row, start_col, direction, symbol):
    """Checks for 4 in a row in a specific direction."""
    dr, dc = direction
    count = 0
    for i in range(4):
        r, c = start_row + i * dr, start_col + i * dc
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
        else:
            break
    return count == 4

def check_win(board, symbol):
    """Checks if the given symbol has a winning condition."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == symbol:
                for dr, dc in directions:
                    if check_win_direction(board, r, c, (dr, dc), symbol):
                        return True
    return False

def is_draw(board):
    """Checks if the game ended in a draw."""
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def play_game():
    """Main function to play the game."""
    # Setup game
    num_players = 2  # Fixed for submission (can be changed for >2 players)
    players = PLAYER_SYMBOLS[:num_players]
    board = initialize_board(ROWS, COLS)
    random.shuffle(players)
    current_player_index = 0

    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    # Game loop
    while True:
        print_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn!")
        col_index = get_valid_input(board)
        drop_checker(board, col_index, current_player)

        # Check for win or draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    play_game()
