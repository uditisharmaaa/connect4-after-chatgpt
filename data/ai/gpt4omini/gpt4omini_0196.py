import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_column_choice(player):
    while True:
        choice = input(f"Player {player}, please enter a column: ").upper()
        if len(choice) == 1 and 'A' <= choice <= chr(64 + COLS):
            return ord(choice) - 65
        print("Invalid input. Please enter a column between A and " + chr(64 + COLS) + ".")

def place_checker(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def check_winner(board, player):
    def check_direction(start_row, start_col, delta_row, delta_col):
        count = 0
        for i in range(4):
            r = start_row + i * delta_row
            c = start_col + i * delta_col
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        return count == 4

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                if (check_direction(row, col, 0, 1) or  # horizontal
                    check_direction(row, col, 1, 0) or  # vertical
                    check_direction(row, col, 1, 1) or  # diagonal /
                    check_direction(row, col, 1, -1)):  # diagonal \
                    return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    random_player = random.choice(range(len(PLAYERS)))
    current_player_index = random_player

    while True:
        print_board(board)
        column = get_column_choice(PLAYERS[current_player_index])
        if place_checker(board, column, PLAYERS[current_player_index]):
            if check_winner(board, PLAYERS[current_player_index]):
                print_board(board)
                print(f"Player {PLAYERS[current_player_index]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Try again.")

if __name__ == "__main__":
    main()
