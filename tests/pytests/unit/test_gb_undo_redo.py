import pytest
import logging

from app.editor_buffer.gap_buffer import GapBuffer

# Configure logging to output to console at DEBUG level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@pytest.fixture
def buffer():
    """
    Initialising the buffer.
    """
    gb = GapBuffer(20)
    gb.insert("abc")
    return gb


def print_buffer_state(buffer, label="Buffer State"):
    """
    Helper function to print the current buffer state for debugging.
    """
    print(f"\n--- {label} ---")
    print(f"Text: '{buffer.get_text()}'")
    print(f"Gap Start: {buffer.gap_start}, Gap End: {buffer.gap_end}")
    print(f"Undo Stack Size: {len(buffer.undo_stack)}")
    print(f"Redo Stack Size: {len(buffer.redo_stack)}")
    print(f"Undo Stack Top: {[s['buffer'][:buffer.size] for s in buffer.undo_stack[-1:]]}")
    print(f"Redo Stack Top: {[s['buffer'][:buffer.size] for s in buffer.redo_stack[-1:]]}")
    print("-----------------------\n")

######################## STANDARD METHOD TESTS ####################################

def test_record_state(buffer):
    """
    Test that record_state correctly saves the current buffer state
    onto the undo stack.
    """
    buffer.record_state()
    logger.debug("Undo stack length: %d", len(buffer.undo_stack))
    logger.debug("Saved state: %s", buffer.undo_stack[-1])
    
    state = buffer.undo_stack[-1]
    saved_buffer_text = ''.join(state["buffer"][:buffer.size])
    logger.debug("Saved buffer text: %s", saved_buffer_text)
    logger.debug("Current buffer text: %s", buffer.get_text())
    
    assert len(buffer.undo_stack) == 2
    assert saved_buffer_text == buffer.get_text()
    assert state["gap_start"] == buffer.gap_start
    assert state["gap_end"] == buffer.gap_end


def test_undo_restores_previous_state(buffer):
    """
    Test that undo correctly restores the buffer to its previous states.
    It should revert the text and gap positions after each undo.
    """

    # Removing the initial 'abc'
    buffer.select(0,3)
    buffer.delete_selection()

    # Saving empty state
    logger.debug("Initial buffer text: %s", buffer.get_text())
    logger.debug("Recorded state 1: %s", buffer.get_text())

    # Recording the empty state then inserting 'abc'
    buffer.insert("abc")   # Now buffer is "abc"
    logger.debug("After insert 'abc': %s", buffer.get_text())

    # Recording the state and inserting 'def'
    buffer.insert("def")   # Now buffer is "abcdef"
    logger.debug("After insert 'def': %s", buffer.get_text())
    assert buffer.get_text() == "abcdef"

    # Print undo stack states
    # for i, state in enumerate(buffer.undo_stack):
    #    text = ''.join(state["buffer"][:buffer.size])
    #    print(f"Undo stack state {i}: '{text}', gap_start={state['gap_start']}, gap_end={state['gap_end']}")

    # Testing a single undo
    buffer.undo()  # Should revert to "abc"
    logger.debug("After first undo: %s", buffer.get_text())
    assert buffer.get_text() == "abc"

    # Testing an additional undo
    buffer.undo()  # Should revert to empty (if you had a blank state first)
    logger.debug("After second undo: %s", buffer.get_text())
    assert buffer.get_text() == ""


def test_redo_restores_state(buffer):
    """
    Test that redo correctly reapplies the undone changes.
    """

    # Recording state and inserting 'def'
    logger.debug("Recorded state 1: %s", buffer.get_text())
    buffer.record_state() # Save state with "abc"
    buffer.insert("def") # Buffer is now "abcdef"

    assert buffer.get_text() == "abcdef"

    buffer.undo() # Undo: back to "abc"
    logger.debug("After undo: %s", buffer.get_text())
    assert buffer.get_text() == "abc"

    buffer.redo() # Redo: should go back to "abcdef"
    logger.debug("After redo: %s", buffer.get_text())
    assert buffer.get_text() == "abcdef"


######################## EDGE CASE TESTS ################################

def test_record_state_clears_redo_stack(buffer):
    """
    Test that calling record_state clears the redo stack.

    After performing an undo, the redo stack should be populated.
    If record_state is called (e.g. after a new edit), it should
    clear the redo stack to prevent redoing outdated states.
    """
    buffer.record_state()       # State: "abc"
    buffer.insert("def")        # State: "abcdef"
    buffer.record_state()       # Record new state

    buffer.undo()               # Undo to "abc"
    assert len(buffer.redo_stack) > 0

    buffer.record_state()       # Simulate new edit
    assert buffer.redo_stack == []


def test_undo_on_empty_stack(buffer):
    """
    Undo with empty undo stack should not fail.
    """
    buffer.undo_stack.clear() # Clear undo stack forcibly
    buffer.undo() # Should do nothing and not raise
    assert True # If no exception, test passes


def test_redo_on_empty_stack(buffer):
    """
    Redo with empty redo stack should not fail.
    """
    buffer.redo_stack.clear() # Clear redo stack forcibly
    buffer.redo() # Should do nothing and not raise
    assert True # If no exception, test passes


def test_redo_stack_cleared_after_new_edit(buffer):
    """
    Test that the redo stack is cleared after making a new edit following an undo.

    After undoing, the redo stack should contain states.
    But once a new edit is made and recorded, the redo stack should be cleared.
    """
    buffer.record_state()
    buffer.insert("def")
    buffer.record_state()

    buffer.undo() # undo to "abc"
    assert len(buffer.redo_stack) > 0

    buffer.insert("xyz") # new edit after undo should clear redo stack
    buffer.record_state()
    assert len(buffer.redo_stack) == 0
