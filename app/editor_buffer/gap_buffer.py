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

        Parameters
        ----------
        initial_size (int): Intial size of the underlying buffer.
        """
        self.buffer = [''] * initial_size
        self.gap_start = 0
        self.gap_end = initial_size
        self.size = initial_size

    def _resize(self, new_size= int) -> None:
        """
        Resize the buffer to at least `new_size`. The gap is preserved during resizing.

        Arguments:
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
        