import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_headers = '  ' + '   '.join(chr(65 + i) for i in range(len(board[0])))
    print(column_headers)
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')

def get_random_first_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_input(input_str, columns):
    if len(input_str) != 1:
        return False
    if not ('A' <= input_str <= chr(65 + columns - 1)):
        return False
    return True

def place_checker(board, column, marker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = marker
            return row
    return -1

def check_for_win(board, last_row, last_col, marker):
    # Check horizontally
    count = 0
    for col in range(len(board[0])):
        count = count + 1 if board[last_row][col] == marker else 0
        if count >= 4:
            return True

    # Check vertically
    count = 0
    for row in range(len(board)):
        count = count + 1 if board[row][last_col] == marker else 0
        if count >= 4:
            return True

    # Check diagonally (\ direction)
    count = 0
    row, col = last_row, last_col
    while row >= 0 and col >= 0:
        if board[row][col] != marker:
            break
        row -= 1
        col -= 1
    row, col = row + 1, col + 1
    while row < len(board) and col < len(board[0]):
        count = count + 1 if board[row][col] == marker else 0
        if count >= 4:
            return True
        row += 1
        col += 1

    # Check diagonally (/ direction)
    count = 0
    row, col = last_row, last_col
    while row >= 0 and col < len(board[0]):
        if board[row][col] != marker:
            break
        row -= 1
        col += 1
    row, col = row + 1, col - 1
    while row < len(board) and col >= 0:
        count = count + 1 if board[row][col] == marker else 0
        if count >= 4:
            return True
        row += 1
        col -= 1

    return False

def check_for_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    num_players = NUM_PLAYERS
    player_markers = PLAYER_MARKERS[:num_players]

    current_player = get_random_first_player(num_players)
    print_board(board)

    while True:
        print(f"Player {player_markers[current_player]}, please enter a column:")
        user_input = input().strip()
        
        if not is_valid_input(user_input, COLUMNS):
            print("Invalid input. Try again.")
            continue
        
        column_index = ord(user_input) - 65
        row_index = place_checker(board, column_index, player_markers[current_player])
        
        if row_index == -1:
            print("Column full. Try a different column.")
            continue
        
        print_board(board)
        
        if check_for_win(board, row_index, column_index, player_markers[current_player]):
            print(f"Player {player_markers[current_player]} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
