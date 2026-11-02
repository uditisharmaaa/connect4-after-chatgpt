import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system("clear")

def create_board():
    # Board: ROWS x COLUMNS filled with spaces " "
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  "
    for i in range(COLUMNS):
        headers += chr(ord('A') + i) + "   "
    print(headers)

    # Print rows with +---+...
    for row in board:
        print("+---" * COLUMNS + "+")
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
    print("+---" * COLUMNS + "+")

def valid_column_input(inp):
    if len(inp) != 1:
        return False
    if not ('A' <= inp <= chr(ord('A') + COLUMNS - 1)):
        return False
    return True

def get_column_index(inp):
    return ord(inp) - ord('A')

def place_checker(board, col, checker):
    # Place checker in lowest available row in column col
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r+i][c] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Diagonal down-right check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLUMNS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r+i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Diagonal up-right check
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLUMNS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    # Select random starting player index
    current_player = random.randint(0, PLAYERS - 1)
    game_over = False

    print_board(board)
    while not game_over:
        checker = CHECKERS[current_player]
        # Input loop
        while True:
            print("Player {}, please enter a column:".format(checker))
            col_input = input().strip().upper()

            if not valid_column_input(col_input):
                continue

            col_index = get_column_index(col_input)

            # Check if column is full:
            if board[0][col_index] != " ":
                # Player loses the turn
                break

            # Place checker
            placed = place_checker(board, col_index, checker)
            if placed:
                break
            else:
                # According to spec, if full turn lost, break to next player
                break

        # Print board after turn (even if turn lost due to full column)
        print_board(board)

        # Check win only if last move was valid and placed
        # If placed=False and column full, player lost turn (no piece placed)
        if board[0][col_index] != " ":
            # We placed a checker (or column full)
            if placed:
                if check_win(board, checker):
                    print("Player {} won!".format(checker))
                    game_over = True
                    break

        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Move to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
