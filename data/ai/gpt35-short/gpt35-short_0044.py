import os
import random

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')  # On Windows use 'cls'
    
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + "   ".join(COL_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            print("Invalid input. Number must be between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_player_move(player_token):
    while True:
        move = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if move in COL_LABELS:
            return COL_LABELS.index(move)
        print("Invalid column. Please pick a letter from A to G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player_token):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_token
            return row, col

def check_direction(board, start_row, start_col, delta_row, delta_col, token):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == token:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, token):
    # Check 4 directions: vertical, horizontal, and two diagonals
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = (
            check_direction(board, row, col, dr, dc, token) +
            check_direction(board, row, col, -dr, -dc, token) - 1
        )
        if total >= 4:
            return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!\n")
    num_players = get_num_players()
    players = PLAYER_TOKENS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player_token = players[current_player_index]

        col = get_player_move(player_token)

        if not is_valid_move(board, col):
            print("Column is full! Choose another column.")
            input("Press Enter to continue...")
            continue

        row, col = make_move(board, col, player_token)

        if check_win(board, row, col, player_token):
            clear_screen()
            print_board(board)
            print(f"Player {player_token} wins! Congratulations!")
            break
        
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_index = (current_player_index + 1) % num_players

    print("Game over.")

if __name__ == "__main__":
    main()
