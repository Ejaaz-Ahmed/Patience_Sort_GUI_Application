import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from typing import List, Optional
import random

class PatienceSortVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Patience Sort Algorithm - Step by Step Visualization")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')
        
        # Algorithm state
        self.original_array = []
        self.piles = []
        self.sorted_array = []
        self.current_index = 0
        self.current_element = 0
        self.target_pile = -1
        
        # Animation state
        self.is_running = False
        self.is_paused = False
        self.is_completed = False
        self.show_sorted = False
        self.animation_speed = 1500  # milliseconds
        
        # Animation phases
        self.PHASE_IDLE = "idle"
        self.PHASE_HIGHLIGHT = "highlight"
        self.PHASE_FIND_PILE = "find_pile"
        self.PHASE_PLACE = "place"
        self.PHASE_RECONSTRUCT = "reconstruct"
        self.current_phase = self.PHASE_IDLE
        
        # Colors
        self.colors = {
            'bg': '#1e1e2e',
            'card_bg': '#2d3748',
            'primary': '#4a90e2',
            'current': '#ff6b6b',
            'pile': '#63b3ed',
            'pile_top': '#ffd700',
            'sorted': '#90ee90',
            'highlight': '#ffa500',
            'text': '#ffffff',
            'text_dark': '#2d3748',
            'header_bg': '#2a2a3e',
            'accent': '#7c3aed'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container with scrollbar
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollable frame
        canvas_container = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas_container.yview)
        scrollable_frame = tk.Frame(canvas_container, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_container.configure(scrollregion=canvas_container.bbox("all"))
        )
        
        canvas_container.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_container.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas_container.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scrolling
        def _on_mousewheel(event):
            canvas_container.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas_container.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Stylish Header Frame
        header_frame = tk.Frame(scrollable_frame, bg=self.colors['header_bg'], relief=tk.RAISED, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Header content with better layout
        header_content = tk.Frame(header_frame, bg=self.colors['header_bg'])
        header_content.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        # Title
        title_label = tk.Label(
            header_content,
            text="PATIENCE SORT ALGORITHM VISUALIZATION",
            font=('Arial', 22, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['header_bg']
        )
        title_label.pack(pady=(0, 15))
        
        # Student and Supervisor Info - Fixed Layout
        info_container = tk.Frame(header_content, bg=self.colors['header_bg'])
        info_container.pack(fill=tk.X)
        
        # Left side - Students
        left_info = tk.Frame(info_container, bg=self.colors['header_bg'])
        left_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            left_info,
            text="DEVELOPED BY:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['header_bg']
        ).pack()
        
        tk.Label(
            left_info,
            text="Ejaz Ahmed",
            font=('Arial', 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['header_bg']
        ).pack(pady=(3, 0))
        
        # Right side - Supervisor
        right_info = tk.Frame(info_container, bg=self.colors['header_bg'])
        right_info.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        tk.Label(
            right_info,
            text="SUPERVISED BY:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['header_bg']
        ).pack()
        
        tk.Label(
            right_info,
            text="Dr. Mudassar Raza",
            font=('Arial', 14, 'bold'),
            fg=self.colors['highlight'],
            bg=self.colors['header_bg']
        ).pack(pady=(3, 0))
        
        # Decorative border
        border_frame = tk.Frame(header_frame, bg=self.colors['accent'], height=3)
        border_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Array Input Section
        input_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        input_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Array input label
        tk.Label(
            input_frame,
            text="🔢 Enter Array (minimum 10 elements, comma-separated):",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        ).pack(anchor=tk.W, pady=(0, 8))
        
        # Input frame container
        input_container = tk.Frame(input_frame, bg=self.colors['bg'])
        input_container.pack(fill=tk.X)
        
        # Array input field
        self.array_entry = tk.Entry(
            input_container,
            font=('Arial', 12),
            bg='white',
            fg=self.colors['text_dark'],
            insertbackground=self.colors['text_dark']
        )
        self.array_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
        
        # Generate random array button
        generate_btn = tk.Button(
            input_container,
            text="🎲 Generate Random",
            command=self.generate_random_array,
            font=('Arial', 10, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            padx=12,
            pady=6
        )
        generate_btn.pack(side=tk.LEFT, padx=3)
        
        # Set array button
        set_array_btn = tk.Button(
            input_container,
            text="✅ Set Array",
            command=self.set_custom_array,
            font=('Arial', 10, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=12,
            pady=6
        )
        set_array_btn.pack(side=tk.LEFT, padx=3)
        
        # Status label
        self.status_label = tk.Label(
            scrollable_frame,
            text="🚀 Ready to start! Enter an array (min 10 elements) and click 'Set Array' to begin.",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['bg'],
            wraplength=1100,
            justify=tk.LEFT
        )
        self.status_label.pack(pady=(0, 15), padx=5)
        
        # Control buttons
        control_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        control_frame.pack(pady=(0, 15))
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶️ Start",
            command=self.start_algorithm,
            font=('Arial', 11, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=18,
            pady=6,
            state=tk.DISABLED
        )
        self.start_btn.pack(side=tk.LEFT, padx=4)
        
        self.step_btn = tk.Button(
            control_frame,
            text="⏭️ Next Step",
            command=self.next_step,
            font=('Arial', 10),
            bg=self.colors['pile'],
            fg='white',
            padx=18,
            pady=6,
            state=tk.DISABLED
        )
        self.step_btn.pack(side=tk.LEFT, padx=4)
        
        self.pause_btn = tk.Button(
            control_frame,
            text="⏸️ Pause",
            command=self.toggle_pause,
            font=('Arial', 10),
            bg=self.colors['highlight'],
            fg='white',
            padx=18,
            pady=6,
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=4)
        
        reset_btn = tk.Button(
            control_frame,
            text="🔄 Reset",
            command=self.reset_algorithm,
            font=('Arial', 10),
            bg=self.colors['current'],
            fg='white',
            padx=18,
            pady=6
        )
        reset_btn.pack(side=tk.LEFT, padx=4)
        
        # Speed control
        speed_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        speed_frame.pack(side=tk.LEFT, padx=15)
        
        tk.Label(speed_frame, text="⚡ Speed:", bg=self.colors['bg'], fg=self.colors['text'], font=('Arial', 10)).pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="Normal")
        speed_combo = ttk.Combobox(
            speed_frame,
            textvariable=self.speed_var,
            values=["Slow", "Normal", "Fast"],
            state="readonly",
            width=8,
            font=('Arial', 9)
        )
        speed_combo.pack(side=tk.LEFT, padx=5)
        speed_combo.bind('<<ComboboxSelected>>', self.change_speed)
        
        # Visualization canvas - Make it scrollable vertically
        canvas_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            bg=self.colors['card_bg'],
            highlightthickness=1,
            highlightcolor=self.colors['accent'],
            height=700  # <-- Increase this value as needed
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        canvas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=canvas_scrollbar.set)
        
        # Update scrollregion after drawing
        def update_canvas_scrollregion(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind("<Configure>", update_canvas_scrollregion)
        
        # Algorithm description
        desc_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        desc_frame.pack(fill=tk.X, pady=10, padx=5)

        desc_text = ("📚 Algorithm: For each element, find the leftmost pile where the element is ≥ top element. "
                    "If no such pile exists, create a new pile. Finally, reconstruct by repeatedly taking "
                    "the smallest top element from all piles.")

        tk.Label(
            desc_frame,
            text=desc_text,
            font=('Arial', 10),
            fg=self.colors['text'],
            bg=self.colors['bg'],
            wraplength=1100,
            justify=tk.LEFT
        ).pack()

        # --- Add code display here ---
        code_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        code_frame.pack(fill=tk.X, pady=(0, 10), padx=5)

        self.code_lines = [
            "import bisect",
            "",
            "def patience_sort(arr):",
            "    piles = []",
            "",
            "    for x in arr:",
            "        idx = bisect.bisect_left([pile[-1] for pile in piles], x)",
            "        if idx == len(piles):",
            "            piles.append([x])",
            "        else:",
            "            piles[idx].append(x)",
            "",
            "    result = [item for pile in piles for item in pile]",
            "    return sorted(result)"
        ]
        self.code_text = tk.Text(
            code_frame,
            height=len(self.code_lines)+2,
            font=('Consolas', 12),
            bg="#232136",
            fg="#e0def4",
            bd=0,
            highlightthickness=0,
            wrap=tk.NONE
        )
        self.code_text.pack(fill=tk.X)
        self.code_text.insert(tk.END, "\n".join(self.code_lines))
        self.code_text.config(state=tk.DISABLED)
        
        # Initialize with empty state
        self.draw_visualization()
    
    def generate_random_array(self):
        """Generate a random array"""
        length = random.randint(10, 20)
        random_array = [random.randint(1, 99) for _ in range(length)]
        self.array_entry.delete(0, tk.END)
        self.array_entry.insert(0, ','.join(map(str, random_array)))
    
    def set_custom_array(self):
        """Set custom array from input"""
        try:
            array_text = self.array_entry.get().strip()
            if not array_text:
                messagebox.showerror("Error", "Please enter an array!")
                return
            
            # Parse the array
            array_elements = [int(x.strip()) for x in array_text.split(',')]
            
            # Validate minimum length
            if len(array_elements) < 10:
                messagebox.showerror("Error", f"Array must have at least 10 elements! You entered {len(array_elements)} elements.")
                return
            
            # Validate elements are positive integers
            if any(x <= 0 for x in array_elements):
                messagebox.showerror("Error", "All elements must be positive integers!")
                return
            
            # Set the array
            self.original_array = array_elements
            self.reset_algorithm()
            
            # Enable start button
            self.start_btn.config(state=tk.NORMAL)
            
            # Update status
            self.update_status(f"✅ Array set successfully! {len(array_elements)} elements ready for sorting.")
            
            # Draw visualization
            self.draw_visualization()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter comma-separated integers only.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def reset_algorithm(self):
        """Reset the algorithm to initial state"""
        self.piles = []
        self.sorted_array = []
        self.current_index = 0
        self.current_element = self.original_array[0] if self.original_array else 0
        self.target_pile = -1
        self.is_running = False
        self.is_paused = False
        self.is_completed = False
        self.show_sorted = False
        self.current_phase = self.PHASE_IDLE
        
        # Reset button states
        if self.original_array:
            self.start_btn.config(state=tk.NORMAL, text="▶️ Start")
        else:
            self.start_btn.config(state=tk.DISABLED, text="▶️ Start")
        self.step_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED, text="⏸️ Pause")
        
        if self.original_array:
            self.update_status(f"🔄 Algorithm reset! Array with {len(self.original_array)} elements ready. Click 'Start' to begin.")
        else:
            self.update_status("🚀 Ready to start! Enter an array (min 10 elements) and click 'Set Array' to begin.")
        self.draw_visualization()
    
    def start_algorithm(self):
        """Start or resume the algorithm"""
        if not self.original_array:
            messagebox.showerror("Error", "Please set an array first!")
            return
            
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.step_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.NORMAL)
            self.current_phase = self.PHASE_HIGHLIGHT
            self.auto_step()
        elif self.is_paused:
            self.toggle_pause()
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_btn.config(text="▶️ Resume")
        else:
            self.pause_btn.config(text="⏸️ Pause")
            self.auto_step()
    
    def change_speed(self, event=None):
        """Change animation speed"""
        speed_map = {"Slow": 2500, "Normal": 1500, "Fast": 800}
        self.animation_speed = speed_map[self.speed_var.get()]
    
    def next_step(self):
        """Execute next step of the algorithm"""
        if not self.original_array:
            return

        # Highlight the for loop line
        self.highlight_code_line(5)  # "for x in arr:"

        if self.is_completed and not self.show_sorted:
            self.reconstruct_sorted_array()
            return

        if self.is_completed:
            return

        if self.current_index >= len(self.original_array):
            self.is_completed = True
            self.current_phase = self.PHASE_IDLE
            self.update_status("📋 Phase 1 Complete! All elements placed in piles. Click 'Next Step' to reconstruct sorted array.")
            self.draw_visualization()
            return

        if self.current_phase == self.PHASE_HIGHLIGHT:
            self.current_element = self.original_array[self.current_index]
            self.current_phase = self.PHASE_FIND_PILE
            self.update_status(f"🔍 Step {self.current_index + 1}/{len(self.original_array)}: Processing element {self.current_element}")
            self.highlight_code_line(6)  # "idx = bisect.bisect_left..."

        elif self.current_phase == self.PHASE_FIND_PILE:
            self.find_target_pile()
            self.current_phase = self.PHASE_PLACE
            self.highlight_code_line(7)  # "if idx == len(piles):"
            if self.target_pile == -1:
                self.update_status(f"🆕 No suitable pile found for {self.current_element}. Creating new pile.")
            else:
                self.update_status(f"🎯 Found suitable pile {self.target_pile + 1} for element {self.current_element}.")

        elif self.current_phase == self.PHASE_PLACE:
            self.place_element()
            self.current_index += 1
            if self.current_index < len(self.original_array):
                self.current_phase = self.PHASE_HIGHLIGHT
            else:
                self.is_completed = True
                self.current_phase = self.PHASE_IDLE
                self.update_status("📋 Phase 1 Complete! All elements placed in piles. Click 'Next Step' to reconstruct sorted array.")

        self.draw_visualization()

    def find_target_pile(self):
        """Find the target pile for current element"""
        self.target_pile = -1
        for i, pile in enumerate(self.piles):
            if pile[-1] >= self.current_element:
                self.target_pile = i
                break
    
    def place_element(self):
        """Place current element in appropriate pile"""
        if self.target_pile == -1:
            self.piles.append([self.current_element])
            self.highlight_code_line(8)  # "piles.append([x])"
        else:
            self.piles[self.target_pile].append(self.current_element)
            self.highlight_code_line(10)  # "piles[idx].append(x)"
        self.target_pile = -1
    
    def reconstruct_sorted_array(self):
        """Reconstruct sorted array from piles"""
        self.current_phase = self.PHASE_RECONSTRUCT
        self.update_status("🔄 Reconstructing sorted sequence by taking smallest top elements...")
        self.highlight_code_line(12)  # "result = [item for pile in piles for item in pile]"

        temp_piles = [pile.copy() for pile in self.piles]
        self.sorted_array = []

        while any(pile for pile in temp_piles):
            min_val = float('inf')
            min_pile = -1

            for i, pile in enumerate(temp_piles):
                if pile and pile[-1] < min_val:
                    min_val = pile[-1]
                    min_pile = i

            if min_pile != -1:
                self.sorted_array.append(temp_piles[min_pile].pop())

        self.show_sorted = True
        self.current_phase = self.PHASE_IDLE
        self.update_status("🎉 Algorithm Complete! Sorted array has been reconstructed from the piles.")
        self.start_btn.config(text="✅ Completed", state=tk.DISABLED)
        self.step_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.highlight_code_line(13)  # "return sorted(result)"
        self.draw_visualization()
    
    def auto_step(self):
        """Automatically execute next step with delay"""
        if not self.is_running or self.is_paused or self.is_completed:
            return
        
        self.next_step()
        
        if self.is_running and not self.is_paused and not self.is_completed:
            self.root.after(self.animation_speed, self.auto_step)
        elif self.is_completed and not self.show_sorted:
            self.root.after(self.animation_speed, self.reconstruct_sorted_array)
    
    def update_status(self, message: str):
        """Update status message"""
        self.status_label.config(text=message)
    
    def draw_visualization(self):
        """Draw the complete visualization"""
        self.canvas.delete("all")

        if not self.original_array:
            self.canvas.create_text(
                575, 250,
                text="Enter an array to begin visualization\n(Minimum 10 elements required)",
                font=('Arial', 18, 'bold'),
                fill=self.colors['text'],
                justify=tk.CENTER
            )
            return

        # Draw original array
        self.draw_original_array()

        # Draw piles and get the bottom Y position
        piles_bottom_y = 180
        if self.piles:
            piles_bottom_y = self.draw_piles()

        # Draw sorted array below the piles
        if self.show_sorted:
            self.draw_sorted_array(start_y=piles_bottom_y)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def draw_original_array(self):
        """Draw the original input array"""
        if not self.original_array:
            return
            
        start_x = 30
        start_y = 40
        box_width = min(50, (1090 - 60) // len(self.original_array))  # Adjust width based on array size
        box_height = 35
        spacing = 3
        
        # Calculate actual width needed
        total_width = len(self.original_array) * (box_width + spacing) - spacing
        if total_width > 1090:
            # If too wide, make multiple rows
            elements_per_row = 1090 // (box_width + spacing)
            rows = (len(self.original_array) + elements_per_row - 1) // elements_per_row
        else:
            elements_per_row = len(self.original_array)
            rows = 1
        
        # Label
        self.canvas.create_text(
            start_x, start_y - 18,
            text=f"Input Array ({len(self.original_array)} elements):",
            font=('Arial', 12, 'bold'),
            fill=self.colors['text'],
            anchor=tk.W
        )
        
        for i, value in enumerate(self.original_array):
            row = i // elements_per_row
            col = i % elements_per_row
            x = start_x + col * (box_width + spacing)
            y = start_y + row * (box_height + spacing + 3)
            
            # Determine color
            if i == self.current_index and self.current_phase in [self.PHASE_HIGHLIGHT, self.PHASE_FIND_PILE]:
                color = self.colors['current']
                text_color = 'white'
            elif i < self.current_index:
                color = '#666666'  # Processed
                text_color = 'white'
            else:
                color = self.colors['primary']
                text_color = 'white'
            
            # Draw box
            self.canvas.create_rectangle(
                x, y, x + box_width, y + box_height,
                fill=color,
                outline='white',
                width=2
            )
            
            # Draw value
            self.canvas.create_text(
                x + box_width // 2, y + box_height // 2,
                text=str(value),
                font=('Arial', min(14, box_width // 3), 'bold'),
                fill=text_color
            )
    
    def draw_piles(self):
        """Draw the piles and return the bottom Y position"""
        if not self.piles:
            return 180  # Default start_y if no piles

        start_x = 30
        start_y = 180
        box_width = min(45, (1090 - 60) // len(self.piles))
        box_height = 30
        pile_spacing = box_width + 15

        max_pile_height = 0

        # Label
        self.canvas.create_text(
            start_x, start_y - 18,
            text=f"Piles ({len(self.piles)} piles):",
            font=('Arial', 12, 'bold'),
            fill=self.colors['text'],
            anchor=tk.W
        )

        for pile_idx, pile in enumerate(self.piles):
            x = start_x + pile_idx * pile_spacing
            pile_height = len(pile) * (box_height + 2)
            if pile_height > max_pile_height:
                max_pile_height = pile_height

            # Pile number
            self.canvas.create_text(
                x + box_width // 2, start_y - 5,
                text=f"P{pile_idx + 1}",
                font=('Arial', 10),
                fill=self.colors['text']
            )

            # Highlight target pile
            if pile_idx == self.target_pile and self.current_phase == self.PHASE_FIND_PILE:
                highlight_height = len(pile) * (box_height + 2) + 8
                self.canvas.create_rectangle(
                    x - 3, start_y - 3,
                    x + box_width + 3, start_y + highlight_height,
                    fill='',
                    outline=self.colors['highlight'],
                    width=3
                )

            # Draw pile elements (bottom to top)
            for elem_idx, value in enumerate(pile):
                y = start_y + (len(pile) - 1 - elem_idx) * (box_height + 2)
                if elem_idx == len(pile) - 1:
                    color = self.colors['pile_top']
                    text_color = self.colors['text_dark']
                else:
                    color = self.colors['pile']
                    text_color = 'white'
                self.canvas.create_rectangle(
                    x, y, x + box_width, y + box_height,
                    fill=color,
                    outline='white',
                    width=2
                )
                self.canvas.create_text(
                    x + box_width // 2, y + box_height // 2,
                    text=str(value),
                    font=('Arial', min(12, box_width // 4), 'bold'),
                    fill=text_color
                )

        # Return the Y position just below the tallest pile
        return start_y + max_pile_height + 30  # +30 for spacing
    
    def draw_sorted_array(self, start_y=400):
        """Draw the final sorted array below the piles"""
        if not self.sorted_array:
            return

        start_x = 30
        box_width = min(50, (1090 - 60) // len(self.sorted_array))
        box_height = 35
        spacing = 3

        elements_per_row = 1090 // (box_width + spacing)
        if len(self.sorted_array) > elements_per_row:
            elements_per_row = elements_per_row
        else:
            elements_per_row = len(self.sorted_array)

        # Label
        self.canvas.create_text(
            start_x, start_y - 18,
            text=f"Sorted Result ({len(self.sorted_array)} elements):",
            font=('Arial', 12, 'bold'),
            fill=self.colors['text'],
            anchor=tk.W
        )

        for i, value in enumerate(self.sorted_array):
            row = i // elements_per_row
            col = i % elements_per_row
            x = start_x + col * (box_width + spacing)
            y = start_y + row * (box_height + spacing + 3)

            self.canvas.create_rectangle(
                x, y, x + box_width, y + box_height,
                fill=self.colors['sorted'],
                outline='white',
                width=2
            )
            self.canvas.create_text(
                x + box_width // 2, y + box_height // 2,
                text=str(value),
                font=('Arial', min(14, box_width // 3), 'bold'),
                fill=self.colors['text_dark']
            )
    
    def run(self):
        """Start the GUI application"""
        self.draw_visualization()
        self.root.mainloop()

    def highlight_code_line(self, line_idx):
        """Highlight a specific line in the code display"""
        self.code_text.config(state=tk.NORMAL)
        self.code_text.tag_remove("highlight", "1.0", tk.END)
        self.code_text.tag_configure("highlight", background="#ffd700", foreground="#232136")
        self.code_text.tag_add("highlight", f"{line_idx+1}.0", f"{line_idx+1}.end")
        self.code_text.config(state=tk.DISABLED)

def main():
    """Main function to run the visualizer"""
    try:
        app = PatienceSortVisualizer()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()