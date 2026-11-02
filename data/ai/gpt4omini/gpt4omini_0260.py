import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Add more players if needed

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))  # Column headers A, B, C, ...
    print('+' + '---+' * COLS)  # Row separator
    for row in board:
        print('|' + ' | '.join(row) + '|')  # Print each row
        print('+' + '---+' * COLS)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    return ord(column.upper()) - 65

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if check_direction(board, r, c, 1, 0, checker):  # Horizontal
                    return True
                if check_direction(board, r, c, 0, 1, checker):  # Vertical
                    return True
                if check_direction(board, r, c, 1, 1, checker):  # Diagonal /
                    return True
                if check_direction(board, r, c, 1, -1, checker):  # Diagonal \
                    return True
    return False

def check_direction(board, start_r, start_c, delta_r, delta_c, checker):
    count = 0
    for i in range(4):  # Check 4 in a row
        r = start_r + i * delta_r
        c = start_c + i * delta_c
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if is_valid_input(column_input):
            col_index = get_column_index(column_input)

            if not is_column_full(board, col_index):
                place_checker(board, col_index, current_player)

                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    break

                if check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    break

                current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch player
            else:
                print("Column is full, try a different column.")
        else:
            print("Invalid input, please enter a valid column (A-G).")

if __name__ == "__main__":
    main()
