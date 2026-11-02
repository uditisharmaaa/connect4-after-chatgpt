import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    print(col_labels)
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= chr(64 + COLS)

def get_column_index(col):
    return ord(col.upper()) - 65

def drop_checker(board, col, player_mark):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_mark
            return True
    return False

def check_win(board, player_mark):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player_mark:
                # Check horizontal
                if c <= COLS - 4 and all(board[r][c + i] == player_mark for i in range(4)):
                    return True
                # Check vertical
                if r <= ROWS - 4 and all(board[r + i][c] == player_mark for i in range(4)):
                    return True
                # Check diagonal right-down
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == player_mark for i in range(4)):
                    return True
                # Check diagonal left-down
                if r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == player_mark for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = PLAYER_MARKS[:2]  # Can adjust for more players
    current_player = random.choice(players)
    game_over = False

    print_board(board)

    while not game_over:
        print(f"Player {current_player}, please enter a column: ")
        user_input = input().strip()

        if not is_valid_input(user_input):
            print("Invalid input! Please enter a valid column letter.")
            continue

        col_index = get_column_index(user_input)
        
        if not drop_checker(board, col_index, current_player):
            print("Column is full! Please choose another column.")
            continue

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            break
        
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            break

        # Switch to the next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % len(players)]

if __name__ == "__main__":
    main()
