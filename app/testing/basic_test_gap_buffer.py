from app.editor_buffer.gap_buffer import GapBuffer

class BasicGapBufferFuncTests():

    def test_init(self):
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


    def test_resize(self):
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

        print("test_resize passed.")

    def test_insert(self):
        """
        Test inserting characters into the buffer.
        """
        gb = GapBuffer(5)
        gb.insert("hello")
        assert gb.get_text() == "hello", "Insert failed for full word"

        gb.insert(" world")
        assert gb.get_text() == "hello world", "Insert with resize failed"

        print("test_insert passed.")

    def test_get_text(self):
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

        print("test_get_text passed")

    def test_delete(self):
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

        print("test_delete passed")


    def test_move_cursor(self):
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

        print("test_move_cursor passed")
    
    
if __name__ == "__main__":

    # Testing the basic gapbuffer functionality
    basic_gapbuffer_tests = BasicGapBufferFuncTests()
    basic_gapbuffer_tests.test_init()
    basic_gapbuffer_tests.test_resize()
    basic_gapbuffer_tests.test_insert()
    basic_gapbuffer_tests.test_get_text()
    basic_gapbuffer_tests.test_delete()
    basic_gapbuffer_tests.test_move_cursor()
