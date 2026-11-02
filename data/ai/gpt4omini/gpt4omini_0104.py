import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Max of 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers A to G
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:  # Valid column check
            return ord(column) - 65
        print("Invalid input. Please try again.")

def drop_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal win
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal (bottom-right)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                # Check diagonal (top-right)
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while True:
        player_checker = PLAYERS[current_player]
        column = get_valid_input(player_checker)

        if drop_checker(board, column, player_checker):
            print_board(board)

            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % len(PLAYERS)  # Change player
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    main()
