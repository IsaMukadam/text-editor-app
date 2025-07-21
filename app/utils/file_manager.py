import os

class FileManager:
    """
    Helper class for reading from and writing to files.
    """

    @staticmethod
    def save_to_file(file_contents: str, filename: str) -> None:
        """
        Save the text content of the buffer to a file.

        Args:
            file_contents (str): The contents of the file.
            filename (str): The name or path of the file to save to.

        Raises:
            ValueError: If the filename is empty.
            IOError: If there is an error during file writing.
        """
        if not filename:
            raise ValueError("Filename cannot be empty.")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(file_contents)
        except IOError as e:
            raise IOError(f"Error saving file: {e}")


    @staticmethod
    def load_from_file(filename: str) -> str:
        """
        Load text content from a file into the buffer.

        This resets the current buffer and inserts the file's contents.

        Args:
            filename (str): The name or path of the file to load from.

        Returns:
            file_contents (str): The contents of the file. 
        Raises:
            ValueError: If the filename is empty.
            FileNotFoundError: If the specified file does not exist.
            IOError: If there is an error during file reading.
        """
        if not filename:
            raise ValueError("Filename cannot be empty.")

        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found.")

        try:
            with open(filename, 'r', encoding='utf-8') as f:
               file_contents = f.read()
        except IOError as e:
            raise IOError(f"Error loading file: {e}")
        
        return file_contents
