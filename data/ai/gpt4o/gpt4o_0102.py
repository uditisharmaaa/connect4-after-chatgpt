import os
import random

# Global constants
NUM_PLAYERS = 2
BOARD_ROWS = 6
BOARD_COLUMNS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {header}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def get_valid_column(columns):
    while True:
        user_input = input("Enter a column (A-G): ").strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(64 + columns):
            return ord(user_input) - 65
        print("Invalid input! Please enter a valid column.")

def drop_checker(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player_symbol
            return True
    return False

def check_winner(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == " ":
                continue
            if check_direction(board, row, col, 1, 0) or \
               check_direction(board, row, col, 0, 1) or \
               check_direction(board, row, col, 1, 1) or \
               check_direction(board, row, col, 1, -1):
                return board[row][col]
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col):
    player_symbol = board[start_row][start_col]
    for i in range(1, 4):
        new_row = start_row + delta_row * i
        new_col = start_col + delta_col * i
        if not (0 <= new_row < len(board) and 0 <= new_col < len(board[0])):
            return False
        if board[new_row][new_col] != player_symbol:
            return False
    return True

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        column = get_valid_column(BOARD_COLUMNS)
        if not drop_checker(board, column, current_player):
            print("Column is full! Turn lost.")
        else:
            print_board(board)
            winner = check_winner(board)
            if winner:
                print(f"Player {winner} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
