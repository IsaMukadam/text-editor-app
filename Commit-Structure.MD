## ✅ Typical Commit Structure

<type>(<scope>): <short summary>

### 1. Type (required)

- `feat`: A new feature  
- `fix`: A bug fix  
- `chore`: Routine tasks, maintenance  
- `refactor`: Code change that neither fixes a bug nor adds a feature  
- `test`: Adding or modifying tests  
- `docs`: Documentation changes  
- `style`: Formatting, linting, white-space (no code changes)  
- `perf`: Performance improvements  
- `ci` / `build`: CI pipeline or build system changes  

---

### 2. Scope (optional but helpful)

A noun describing what part of the codebase is affected (e.g., `buffer`, `api`, `auth`, `ui`, `parser`, etc.)

---

### 3. Message

A concise, imperative sentence describing the change.

---

### 🔍 Example

feat(buffer): add undo/redo state management

**Optional Body:**

Includes stack-based undo/redo using snapshots.  
Test coverage added for both undo and redo paths.

**Optional Footer (for breaking changes or issues):**

BREAKING CHANGE: Buffer history now only tracks after record_state is called  
Closes #42


