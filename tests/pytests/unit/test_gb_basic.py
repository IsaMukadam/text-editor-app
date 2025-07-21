import pytest

from app.editor_buffer.gap_buffer import GapBuffer


def test_init():
    """
    Unit test for GapBuffer.__init__ method.

    Validates initial state of the gap buffer, ensuring correct size,
    gap pointers, and empty character buffer.
    """
    buf = GapBuffer(10)
    assert buf.size == 10, "Buffer size should be 10"
    assert buf.gap_start == 0, "Initial gap_start should be 0"
    assert buf.gap_end == 10, "Initial gap_end should be equal to buffer size"
    assert buf.buffer == [''] * 10, "Buffer should be initialised with empty strings"

def test_resize():
    """
    Test resizing the buffer while preserving text and gap.
    """
    gb = GapBuffer(5)
    gb.insert("abc")
    old_text = gb.get_text()
    old_buffer_len = len(gb.buffer)
    gb.resize(10)
    new_buffer_len = len(gb.buffer)

    assert new_buffer_len > old_buffer_len, "Buffer did not resize properly"
    assert gb.get_text() == old_text, "Text changed after resizing"
    assert gb.gap_end - gb.gap_start >= 0, "Gap is not valid after resize"

def test_insert():
    """
    Test inserting characters into the buffer.
    """
    gb = GapBuffer(5)
    gb.insert("hello")
    assert gb.get_text() == "hello", "Insert failed for full word"

    gb.insert(" world")
    assert gb.get_text() == "hello world", "Insert with resize failed"

def test_get_text():
    """
    Test retrieving text from the buffer.
    """
    gb = GapBuffer(10)
    gb.insert("abc")
    text = gb.get_text()
    assert text == "abc", f"Expected 'abc', got '{text}'"

    gb.insert("def")
    text = gb.get_text()
    assert text == "abcdef", f"Expected 'abcdef', got '{text}'"

def test_delete():
    """
    Test deleting characters after the cursor position.
    """
    gb = GapBuffer(10)
    gb.insert("Hello")
    gb.move_cursor(2)
    gb.delete(2)
    assert gb.get_text() == "Heo", "Characters not deleted correctly"

    gb.delete(1)
    assert gb.get_text() == "He", "Last character not deleted correctly"

def test_move_cursor():
    """
    Test that the cursor moves correctly to different positions.
    """
    gb = GapBuffer(10)
    gb.insert("abc")
    gb.move_cursor(0)
    gb.insert("X")
    assert gb.get_text() == "Xabc", "Cursor did not move to start correctly"

    gb.move_cursor(3)
    gb.insert("Y")
    assert gb.get_text() == "XabYc", "Cursor did not move to middle correctly"

    gb.move_cursor(5)
    gb.insert("Z")
    assert gb.get_text() == "XabYcZ", "Cursor did not move to end correctly"




