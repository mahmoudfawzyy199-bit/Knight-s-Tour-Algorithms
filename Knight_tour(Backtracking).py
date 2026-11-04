import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import queue


# ============================================================================
# BACKTRACKING ALGORITHM 
# ============================================================================

class KnightsTourBacktrack:
    """Backtracking algorithm with cancellation"""
    
    def __init__(self, size):
        self.size = size
        self.board = None
        self.row = 0
        self.col = 0
        
    def initialize(self, start_row, start_col):
        """Initialize board with start position"""
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.row = start_row
        self.col = start_col
        self.board[self.row][self.col] = 1
    
    def print_board(self):
        """Print solution"""
        for row in self.board:
            print(row)
    
    def is_valid_move(self, next_row, next_col):
        """Check if next step is valid or not"""
        if (next_row >= 0 and next_row < self.size and 
            next_col >= 0 and next_col < self.size and 
            self.board[next_row][next_col] == 0):
            return True
        return False
    
    def get_next_step(self, move, row, col):
        """Get next position"""
        row_moves = (-2, -1, 1, 2, 2, 1, -1, -2)
        col_moves = (1, 2, 2, 1, -1, -2, -2, -1)
        next_row = row + row_moves[move]
        next_col = col + col_moves[move]
        return (next_row, next_col)
    
    def solve_backtrack(self, step, row, col, callback=None, should_continue=lambda: True, delay=0):
        """This Backtracking"""
        if not should_continue():
            return False
        if step == self.size * self.size + 1:  # Base Case
            return True
        
        for move in range(8):  # loop in range(8) because Knight has 8 available moves
            # Check cancellation more frequently - BEFORE getting next position
            if not should_continue():
                return False
                
            next_row, next_col = self.get_next_step(move, row, col)  # Get Next Position
            
            # Check cancellation again after getting next position
            if not should_continue():
                return False
                
            if self.is_valid_move(next_row, next_col):  # Check if is valid or not
                self.board[next_row][next_col] = step  # Assign the move on the board
                
                # Callback for visualization
                if callback:
                    callback(self.board, (next_row, next_col))
                    if delay > 0:
                        time.sleep(delay / 1000.0)
                
                # Check cancellation before recursive call
                if not should_continue():
                    self.board[next_row][next_col] = 0  # Clean up
                    return False
                
                if self.solve_backtrack(step + 1, next_row, next_col, callback, should_continue, delay):  # Recursively try to complete
                    return True  # Return true to last solve_backtrack call
                
                # if it can not complete from last solve_backtrack it backtrack
                self.board[next_row][next_col] = 0  # Backtracking: undo the move
                
                # Callback for visualization after backtracking
                if callback:
                    callback(self.board, (row, col))  # Show backtracked state
                    if delay > 0:
                        time.sleep(delay / 1000.0)
            
            # Check cancellation between moves
            if not should_continue():
                return False
        
        return False  # Return false if all 8 moves checks and is not valid
    
    def solve(self, start_row, start_col, callback=None, should_continue=lambda: True, delay=0):
        """Solve the tour by calling solve_backtrack method"""
        self.initialize(start_row, start_col)
        
        # Check cancellation before starting
        if not should_continue():
            return False
        
        # Show initial state
        if callback:
            callback(self.board, (start_row, start_col))
            if delay > 0:
                time.sleep(delay / 1000.0)
        
        # Check cancellation after showing initial state
        if not should_continue():
            return False
        
        # Call solve_backtrack method
        return self.solve_backtrack(2, start_row, start_col, callback, should_continue, delay)


# ============================================================================
#  Cultural Algorithm
# ============================================================================

class KnightsTourCultural:
    """Cultural Algorithm (faster than backtracking)"""
    
    #--------------------------------------------------------
    # Implementation Code
    #--------------------------------------------------------
    
     


# ============================================================================
# GUI CLASS WITH ALGORITHM SELECTION
# ============================================================================

class KnightTourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour Solver - Choose Algorithm")
        self.root.geometry("750x800")

        # State
        self.size = 8
        self.cell_size = 60
        self.solver = None
        self.solving = False
        self.delay = 100
        self.current_algorithm = "backtrack"
        self.gui_queue = queue.Queue()

        # Colors
        self.light_square = "#F0D9B5"
        self.dark_square = "#B58863"
        self.path_color = "#4ECDC4"
        self.current_color = "#FF6B6B"

        self.setup_ui()
        self.initialize_board()
        self.setup_thread_safety()

    def setup_thread_safety(self):
        """Set up periodic checking for thread-safe GUI updates"""
        def process_queue():
            try:
                while True:
                    callback = self.gui_queue.get_nowait()
                    callback()
            except queue.Empty:
                pass
            self.root.after(100, process_queue)
        
        self.root.after(100, process_queue)

    def safe_gui_update(self, callback):
        """Safely update GUI from any thread"""
        self.gui_queue.put(callback)

    def setup_ui(self):
        # Main control frame
        top = tk.Frame(self.root)
        top.pack(pady=8)

        # Board size
        tk.Label(top, text="Board Size:").grid(row=0, column=0, padx=2)
        self.size_var = tk.StringVar(value="8")
        tk.Entry(top, textvariable=self.size_var, width=5).grid(row=0, column=1, padx=2)

        # Start position
        tk.Label(top, text="Start Row:").grid(row=0, column=2, padx=2)
        self.start_row = tk.StringVar(value="0")
        tk.Entry(top, textvariable=self.start_row, width=5).grid(row=0, column=3, padx=2)

        tk.Label(top, text="Start Col:").grid(row=0, column=4, padx=2)
        self.start_col = tk.StringVar(value="0")
        tk.Entry(top, textvariable=self.start_col, width=5).grid(row=0, column=5, padx=2)

        # Speed control
        tk.Label(top, text="Speed:").grid(row=0, column=6, padx=2)
        self.speed_var = tk.StringVar(value="100")
        speed_scale = tk.Scale(top, from_=10, to=500, orient=tk.HORIZONTAL, 
                              variable=self.speed_var, showvalue=False, width=10, length=80)
        speed_scale.grid(row=0, column=7, padx=2)
        tk.Label(top, textvariable=self.speed_var).grid(row=0, column=8, padx=2)

        # Algorithm selection frame
        algo_frame = tk.LabelFrame(self.root, text="Choose Algorithm", padx=10, pady=10)
        algo_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Algorithm selection using Combobox (dropdown)
        tk.Label(algo_frame, text="Algorithm:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.algo_var = tk.StringVar(value="Backtracking")
        self.algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var, 
                                     state="readonly", width=25)
        self.algo_combo['values'] = ("Backtracking", "Cultural")
        self.algo_combo.pack(side=tk.LEFT, padx=5)
        self.algo_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)
        
        # Algorithm description label
        self.algo_desc = tk.Label(algo_frame, text="", font=("Arial", 9), fg="blue")
        self.algo_desc.pack(side=tk.LEFT, padx=10)
        
        # Update description for default algorithm
        self.update_algorithm_description()

        # Button frame
        btns = tk.Frame(self.root)
        btns.pack(pady=6)

        self.solve_btn = tk.Button(btns, text="Solve (animate)", command=self.start_solve_thread)
        self.solve_btn.pack(side=tk.LEFT, padx=6)

        self.cancel_btn = tk.Button(btns, text="Cancel", command=self.cancel_solve, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=6)

        self.reset_btn = tk.Button(btns, text="Reset", command=self.reset_board)
        self.reset_btn.pack(side=tk.LEFT, padx=6)

        self.full_btn = tk.Button(btns, text="Full Solution", command=self.start_full_solution_thread)
        self.full_btn.pack(side=tk.LEFT, padx=6)

        # Status labels
        self.status = tk.Label(self.root, text="Ready", font=("Arial", 10))
        self.status.pack(pady=6)

        self.stats_label = tk.Label(self.root, text="", font=("Arial", 9))
        self.stats_label.pack(pady=2)

        # Canvas for board
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack(pady=6)

        # Load knight image
        self.knight_img = self.load_knight_image()

    def on_algorithm_change(self, event=None):
        """Handle algorithm selection change"""
        self.update_algorithm_description()
        
    def update_algorithm_description(self):
        """Update the description based on selected algorithm"""
        algo = self.algo_var.get()
        if algo == "Backtracking":
            self.algo_desc.config(text="Basic backtracking - tries all moves systematically")
            self.current_algorithm = "backtrack"
        elif algo == "Cultural":
            self.algo_desc.config(text="Cultural - ")
            self.current_algorithm = "Cultural"

    def load_knight_image(self):
        """load knight image"""
        try:
            return tk.PhotoImage(file="knight.png")
        except Exception:
            return None

    def initialize_board(self):
        """Initialize or reset the board"""
        try:
            s = int(self.size_var.get())
            if s < 3 or s > 16:
                raise ValueError("size out of range")
        except Exception:
            messagebox.showerror("Error", "Invalid board size (3-16). Using 8.")
            s = 8
            self.size_var.set("8")

        self.size = s
        self.cell_size = max(20, 500 // self.size)
        self.canvas.config(width=self.cell_size * self.size, height=self.cell_size * self.size)
        
        # Create solver instance based on selected algorithm
        self.create_solver()
        
        # Draw empty board
        self.draw_board(None, (0, 0))

    def create_solver(self):
        """Create solver instance based on selected algorithm"""
        if self.current_algorithm == "backtrack":
            self.solver = KnightsTourBacktrack(self.size)
        elif self.current_algorithm == "cultural":
            self.solver = KnightsTourCultural(self.size)
        else:
            self.solver = KnightsTourBacktrack(self.size)

    def draw_board(self, board, knight_pos):
        """Draw the chess board based on solver state"""
        self.canvas.delete("all")
        
        # Draw squares
        for r in range(self.size):
            for c in range(self.size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = self.light_square if (r + c) % 2 == 0 else self.dark_square
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                
                # Draw move number if exists
                if board and board[r][c] != 0:
                    fill_color = self.current_color if (r, c) == knight_pos else self.path_color
                    self.canvas.create_text(
                        x1 + self.cell_size // 2,
                        y1 + self.cell_size // 2,
                        text=str(board[r][c]),
                        font=("Arial", max(8, self.cell_size // 4), "bold"),
                        fill=fill_color
                    )
        
        # Draw knight
        self.draw_knight(knight_pos)

    def draw_knight(self, knight_pos):
        """Draw knight at given position"""
        kr, kc = knight_pos
        x = kc * self.cell_size + self.cell_size // 2
        y = kr * self.cell_size + self.cell_size // 2
        
        if self.knight_img:
            self.canvas.create_image(x, y, image=self.knight_img)
        else:
            size = self.cell_size // 3
            self.canvas.create_text(x, y, text="♞", 
                                  font=("Arial", size, "bold"), 
                                  fill="#2C3E50")

    # Thread management
    def start_solve_thread(self):
        if self.solving:
            return
        self.initialize_board() 
        self.solving = True
        
        # Update solver based on current algorithm selection
        self.create_solver()
        
        t = threading.Thread(target=self.solve_tour_with_animation)
        t.daemon = True
        t.start()

    def start_full_solution_thread(self):
        if self.solving:
            return
        self.initialize_board() 
        self.solving = True
        
        # Update solver based on current algorithm selection
        self.create_solver()
        
        t = threading.Thread(target=self.solve_tour_without_animation)
        t.daemon = True
        t.start()

    def solve_tour_with_animation(self):
        """Solve with animation using selected algorithm"""
        try:
            r = int(self.start_row.get())
            c = int(self.start_col.get())
            if not (0 <= r < self.size and 0 <= c < self.size):
                raise ValueError
        except Exception:
            self.safe_gui_update(lambda: messagebox.showerror("Error", "Invalid start position"))
            self.solving = False
            return

        # Update UI
        self.delay = max(10, min(1000, int(self.speed_var.get())))
        algo_name = self.algo_var.get()
        self.safe_gui_update(lambda: self.status.config(
            text=f"Solving with {algo_name} (animated)..."
        ))
        self.safe_gui_update(lambda: self.solve_btn.config(state=tk.DISABLED))
        self.safe_gui_update(lambda: self.cancel_btn.config(state=tk.NORMAL))
        self.safe_gui_update(lambda: self.full_btn.config(state=tk.DISABLED))
        
        # Draw initial board
        initial_board = [[0] * self.size for _ in range(self.size)]
        initial_board[r][c] = 1
        self.safe_gui_update(lambda: self.draw_board(initial_board, (r, c)))

        start_time = time.time()
        
        # Define callback for GUI updates
        def update_gui(board, knight_pos):
            self.safe_gui_update(lambda: self.draw_board(board, knight_pos))
        
        # Define continuation check - MORE FREQUENT UPDATES
        def should_continue():
            return self.solving
        
        # CALL THE SELECTED ALGORITHM
        success = self.solver.solve(
            start_row=r,
            start_col=c,
            callback=update_gui,
            should_continue=should_continue,
            delay=self.delay
        )
        
        solve_time = time.time() - start_time
        self.solving = False

        # Update results
        def update_results():
            self.solve_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.full_btn.config(state=tk.NORMAL)
            
            if success:
                # Get board from solver
                board = self.solver.board if hasattr(self.solver, 'board') else None
                knight_pos = self.solver.current_pos if hasattr(self.solver, 'current_pos') else (r, c)
                self.draw_board(board, knight_pos)
                self.status.config(text=f"{algo_name} solution found! Time: {solve_time:.2f}s")
                self.stats_label.config(text=f"Board: {self.size}x{self.size}, Start: ({r},{c}), Algorithm: {algo_name}")
            else:
                if not self.solving:  # Only show "No solution" if not cancelled
                    self.status.config(text="No solution found")
                    self.stats_label.config(text="")
                else:
                    self.status.config(text="Solving cancelled")
                    self.stats_label.config(text="")
        
        self.safe_gui_update(update_results)

    def solve_tour_without_animation(self):
        """Solve without animation using selected algorithm"""
        try:
            r = int(self.start_row.get())
            c = int(self.start_col.get())
            if not (0 <= r < self.size and 0 <= c < self.size):
                raise ValueError
        except Exception:
            self.safe_gui_update(lambda: messagebox.showerror("Error", "Invalid start position"))
            self.solving = False
            return

        # Update UI
        algo_name = self.algo_var.get()
        self.safe_gui_update(lambda: self.status.config(
            text=f"Finding solution with {algo_name}..."
        ))
        self.safe_gui_update(lambda: self.solve_btn.config(state=tk.DISABLED))
        self.safe_gui_update(lambda: self.full_btn.config(state=tk.DISABLED))
        
        initial_board = [[0] * self.size for _ in range(self.size)]
        initial_board[r][c] = 1
        self.safe_gui_update(lambda: self.draw_board(initial_board, (r, c)))

        start_time = time.time()
        
        # CALL THE SELECTED ALGORITHM (no animation)
        success = self.solver.solve(r, c, delay=0)
        
        solve_time = time.time() - start_time
        self.solving = False

        def update_full_results():
            self.solve_btn.config(state=tk.NORMAL)
            self.full_btn.config(state=tk.NORMAL)
            
            if success:
                board = self.solver.board if hasattr(self.solver, 'board') else None
                knight_pos = self.solver.current_pos if hasattr(self.solver, 'current_pos') else (r, c)
                self.draw_board(board, knight_pos)
                self.status.config(text=f"{algo_name} solution ready! Time: {solve_time:.2f}s")
                self.stats_label.config(text=f"Board: {self.size}x{self.size}, Start: ({r},{c}), Algorithm: {algo_name}")
            else:
                if not self.solving:  # Only show "No solution" if not cancelled
                    self.status.config(text="No solution found")
                    self.stats_label.config(text="")
                else:
                    self.status.config(text="Solving cancelled")
                    self.stats_label.config(text="")

        self.safe_gui_update(update_full_results)

    def cancel_solve(self):
        """Cancel the current solving process - IMMEDIATE"""
        self.solving = False
        self.safe_gui_update(lambda: self.status.config(text="Cancelling..."))
        self.safe_gui_update(lambda: self.cancel_btn.config(state=tk.DISABLED))
        # Don't enable other buttons yet - wait for algorithm to actually stop

    def reset_board(self):
        """Reset the board to initial state"""
        self.solving = False
        self.initialize_board()
        self.status.config(text="Ready")
        self.stats_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = KnightTourGUI(root)
    root.mainloop()