import random
import os

# CONSTANTS
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  A   B   C   D   E   F   G")
    print(" " + "---+" * 6 + "---")
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n " + "---+" * 6 + "---")
    print()

def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        choice = input(f"Player {player}, enter column (A-G): ").upper().strip()
        
        if len(choice) != 1 or choice not in 'ABCDEFG':
            print("Invalid input! Please enter a letter from A to G.")
            continue
        
        col_index = ord(choice) - ord('A')
        return col_index

def drop_piece(board, col, player):
    """Drop a piece in the specified column. Returns row index or -1 if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    moves = 0
    max_moves = ROWS * COLS
    
    while moves < max_moves:
        current_player = players[current_player_index]
        print_board(board)
        
        # Get valid column input
        while True:
            col = get_column_input(current_player)
            row = drop_piece(board, col, current_player)
            
            if row == -1:
                print("Column is full! Choose another column.")
            else:
                break
        
        moves += 1
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            return
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            return
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Run the game with option to play again."""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
