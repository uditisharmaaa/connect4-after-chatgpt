import os
import random

# CONSTANTS
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def drop_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return True
    return False

def is_valid_input(user_input):
    return len(user_input) == 1 and user_input.isalpha() and "A" <= user_input <= "A" + chr(COLS - 1)

def check_winner(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and
                board[r][c] == player == board[r][c + 1] == board[r][c + 2] == board[r][c + 3]) or \
               (r + 3 < ROWS and
                board[r][c] == player == board[r + 1][c] == board[r + 2][c] == board[r + 3][c]) or \
               (r + 3 < ROWS and c + 3 < COLS and
                board[r][c] == player == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3]) or \
               (r - 3 >= 0 and c + 3 < COLS and
                board[r][c] == player == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3]):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        player = players[current_player_idx]
        print(f"Player {player}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_input(user_input):
            print("Invalid input. Try again.")
            continue

        col = ord(user_input) - 65
        if not drop_checker(board, col, player):
            print("Column full. Try another column.")
            continue

        print_board(board)

        if check_winner(board, player):
            print(f"Player {player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
