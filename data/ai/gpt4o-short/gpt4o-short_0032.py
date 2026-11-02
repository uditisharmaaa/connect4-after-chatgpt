import random
import os

# Constants for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Set number of players (between 2 to 5)

# Board dimensions and labels
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def display_board(board):
    os.system('clear')
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLUMNS + 1))

def get_move():
    while True:
        move = input("Enter a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        print("Invalid input. Please enter a column labeled A-G.")

def is_valid_move(board, column):
    return board[0][column] == ' '

def apply_move(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            break

def check_win(board, player):
    # Check horizontal, vertical, and diagonal for a win
    def check_direction(row, col, d_row, d_col):
        count = 0
        for _ in range(4):
            if 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == player:
                count += 1
                row += d_row
                col += d_col
            else:
                break
        return count == 4

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                # Horizontal, vertical, diagonal /
                if any(check_direction(row, col, d_row, d_col)
                       for d_row, d_col in [(0, 1), (1, 0), (1, 1), (1, -1)]):
                    return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        current_player = PLAYERS[current_player_index]
        display_board(board)
        
        print(f"Player {current_player}'s turn.")
        
        while True:
            column = get_move()
            if is_valid_move(board, column):
                apply_move(board, column, current_player)
                break
            else:
                print("Column full. Try again.")

        if check_win(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            display_board(board)
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
