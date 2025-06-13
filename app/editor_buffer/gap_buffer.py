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
        self.buffer = [''] * initial_size
        self.gap_start = 0
        self.gap_end = initial_size
        self.size = initial_size
        self.selection_start = None
        self.selection_end = None

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
        if not 0 <= position <= self.size:
            raise ValueError("Cursor position out of bounds")
        
        if position < self.gap_start:
            # Move gap left
            while self.gap_start > position:
                self.gap_start -= 1
                self.gap_end -= 1
                self.buffer[self.gap_end] = self.buffer[self.gap_start]
                self.buffer[self.gap_start] = ''

        elif position > self.gap_start:
            # Move gap right
            while self.gap_start < position:
                self.buffer[self.gap_start] = self.buffer[self.gap_end]
                self.buffer[self.gap_end] = ''
                self.gap_start += 1
                self.gap_end += 1


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

    ########################## EXTENDED GAPBUFFER FUNCTIONALITY ###########################

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
        
        self.select_start = start
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
        if self.selection_start is None or self.selection_end is None:
            return
        
        self.move_cursor(self.selection_start)
        count = self.selection_end - self.selection_start
        for _ in range(count):
            if self.gap_end < self.size:
                self.buffer[self.gap_end] = ''
                self.gap_end += 1

        # Clear selection
        self.selection_start = None
        self.selection_end = None