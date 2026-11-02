import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    col = ord(col_letter) - ord('A')
    if 0 <= col < cols:
        return True
    return False

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count +=1
            r += r_step
            c += c_step
        return count

    # Horizontal check
    total = 1 + count_dir(0, -1) + count_dir(0, 1)
    if total >= 4:
        return True

    # Vertical check
    total = 1 + count_dir(-1, 0) + count_dir(1, 0)
    if total >= 4:
        return True

    # Diagonal 1 check (\)
    total = 1 + count_dir(-1, -1) + count_dir(1, 1)
    if total >= 4:
        return True

    # Diagonal 2 check (/)
    total = 1 + count_dir(-1, 1) + count_dir(1, -1)
    if total >= 4:
        return True

    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)

    print_board(board)
    while True:
        player = players[current_player_index]
        print(f"Player {player}, please enter a column:")
        col_letter = input().strip().upper()

        # Validate input
        if not is_valid_column(col_letter, COLUMNS):
            print("Invalid column. Please enter a valid column letter.")
            continue

        col = get_column_index(col_letter)
        row = place_checker(board, col, player)
        if row == -1:
            # Column full, player loses turn
            print("Column full. You lose your turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, row, col, player):
            print(f"Player {player} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
