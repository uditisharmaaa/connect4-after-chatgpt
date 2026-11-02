import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(columns)]
    print("  " + "   ".join(letters))
    # Print horizontal line + rows
    line = "+" + "---+" * columns
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def is_valid_column(input_str, columns):
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    return 'A' <= c < chr(ord('A') + columns)

def column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def find_row(board, col):
    # Return the lowest available row index in the column or None if full
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            return r
    return None

def check_win(board, player_checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(r, c, dr, dc):
        count = 0
        rr, cc = r, c
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == player_checker:
            count += 1
            rr += dr
            cc += dc
        return count

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == player_checker:
                # Horizontal (right)
                if count_direction(r, c, 0, 1) >= WIN_COUNT:
                    return True
                # Vertical (down)
                if count_direction(r, c, 1, 0) >= WIN_COUNT:
                    return True
                # Diagonal down-right
                if count_direction(r, c, 1, 1) >= WIN_COUNT:
                    return True
                # Diagonal down-left
                if count_direction(r, c, 1, -1) >= WIN_COUNT:
                    return True
    return False

def board_full(board):
    # If no empty spaces, board is full
    for row in board:
        if " " in row:
            return False
    return True

def get_player_input(player_checker, board):
    cols = len(board[0])
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(inp, cols):
            continue
        col = column_index(inp)
        row = find_row(board, col)
        if row is None:
            # column full, player loses turn by instructions
            return None
        return row, col

def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    # Setup board and players
    rows = ROWS
    columns = COLUMNS
    players = PLAYERS
    checkers = CHECKERS[:players]

    board = create_board(rows, columns)
    current_player = random.randint(0, players - 1)

    print_board(board)

    while True:
        player_checker = checkers[current_player]
        move = get_player_input(player_checker, board)
        if move is None:
            # Column full: player loses turn, just inform and next player
            print_board(board)
            current_player = next_player_index(current_player, players)
            continue
        r, c = move
        board[r][c] = player_checker
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player = next_player_index(current_player, players)

if __name__ == "__main__":
    main()
