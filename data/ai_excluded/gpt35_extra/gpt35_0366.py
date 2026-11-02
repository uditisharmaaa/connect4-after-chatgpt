import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players
NUM_PLAYERS = 2  # Must be between 2 and 5

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    # Print rows with separators
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def get_valid_column_input(player_checker, board):
    columns = len(board[0])
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col) != 1:
            # Invalid if input length is not 1
            continue
        if not ('A' <= col <= chr(ord('A') + columns - 1)):
            # Not a valid column letter
            continue
        col_index = ord(col) - ord('A')
        # Check if the column is fully filled
        if board[0][col_index] != " ":
            # Column full: player loses turn (return None to indicate this)
            return None
        return col_index

def place_checker(board, col, checker):
    # Place checker in lowest available space in given column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # Return the position where checker was placed
    # Should not get here if called correctly (caller checks column full)
    return None, None

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Number of checkers in a row needed to win
    to_win = 4

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == to_win:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == to_win:
                    return True
            else:
                count = 0

    # Diagonal checks
    # Down-right diagonals (\)
    for r in range(rows - to_win + 1):
        for c in range(cols - to_win + 1):
            if all(board[r + i][c + i] == checker for i in range(to_win)):
                return True

    # Down-left diagonals (/)
    for r in range(rows - to_win + 1):
        for c in range(to_win - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(to_win)):
                return True

    return False

def board_full(board):
    # If no empty spaces in top row, board is full
    return all(cell != " " for cell in board[0])

def main():
    # Setup
    num_players = NUM_PLAYERS
    players = CHECKERS[:num_players]

    board = create_board(ROWS, COLUMNS)

    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} starts the game!")

    while True:
        player_checker = players[current_player_index]

        col = get_valid_column_input(player_checker, board)

        if col is None:
            # Column full, lose turn
            # Just continue to next player
            current_player_index = (current_player_index + 1) % num_players
            continue

        place_checker(board, col, player_checker)
        print_board(board)

        # Check for winner
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
