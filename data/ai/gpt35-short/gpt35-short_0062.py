import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players allowed

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows if needed

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--'*COLS + '+')

def get_player_input(player, board):
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper()
        if choice not in COLUMN_LABELS:
            print("Invalid column. Please choose from A-G.")
            continue
        
        col = COLUMN_LABELS.index(choice)
        # Check if the column is full
        if board[0][col] != ' ':
            print("Column full. Choose another one.")
            continue
        
        return col

def drop_piece(board, col, player):
    # Start from bottom row and place piece in the first available slot
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, row, col, player):
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # horizontal, vertical, diagonal /
    for dr, dc in directions:
        count = 1  # count current piece
        
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If top row has no empty space, grid is full
    return all(space != ' ' for space in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Number of players must be between 2 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players -1)
    board = create_board()
    
    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_index]
        col = get_player_input(player, board)
        row, col = drop_piece(board, col, player)
        
        if check_win(board, row, col, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players
    
    print("Game over.")

if __name__ == "__main__":
    main()
