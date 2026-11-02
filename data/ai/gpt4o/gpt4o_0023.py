import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = ' '.join([chr(i) for i in range(ord('A'), ord('A') + COLUMNS)])
    print(f"  {column_labels}")
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def is_valid_column(column):
    return column.isalpha() and ord(column) - ord('A') < COLUMNS

def is_column_available(board, column):
    column_index = ord(column) - ord('A')
    return any(cell == ' ' for cell in board[0][column_index:column_index + 1])

def drop_checker(board, column, checker):
    column_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            break

def check_winner(board, player_checker):
    # Check horizontal, vertical and diagonal (both directions) for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS - 4 and all(board[row][col + i] == player_checker for i in range(4)) or
                row <= ROWS - 4 and all(board[row + i][col] == player_checker for i in range(4)) or
                col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == player_checker for i in range(4)) or
                col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == player_checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(CHECKERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column.")
            continue

        if not is_column_available(board, column):
            print("Column is fully occupied. Turn lost.")
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYER_COUNT]
            continue

        drop_checker(board, column, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYER_COUNT]

if __name__ == "__main__":
    main()
