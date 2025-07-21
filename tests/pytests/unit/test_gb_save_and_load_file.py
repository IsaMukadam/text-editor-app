import pytest

from app.utils.file_manager import FileManager

def test_save_and_load_file(tmp_path):
    """
    Test that saving text to a file and then loading it
    returns the exact same content.
    """
    test_text = "Hello, pytest!"
    test_file = tmp_path / "sample.txt"

    FileManager.save_to_file(test_text, str(test_file))
    loaded_text = FileManager.load_from_file(str(test_file))

    assert loaded_text == test_text

def test_load_from_nonexistent_file_raises(tmp_path):
    """
    Test that loading from a non-existent file
    raises a FileNotFoundError
    """
    non_existent_file = tmp_path / "does_not_exist.txt"

    with pytest.raises(FileNotFoundError):
        FileManager.load_from_file(str(non_existent_file))

def test_save_to_file_overwrites_existing(tmp_path):
    """
    Test that saving an existing file overwrites
    its previous content.
    """
    test_file = tmp_path / "overwrite.txt"

    FileManager.save_to_file("First content", str(test_file))
    FileManager.save_to_file("Second content", str(test_file))

    loaded_text = FileManager.load_from_file(str(test_file))
    assert loaded_text == "Second content"
