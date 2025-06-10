from editor_buffer.gap_buffer import GapBuffer

if __name__ == "__main__":
    buf = GapBuffer()

    for c in "hello":
        buf.insert(c)

    buf.move_cursor_left()
    buf.move_cursor_left()
    buf.insert('X')

    print("Buffer:", buf.get_text())
    print("Cursor at:", buf.get_cursor_position())
    print("Internal:", buf)

