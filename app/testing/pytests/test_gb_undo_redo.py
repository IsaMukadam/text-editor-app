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
    
    assert len(buffer.undo_stack) == 1
    assert saved_buffer_text == buffer.get_text()
    assert state["gap_start"] == buffer.gap_start
    assert state["gap_end"] == buffer.gap_end

