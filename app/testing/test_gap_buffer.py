from app.editor_buffer.gap_buffer import GapBuffer

def test_init():
    """
    Unit test for GapBuffer.__init__ method.

    Validates initial state of the gap buffer, ensuring correct size,
    gap pointers, and empty character buffer.
    """
    buf = GapBuffer(10)
    assert buf.size == 10, "Buffer size should be 10"
    assert buf.gap_start == 0, "Inital gap_start should be 0"
    assert buf.gap_end == 10, "Initial gap_end should be equal to buffer size"
    assert buf.buffer == [''] * 10, "Buffer should be initialised with empty strings"
    print("test_init passed")


def test_resize():
    """
    Test resizing the buffer while preserving text and gap.
    """
    gb = GapBuffer(5)
    gb.insert("abc")
    old_buffer_len = len(gb.buffer)
    gb._resize(10)

if __name__ == "__main__":
    test_init()


