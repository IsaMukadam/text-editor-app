# GapBuffer Class: @IsaMukadam
class GapBuffer:
    """
    A gap buffer data structure used for efficient text editing operations.

    The gap buffer maintains a 'gap' at the cursor position within a fixed-size buffer.
    Insertions occur at the gap, and cursor movement adjusts the gap position,
    minimising the number of memory operations compared to standard lists or strings.
    """
    def __init__(self, initial_size=100):
        """
        Initialise the gap buffer.

        Args:
            initial_size (int): Intial size of the underlying buffer.
        """
        # Basic functionality:
        self.buffer = [''] * initial_size
        self.gap_start = 0
        self.gap_end = initial_size
        self.size = initial_size
        # Selection functionality
        self.selection_start = None
        self.selection_end = None
        # Unde/Redo functionality:
        self.undo_stack = []
        self.redo_stack = []

    ########################## BASIC GAPBUFFER FUNCTIONALITY ###########################

    def resize(self, new_size= int) -> None:
        """
        Resize the buffer to at least `new_size`. The gap is preserved during resizing.

        Args:
            new_size (int): The desired minimum size of the buffer.

        Returns:
            None
        """
        if new_size <= len(self.buffer):
            return
        
        new_buffer = [''] * new_size
        # Copy text before gap
        new_buffer[:self.gap_start] = self.buffer[:self.gap_start]
        # Copy text after gap
        after_gap_length = len(self.buffer) - self.gap_end
        new_buffer[new_size - after_gap_length:] = self.buffer[self.gap_end:]
        # Update gap_end to new location after resizing
        self.gap_end = new_size - after_gap_length
        self.buffer = new_buffer
    

    def insert(self, text: str) -> None:
        """
        Insert a string of text at the current cursor (gap start) position.

        If the gap is not large enough to hold the new text, the buffer is resized.

        Args:
            text (str): The text to insert.

        Returns:
            None
        """
        for char in text:
            if self.gap_start == self.gap_end:
                self.resize(len(self.buffer) * 2)
            self.buffer[self.gap_start] = char
            self.gap_start += 1 


    def get_text(self) -> str:
        """
        Retrieve the current text in the buffer, excluding the gap.

        Returns:
            str: The full visible text in the buffer.
        """
        return ''.join(self.buffer[:self.gap_start] + self.buffer[self.gap_end:])
    

    def move_cursor(self, position: int) -> None:
        """
        Move the cursor (gap) to the specified position in the text.

        Args:
            position(int): The new cursor position.

        Raises:
            ValueError: If position is out of bounds.
        """
        # Ensure the new cursor position is within valid bounds (0 to size inclusive)
        if not 0 <= position <= self.size:
            raise ValueError("Cursor position out of bounds")

        # Case 1: Move the gap to the left (cursor is before current gap start)
        if position < self.gap_start:
            # Shift characters from before the gap into the gap space, one by one
            while self.gap_start > position:
                self.gap_start -= 1               # Move gap_start one step left
                self.gap_end -= 1                 # Move gap_end one step left
                self.buffer[self.gap_end] = self.buffer[self.gap_start]  # Copy char to the right side
                self.buffer[self.gap_start] = ''  # Clear original position

        # Case 2: Move the gap to the right (cursor is after current gap start)
        elif position > self.gap_start:
            # Shift characters from after the gap into the gap space, one by one
            while self.gap_start < position:
                self.buffer[self.gap_start] = self.buffer[self.gap_end]  # Copy char from right into left
                self.buffer[self.gap_end] = ''      # Clear original right-side char
                self.gap_start += 1                 # Move gap_start one step right
                self.gap_end += 1                   # Move gap_end one step right



    def delete(self, count: int = 1) -> None:
        """
        Delete a number of characters after the cursor (i.e. from the right side of the gap).

        Args:
            count (int): Number of characters to delete. Default is 1.

        Raises:
            ValueError: If trying to delete more characters than available
        """
        available = len(self.buffer) - self.gap_end
        if count < 0 or count > available:
            raise ValueError("Invalid delete count")
        
        for _ in range(count):
            self.buffer[self.gap_end] = ''
            self.gap_end += 1

    ########################## SELECTION GAPBUFFER FUNCTIONALITY ###########################

    def select(self, start: int, end: int) -> None:
        """
        Select a range of text from start to end (non-inclusive).

        Args:
            start (int): Starting index of selection.
            end (int): Ending index (exclusive).

        Raises:
            ValueError: If selection range is invalid.
        """
        if not (0 <= start <= end <= self.size):
            raise ValueError("Invalid selection range")
        
        self.selection_start = start
        self.selection_end = end

    def get_selection(self) -> str:
        """
        Return the currently selected text.

        Returns:
            str: The selected substring, or an empty string if none selected.
        """
        if self.selection_start is None or self.selection_end is None:
            return ''
        
        text = self.get_text()
        return text[self.select_start:self.selection_end]
    
    def delete_selection(self) -> None:
        """
        Delete the currently selected text.

        Returns:
            None
        """
         # If no selection is active, do nothing and return
        if self.selection_start is None or self.selection_end is None:
            return

        # Move the gap to the beginning of the selection range
        self.move_cursor(self.selection_start)

        # Calculate how many characters are in the selection
        count = self.selection_end - self.selection_start

        # For each character in the selection, move the gap_end pointer forward,
        # and overwrite characters with empty strings (effectively deleting them)
        for _ in range(count):
            if self.gap_end < self.size:
                self.buffer[self.gap_end] = ''  # Clear the character after the gap
                self.gap_end += 1              # Expand the gap forward

        # Clear the selection markers since it's been deleted
        self.selection_start = None
        self.selection_end = None


    ########################## UNDO/REDO GAPBUFFER FUNCTIONALITY ###########################

    def _get_state_snapshot(self):
        """
        Creates a snapshot (deep copy) of the current buffer state.
        This includes the buffer content, gap positions, and selection.
        """
        return {
            "buffer": self.buffer[:], # Copy the list to avoid shared reference
            "gap_start": self.gap_start,
            "gap_end": self.gap_end,
            "size": self.size,
            "selection_start": self.selection_start,
            "selection_end": self.selection_end,
        }    


    def _restore_state(self, state):
        """
        Restore the buffer to a previously recorded state.
        All fields are overwritten to match the saved snapshot.
        """
        self.buffer = state["buffer"][:] # Copy to avoid shared reference
        self.gap_start = state["gap_start"]
        self.gap_end = state["gap_end"]
        self.size = state["size"]
        self.selection_start = state["selection_start"]
        self.selection_end = state["selection_end"]


    def record_state(self):
        """
        Record the current state of the buffer before making a change.
        This is used to support undo operations.
        """
        state = self._get_state_snapshot()
        self.undo_stack.append(state)
        self.redo_stack.clear() # Once a new change is made, redo history is no longer valid


    def undo(self):
        """
        Undo the last recorded operation by restoring the most recent state
        from the undo stack. The current state is saved in the redo stack
        so it can be reapplied later.
        """
        if not self.undo_stack:
            return # No previous state to revert to
        
        # Save current state in redo stack before restoring
        self.redo_stack.append(self._get_state_snapshot())

        # Pop and restore the last state from undo stack
        previous_state = self.undo_stack.pop()
        self._restore_state(previous_state)
        

    def redo(self):
        """
        Redo the last undone operation by restoring the most recent state
        from the redo stack. The current state is saved in the undo stack.
        """
        if not self.redo_stack:
            return # No state to redo
        
        # Save the current state in undo stack before restoring
        self.undo_stack.append(self._get_state_snapshot())

        # Pop and restore the last state from redo stack
        next_state = self.redo_stack.pop()
        self._restore_state(next_state)
