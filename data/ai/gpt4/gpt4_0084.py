import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
STARTING_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_empty_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    column_headers = "  " + "   ".join(alphabet[:len(board[0])])
    print(column_headers)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def prompt_player_input(player, columns):
    while True:
        column_letter = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column_letter) == 1 and column_letter.isalpha():
            column_index = ord(column_letter) - ord("A")
            if 0 <= column_index < columns:
                return column_index
        print("Invalid input. Try again.")

def place_checker(board, column, player):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return True
    return False

def is_winning_move(board, row, col, player):
    # Check horizontally
    for start_col in range(max(0, col - 3), min(COLUMNS - 3, col) + 1):
        if all(board[row][start_col + i] == player for i in range(4)):
            return True

    # Check vertically
    if row >= 3 and all(board[row - i][col] == player for i in range(4)):
        return True

    # Check diagonal (\)
    for start_row, start_col in zip(range(row - 3, row + 1), range(col - 3, col + 1)):
        if 0 <= start_row <= ROWS - 4 and 0 <= start_col <= COLUMNS - 4:
            if all(board[start_row + i][start_col + i] == player for i in range(4)):
                return True

    # Check anti-diagonal (/)
    for start_row, start_col in zip(range(row - 3, row + 1), range(col + 3, col - 1, -1)):
        if 0 <= start_row <= ROWS - 4 and 3 <= start_col < COLUMNS:
            if all(board[start_row + i][start_col - i] == player for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def find_last_filled_row(board, column):
    for r in range(ROWS):
        if board[r][column] != " ":
            return r
    return None

def main():
    # Game initialization
    num_players = STARTING_PLAYERS
    players = PLAYERS[:num_players]
    board = create_empty_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    while True:
        player = players[current_player_index]
        column = prompt_player_input(player, COLUMNS)

        if not place_checker(board, column, player):
            print("Column is full. Try a different column.")
            continue

        print_board(board)  # Update the board after a valid move

        # Check for win
        last_row = find_last_filled_row(board, column)
        if is_winning_move(board, last_row, column, player):
            print(f"Player {player} won!")
            break

        # Check for draw
        if check_for_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
