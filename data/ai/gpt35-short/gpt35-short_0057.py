import os
import random

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
MIN_PLAYERS = 2
MAX_PLAYERS = 5

def clear():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(' ' + ' '.join(COL_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('+' + '-+' * COLS)

def get_num_players():
    while True:
        try:
            num = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num <= MAX_PLAYERS:
                return num
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_move(player_token, board):
    while True:
        move = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if move in COL_LABELS:
            col = COL_LABELS.index(move)
            # Check if column is full
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full. Choose another one.")
        else:
            print("Invalid column. Please enter a letter from A to G.")

def make_move(board, col, player_token):
    # Place token in lowest empty spot in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_token
            return row, col

def check_win(board, row, col, player_token):
    # Directions to check: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If top row has no empty spaces, board is full (draw)
    return all(cell != ' ' for cell in board[0])

def main():
    clear()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_TOKENS[:num_players]
    random.shuffle(players)  # Random order of players
    print("Player order:", ' '.join(players))
    input("Press Enter to start the game...")
    
    board = create_board()
    current_index = 0
    
    while True:
        clear()
        print_board(board)
        player = players[current_index]
        col = get_move(player, board)
        row, col = make_move(board, col, player)
        
        if check_win(board, row, col, player):
            clear()
            print_board(board)
            print(f"Player {player} wins!")
            break
        elif check_draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        
        current_index = (current_index + 1) % num_players

if __name__ == "__main__":
    main()
