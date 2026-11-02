import os
import random

# Constants for game configuration
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console for a fresh view
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row values
        print("+---" + "---+" * COLS)

def get_input(player):
    while True:
        column = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if column in [chr(i) for i in range(65, 65 + COLS)]:
            return ord(column) - 65
        print("Invalid input. Please try again.")

def place_checker(board, column, player):
    for row in reversed(board):  # Place the checker in the lowest available row
        if row[column] == " ":
            row[column] = player
            return True
    return False  # Column is full

def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if (
                check_line(board, player, r, c, 1, 0) or  # Check horizontal
                check_line(board, player, r, c, 0, 1) or  # Check vertical
                check_line(board, player, r, c, 1, 1) or  # Check diagonal \
                check_line(board, player, r, c, 1, -1)    # Check diagonal /
            ):
                return True
    return False

def check_line(board, player, start_row, start_col, delta_row, delta_col):
    count = 0
    for i in range(4):
        r = start_row + i * delta_row
        c = start_col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        column = get_input(current_player)

        if place_checker(board, column, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            
            # Switch to the next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    main()
