import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(len(board[0]))))
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(' ' + cell + ' ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')

def get_column_input():
    while True:
        col = input("Please enter a column (A-G): ").upper()
        if len(col) == 1 and 'A' <= col <= chr(64 + COLUMNS):
            return ord(col) - 65
        print("Invalid input. Try again.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_winner(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != ' ':
                # Check horizontal
                if col <= COLUMNS - 4 and all(board[row][col + i] == board[row][col] for i in range(4)):
                    return board[row][col]
                # Check vertical
                if row <= ROWS - 4 and all(board[row + i][col] == board[row][col] for i in range(4)):
                    return board[row][col]
                # Check diagonal /
                if row <= ROWS - 4 and col >= 3 and all(board[row + i][col - i] == board[row][col] for i in range(4)):
                    return board[row][col]
                # Check diagonal \
                if row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                    return board[row][col]
    return None

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    print_board(board)
    current_player_index = random.randint(0, PLAYERS - 1)
    
    while True:
        print(f"Player {CHECKERS[current_player_index]}, it's your turn.")
        col = get_column_input()
        if not place_checker(board, col, CHECKERS[current_player_index]):
            print("Column is full. Turn lost.")
        else:
            print_board(board)
            winner = check_winner(board)
            if winner:
                print(f"Player {winner} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
