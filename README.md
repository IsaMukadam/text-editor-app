## Recommended Project to Complete  
[Challenging Projects – Austin Henley](https://austinhenley.com/blog/challengingprojects.html)

### Text Editor

We use text editors every day, but do you know how they really work? Ignoring all of the fancy features your favorite editor has, how would you implement a textbox that supports a movable text cursor and selecting, inserting, and deleting text?  
**No, you can't use the built-in textbox component from your favorite GUI framework!**

The biggest challenge is figuring out how to store the text document in memory. My first thought was to use an array, but that has horrible performance if the user inserts text anywhere other than the end of the document. Luckily, there are some nice data structures to learn to solve this.

Another hurdle was learning how a text cursor behaves in popular editors. For example, if I press the up arrow key with the cursor in the middle of the document, where will the cursor move? Same column? Not if that line is shorter. Keep pressing up. The cursor will snap back to the original column once a line is long enough. It turns out that the cursor has a memory for the column and tries to get back to it.  
It is these details that I never noticed until I tried to implement it.

---

After implementing the basic editor, I challenge you to implement two more features:

- **Undo/Redo**
- **Word Wrapping**

Implementing undo/redo in an efficient way was mind-blowing to me! I first tried keeping an array of previous states, then tried the Memento pattern, before finally settling on the Command pattern.  
Word wrapping forces you to separate the visual aspects of a text line from the memory aspects.

---

### Things to Learn

- Data structures for storing the text: **array**, **rope**, **gap buffer**, **piece table**
- Behavior and implementation of the text cursor
- Design patterns for undo/redo: **Memento**, **Command**
- Abstractions to separate the visual and memory aspects of the text

---

### Further Reading

- [Text Editor: Data Structures (web)](https://austinhenley.com/blog/dataforstrings.html)  
- [Design and Implementation of a Win32 Text Editor (web)](https://learn.microsoft.com/en-us/windows/win32/learnwin32/winmain--the-application-entry-point)  
- [Data Structures and Algorithms in Java (Amazon)](https://www.amazon.com/Data-Structures-Algorithms-Java-6th/dp/0133769399)
