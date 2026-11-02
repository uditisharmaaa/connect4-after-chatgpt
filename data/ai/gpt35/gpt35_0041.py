import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print the board with separators
    for row in board:
        print("+" + "---+" * len(board[0]))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def choose_first_player(players):
    return random.randint(0, players - 1)

def input_column(player_checker, cols, board):
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ")
        if len(col_input) != 1:
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        if col_input not in valid_cols:
            print("Invalid column. Please enter a letter from A to " + chr(ord('A') + cols - 1) + ".")
            continue
        col_index = ord(col_input) - ord('A')
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full - turn lost
            return -1
        return col_index

def place_checker(board, col, checker):
    # Place checker in lowest empty spot in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Should not reach here if called correctly

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def check_draw(board):
    # If no spaces in top row, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS
    checkers = CHECKERS[:players]

    current_player = choose_first_player(players)
    print_board(board)

    while True:
        player_checker = checkers[current_player]

        col = input_column(player_checker, COLS, board)
        if col == -1:
            # Column full, player loses turn
            print(f"Column full. Player {player_checker} loses their turn.")
            current_player = (current_player + 1) % players
            continue

        place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
