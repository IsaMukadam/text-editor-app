from editor_buffer.gap_buffer import GapBuffer

def print_state(editor: GapBuffer) -> None:
    """
    Prints the current state of the text editor buffer.

    Args:
        editor (GapBuffer): The gap buffer instance.
    """
    print("\nCurrent text:", repr(editor.get_text()))
    print("Cursor at:", editor.gap_start)
    print("-" * 40)

def main() -> None:
    """
    Starts an interactive command-line REPL for the gap buffer text editor.

    Allows users to insert, delete, move the cursor, select text, and perform undo/redo functionality.
    """
    editor = GapBuffer()

    while True:
        # The command being input
        command = input(">> ").strip()

        # If exit
        if command == "exit":
            print("Exiting...")
            break
        
        # If something is inserted
        elif command.startswith("insert "):
            text = command[len("insert "):]
            editor.insert(text)

        # If cursor move
        elif command.startswith("move "):
            try:
                pos = int(command[len("move "):])
                editor.move_cursor(pos)
            except ValueError:
                print("Invalid position")

        # If delete
        elif command.startswith("delete "):
            try:
                count = int(command[len("delete "):])
                editor.delete(count)
            except ValueError as e:
                print(e)

        # If select
        elif command.startswith("select "):
            try:
                _, start, end=command.split()
                editor.select(int(start), int(end))
            except Exception:
                print("Usage: select <start> <end>")

        # If get
        elif command == "get":
            print("Full Text: ", repr(editor.get_text()))
        
        # If selection
        elif command == "selection":
            print("Selected:", repr(editor.get_selection()))

        # If delete selection
        elif command == "delete_selection":
            editor.delete_selection()

        # If undo
        elif command == "undo":
            editor.undo()

        # If redo
        elif command == "redo":
            editor.redo()

        elif command == "help":
            print("""
Available commands:
    insert <text>          Insert text at cursor
    move <pos>             Move cursor to position
    delete <count>         Delete characters after cursor
    select <start> <end>   Select a range of text
    selection              Show current selection
    delete_selection       Delete selected text
    get                    Show full text
    undo                   Undo last change
    redo                   Redo last undone change
    exit                   Quit editor      
                  """)
            
        else:
            print("Unknown command. Type 'help' for a list of commands.")

        print_state(editor)

if __name__ == "__main__":
    main()

    
