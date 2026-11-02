import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    header = "  " + "   ".join(COLUMN_LABELS[:len(board[0])])
    print(header)
    # Print board rows
    for row in range(len(board)):
        line = "+---" * len(board[0]) + "+"
        print(line)
        row_str = "|"
        for col in range(len(board[0])):
            row_str += " {} |".format(board[row][col])
        print(row_str)
    print("+---" * len(board[0]) + "+")


def valid_column_input(input_str, cols):
    if len(input_str) != 1:
        return False
    upper = input_str.upper()
    if upper not in COLUMN_LABELS[:cols]:
        return False
    return True


def find_row_to_place(board, col):
    # Column is 0-based index
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None  # Column full


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal checks
    # Diagonal down-right (\)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            win = True
            for i in range(WIN_LENGTH):
                if board[r + i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal up-right (/)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            win = True
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    return False


def check_draw(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def get_next_player_index(current_index, num_players):
    return (current_index + 1) % num_players


def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS[:NUM_PLAYERS]

    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player]
        prompt = "Player {}, please enter a column: ".format(player_checker)
        while True:
            move = input(prompt).strip().upper()
            if not valid_column_input(move, COLS):
                continue
            col = COLUMN_LABELS.index(move)
            row_to_place = find_row_to_place(board, col)
            if row_to_place is None:
                # Column full, player loses turn
                break  # Exit input loop, will check win/draw and continue with next player
            else:
                board[row_to_place][col] = player_checker
                break  # Valid move placed

        print_board(board)

        # If move was valid, check win/draw
        if row_to_place is not None:
            if check_winner(board, player_checker):
                print("Player {} won!".format(player_checker))
                return
            if check_draw(board):
                print("The game is a draw!")
                return

        # If column full, player loses turn next player plays

        current_player = get_next_player_index(current_player, NUM_PLAYERS)


if __name__ == "__main__":
    main()
