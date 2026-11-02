import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_COUNT = 2  # Default to 2 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' '] * COLS for _ in range(ROWS)]

def print_board(board):
    board_view = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS)) + "\n"
    board_view += "+---" * COLS + "+\n"
    for row in board:
        board_view += "|" + "|".join(f" {cell} " for cell in row) + "|\n"
        board_view += "+---" * COLS + "+\n"
    print(board_view)

def get_valid_move(board):
    while True:
        move = input().strip().upper()
        if len(move) == 1 and 'A' <= move < chr(ord('A') + COLS):
            col = ord(move) - ord('A')
            if board[0][col] == ' ':
                return col
        print("Invalid move. Try again.")

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def check_win(board, row, col):
    def check_direction(delta_x, delta_y):
        count = 0
        for dir in (-1, 1):
            r, c = row, col
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == board[row][col]:
                count += 1
                if count >= 4:
                    return True
                r += delta_y * dir
                c += delta_x * dir
        return False

    return (check_direction(1, 0) or  # Horizontal
            check_direction(0, 1) or  # Vertical
            check_direction(1, 1) or  # Diagonal /
            check_direction(1, -1))   # Diagonal \

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYER_COUNT - 1)

    clear_screen()
    print_board(board)

    while True:
        print(f"Player {PLAYERS[current_player]}, please enter a column:")
        col = get_valid_move(board)
        row, col = drop_checker(board, col, PLAYERS[current_player])

        clear_screen()
        print_board(board)

        if check_win(board, row, col):
            print(f"Player {PLAYERS[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
