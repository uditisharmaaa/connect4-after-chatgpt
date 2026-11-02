import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Global variables
num_players = 2
players = []
current_player_index = 0
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board():
    print('  ' + '   '.join(chr(65+i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_column(col):
    return col in range(COLS) and board[0][col] == ' '

def get_valid_column_input():
    while True:
        col_letter = input(f'Player {players[current_player_index]}, please enter a column: ').strip().upper()
        if len(col_letter) == 1 and 'A' <= col_letter <= 'A'+chr(COLS-1):
            col = ord(col_letter) - ord('A')
            if is_valid_column(col):
                return col
        print('Invalid input. Please enter a valid column letter that is not full.')

def place_checker(col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = players[current_player_index]
            return row, col

def check_winner(row, col):
    def check_direction(dx, dy):
        count = 0
        for d in range(-3, 4):
            r, c = row + d * dx, col + d * dy
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == players[current_player_index]:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    return (check_direction(1, 0) or  # Vertical
            check_direction(0, 1) or  # Horizontal
            check_direction(1, 1) or  # Diagonal /
            check_direction(1, -1))   # Diagonal \

def is_draw():
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    global current_player_index
    while True:
        clear_screen()
        print_board()
        col = get_valid_column_input()
        row, col = place_checker(col)
        if check_winner(row, col):
            clear_screen()
            print_board()
            print(f'Player {players[current_player_index]} won!')
            break
        elif is_draw():
            clear_screen()
            print_board()
            print('The game is a draw!')
            break
        current_player_index = (current_player_index + 1) % num_players

def main():
    global num_players, players
    num_players = max(min(num_players, MAX_PLAYERS), MIN_PLAYERS)
    players = CHECKERS[:num_players]
    # Randomly select start player
    random.shuffle(players)
    play_game()

if __name__ == "__main__":
    main()
