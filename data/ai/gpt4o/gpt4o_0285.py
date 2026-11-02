import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LABELS))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

def is_valid_move(column, board):
    return column in COLUMN_LABELS and board[0][COLUMN_LABELS.index(column)] == ' '

def place_checker(checker, column, board):
    col_idx = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            break

def check_win(board):
    def check_line(line):
        return any(line[i:i+4] == [checker] * 4 for checker in CHECKERS for i in range(len(line) - 3))
    
    for row in board:
        if check_line(row):
            return True
    
    for col in range(COLUMNS):
        if check_line([board[row][col] for row in range(ROWS)]):
            return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if check_line([board[row + i][col + i] for i in range(4)]):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if check_line([board[row - i][col + i] for i in range(4)]):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        current_player = CHECKERS[current_player_idx]
        move = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if not is_valid_move(move, board):
            print("Invalid move! Try again.")
            continue

        place_checker(current_player, move, board)
        print_board(board)
        
        if check_win(board):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break
        
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
