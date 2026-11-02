import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print("| " + " | ".join(row) + " |")
        print('+---' * COLUMNS + '+')

def is_valid_move(board, column):
    return column >= 0 and column < COLUMNS and board[0][column] == ' '

def apply_move(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_for_win(board, last_col, checker):
    def check_direction(start_row, start_col, d_row, d_col):
        count = 0
        row, col = start_row, start_col
        while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == checker:
            count += 1
            row += d_row
            col += d_col
        return count
    
    for d_row, d_col in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        count = 1  # include the last placed checker
        count += check_direction(row, last_col, d_row, d_col)
        count += check_direction(row, last_col, -d_row, -d_col)
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def get_column_input():
    while True:
        try:
            column = input("Please enter a column: ").upper()
            if len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1):
                return ord(column) - 65
        except ValueError:
            pass
        print("Invalid input. Please try again.")

def main():
    board = create_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = CHECKERS[current_player_idx]
        print(f"Player {current_checker}, it's your turn.")
        
        column = get_column_input()
        
        if is_valid_move(board, column):
            apply_move(board, column, current_checker)
            
            row = next(i for i, r in enumerate(board) if r[column] == current_checker)
            
            if check_for_win(board, column, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            
            if is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            
            current_player_idx = (current_player_idx + 1) % PLAYERS
        else:
            print("Column full. You lose a turn.")
        
        print_board(board)

if __name__ == "__main__":
    main()
