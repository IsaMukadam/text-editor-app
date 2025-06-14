import pytest

from app.editor_buffer.gap_buffer import GapBuffer


@pytest.fixture
def buffer():
    """
    Initialising the buffer.
    """
    gb = GapBuffer(20)
    gb.insert("Hello, world!")
    return gb

def test_select_valid_range(buffer):
    """
    Test that a valid selection range correctly sets select_start and selection_end.
    """
    buffer.select(0,5)
    assert buffer.selection_start == 0
    assert buffer.selection_end == 5

def test_select_invalid_range_raises():
    """
    Testing selecting an invalid range raises ValidError.
    """
    gb = GapBuffer(10)
    gb.insert("abc")
    with pytest.raises(ValueError):
        gb.select(5, 2)
    with pytest.raises(ValueError):
        gb.select(-1, 3)
    with pytest.raises(ValueError):
        gb.select(0, 100)

def test_get_selection_returns_test(buffer):
    """
    Test get_selection returns empty string when no selection is made.
    """
    buffer.selection_start = None
    buffer.selection_end = None
    assert buffer.get_selection() == ""

def test_delete_selection(buffer):
    """
    Test that delete_selection removes the selected text and clears selection.
    """
    buffer.select(7, 12) # "world"
    buffer.delete_selection()
    assert buffer.get_text() == "Hello, !"
    assert buffer.selection_start is None
    assert buffer.selection_end is None