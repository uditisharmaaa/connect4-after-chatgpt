import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def display_board(board):
    os.system('clear')  # Clear the terminal screen
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print()

def is_valid_move(column, board):
    return column in COLUMN_LABELS and board[0][COLUMN_LABELS.index(column)] == ' '

def apply_move(column, player, board):
    col_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player
            break

def check_for_win(player, board):
    # Horizontal, vertical and diagonal checks
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row][c] == player for c in range(col, col + 4)):
                return True
    
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[r][col] == player for r in range(row, row + 4)):
                return True
    
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == player for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_valid_input():
    while True:
        column = input("Enter column (A-G): ").upper()
        if column in COLUMN_LABELS:
            return column
        print("Invalid input. Please enter a column between A and G.")

def main():
    board = initialize_board()
    num_players = min(max(int(input("Enter number of players (2-5): ")), 2), 5)
    players = PLAYERS[:num_players]
    current_player = random.choice(players)

    while True:
        display_board(board)
        print(f"Player {current_player}'s turn")
        column = get_valid_input()

        if is_valid_move(column, board):
            apply_move(column, current_player, board)
            if check_for_win(current_player, board):
                display_board(board)
                print(f"Player {current_player} wins!")
                break
            if check_for_draw(board):
                display_board(board)
                print("It's a draw!")
                break
            
            current_player = players[(players.index(current_player) + 1) % num_players]
        else:
            print("Column is full. Choose another column.")

if __name__ == '__main__':
    main()
