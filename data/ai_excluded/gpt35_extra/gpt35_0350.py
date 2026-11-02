import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(labels))
    # Print rows
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_player_input(player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip()
        # Validate input length is 1 uppercase letter A-G (or letter within range)
        if len(inp) != 1 or not inp.isalpha():
            # Invalid input, ask again
            continue
        col_letter = inp.upper()
        col_index = ord(col_letter) - ord('A')
        if col_index < 0 or col_index >= COLUMNS:
            # Out of range
            continue
        return col_index

def place_checker(board, col_index, player_checker):
    # Place checker in lowest available spot
    # Return True if placed, False if column is full
    for r in range(ROWS-1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False

def check_winner(board, player_checker):
    # Check horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == player_checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0
    # Check vertical
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == player_checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0
    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r + i][c + i] == player_checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, ROWS):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] == player_checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        player_checker = players[current_player_index]
        col_index = get_player_input(player_checker)
        placed = place_checker(board, col_index, player_checker)
        if not placed:
            # lose turn, just print board and continue with next player
            print_board(board)
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        print_board(board)
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
