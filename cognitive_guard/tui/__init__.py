"""Interactive TUI for documentation assistance"""

import fcntl
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer
from textual.widgets import Button, Footer, Header, Label, Static, TextArea

from cognitive_guard.core.complexity import ComplexityResult
from cognitive_guard.core.config import Config
from cognitive_guard.core.scanner import ScanResults


class CognitiveGuardApp(App):
    """Interactive documentation assistant TUI"""

    CSS = """
    Screen {
        background: $surface;
    }

    #header {
        background: $primary;
        color: $text;
        padding: 1;
        text-align: center;
        height: 3;
    }

    #stats {
        background: $panel;
        border: solid $primary;
        padding: 1;
        margin: 1;
        height: auto;
    }

    #violation-info {
        background: $panel;
        border: solid $warning;
        padding: 1;
        margin: 1;
        height: auto;
    }

    #code-preview {
        background: $panel;
        border: solid $accent;
        padding: 1;
        margin: 1;
        height: 10;
    }

    #editor {
        border: solid $success;
        padding: 0;
        margin: 1;
        height: 10;
    }

    #status {
        background: $panel;
        padding: 1;
        margin: 1;
        height: 3;
    }

    Button {
        margin: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+n", "next", "Next"),
        Binding("ctrl+p", "prev", "Previous"),
    ]

    def __init__(self, config: Config, results: ScanResults | None = None):
        super().__init__()
        self.config = config
        self.results = results
        self.current_violation_index = 0
        self.violations: list[tuple[Path, ComplexityResult]] = []
        self.fixed_count = 0
        self.status_message = ""

        # Flatten violations
        if self.results and self.results.files:
            for file_result in self.results.files:
                for violation in file_result.violations:
                    self.violations.append((Path(file_result.file_path), violation))

    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header()

        with ScrollableContainer():
            yield Static("🧠 Cognitive Guard - Interactive Documentation Assistant", id="header")
            yield Static(self._get_stats_text(), id="stats")
            yield Static(self._get_violation_text(), id="violation-info")
            yield Static(self._get_code_preview(), id="code-preview")

            yield Label("✍️ Enter your docstring below:")
            yield TextArea("", id="editor", language="python")

            yield Static(self._get_status(), id="status")

            with Horizontal():
                yield Button("💾 Save & Next", variant="success", id="save-next")
                yield Button("⏭️  Skip", variant="default", id="skip")
                yield Button("⬅️  Previous", variant="default", id="prev")
                yield Button("❌ Exit", variant="error", id="exit")

        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts"""
        self._update_editor_content()

    def _get_stats_text(self) -> str:
        """Get statistics text"""
        if not self.violations:
            return "✅ No violations detected! All complex functions are documented."

        total = len(self.violations)
        remaining = total - self.fixed_count

        return f"""
📊 Statistics:
• Total Violations: {total}
• Fixed: {self.fixed_count}
• Remaining: {remaining}
• Current Progress: {self.current_violation_index + 1}/{total}
• Target Coverage: {self.config.target_coverage:.0%}
        """.strip()

    def _get_violation_text(self) -> str:
        """Get current violation text"""
        if not self.violations:
            return "✅ No violations!"

        if self.current_violation_index >= len(self.violations):
            return f"""
🎉 All violations reviewed!

• Fixed: {self.fixed_count}
• Skipped: {len(self.violations) - self.fixed_count}

Press 'q' to quit.
            """.strip()

        file_path, violation = self.violations[self.current_violation_index]

        return f"""
🚫 Violation {self.current_violation_index + 1}/{len(self.violations)}

📁 File: {file_path.name}
📍 Full Path: {file_path}
🔧 Function: {violation.name}
📏 Line: {violation.line_number}
🧠 Brain Score: {violation.complexity} {violation.emoji}
⚠️  Severity: {violation.severity.upper()}

💡 This function needs a docstring because it's cognitively complex.
        """.strip()

    def _get_code_preview(self) -> str:
        """Get preview of the function code"""
        if not self.violations or self.current_violation_index >= len(self.violations):
            return ""

        file_path, violation = self.violations[self.current_violation_index]

        try:
            with open(file_path) as f:
                lines = f.readlines()

            # Show function definition and a few lines
            start = max(0, violation.line_number - 1)
            end = min(len(lines), start + 10)

            preview = "".join(lines[start:end])
            return f"📝 Code Preview:\n\n{preview}"
        except Exception as e:
            return f"⚠️  Could not load code preview: {e}"

    def _get_status(self) -> str:
        """Get status message"""
        if self.status_message:
            return self.status_message
        return "💡 Tip: Use Ctrl+S to save, Ctrl+N for next, Ctrl+P for previous"

    def _update_editor_content(self) -> None:
        """Update editor with suggested docstring template"""
        if not self.violations or self.current_violation_index >= len(self.violations):
            return

        _, violation = self.violations[self.current_violation_index]

        # Provide a template
        template = f'''"""
FIXME: Add description of what {violation.name} does

Args:
    Add parameters here

Returns:
    Add return value description

Note:
    This function has a complexity score of {violation.complexity}.
    Consider refactoring if possible.
"""'''

        editor = self.query_one("#editor", TextArea)
        editor.text = template

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "exit":
            self.exit()
        elif event.button.id == "skip":
            self.action_next()
        elif event.button.id == "prev":
            self.action_prev()
        elif event.button.id == "save-next":
            if self.action_save():
                self.action_next()

    def action_prev(self) -> None:
        """Move to previous violation"""
        if self.current_violation_index > 0:
            self.current_violation_index -= 1
            self._refresh_ui()
        else:
            self.status_message = "⚠️  Already at first violation"
            self._refresh_ui()

    def action_next(self) -> None:
        """Move to next violation"""
        if self.current_violation_index < len(self.violations) - 1:
            self.current_violation_index += 1
            self._refresh_ui()
        elif self.current_violation_index == len(self.violations) - 1:
            self.current_violation_index += 1
            self._refresh_ui()
        else:
            self.status_message = "✅ All violations reviewed! Press 'q' to quit."
            self._refresh_ui()

    def action_save(self) -> bool:
        """Save current documentation to file"""
        if not self.violations or self.current_violation_index >= len(self.violations):
            return False

        file_path, violation = self.violations[self.current_violation_index]
        editor = self.query_one("#editor", TextArea)
        docstring = editor.text.strip()

        if not docstring or "FIXME" in docstring:
            self.status_message = "⚠️  Please write a proper docstring (remove FIXME)"
            self._refresh_ui()
            return False

        try:
            # Open file with exclusive lock to prevent race conditions
            with open(file_path, "r+") as f:
                # Acquire exclusive lock (blocking)
                try:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                except (OSError, AttributeError):
                    # fcntl not available on Windows, proceed without locking
                    pass

                # Read the file
                lines = f.readlines()

            # Find the function line and add docstring
            func_line_idx = violation.line_number - 1

            # Find indentation of the function
            func_line = lines[func_line_idx]
            indent = len(func_line) - len(func_line.lstrip())
            doc_indent = " " * (indent + 4)  # Docstring is indented 4 more spaces

            # Format the docstring with proper indentation
            docstring_lines = docstring.split("\n")
            formatted_docstring = "\n".join(
                doc_indent + line if line.strip() else line for line in docstring_lines
            )

            # Insert docstring after function definition
            # Find the line after the function signature (could span multiple lines)
            # Only stop when we find the actual colon ending the signature
            insert_idx = func_line_idx + 1
            # Find the line with : that ends the function signature
            while insert_idx < len(lines):
                line = lines[insert_idx].strip()

                # Found the end of signature (line ends with :)
                if line.endswith(":"):
                    insert_idx += 1
                    break

                # Keep going if we're still in parameters or closing
                # (ends with comma, backslash, or is a closing paren, or decorator)
                if (
                    line.endswith((",", "\\"))
                    or line.startswith((")", "@"))
                    or line == ""  # blank line
                    or
                    # Last param before closing paren (no comma)
                    (insert_idx + 1 < len(lines) and lines[insert_idx + 1].strip().startswith(")"))
                ):
                    insert_idx += 1
                    continue

                # Otherwise we've gone past the signature, insert here
                break

            # Insert the docstring
            lines.insert(insert_idx, formatted_docstring + "\n")

            # Seek to beginning and truncate file before writing
            f.seek(0)
            f.truncate()
            # Write back to same file (still locked)
            f.writelines(lines)
            # Lock will be released when context manager exits

            self.fixed_count += 1
            self.status_message = f"✅ Saved docstring to {file_path.name}! Fixed: {self.fixed_count}/{len(self.violations)}"
            self._refresh_ui()
            return True

        except Exception as e:
            self.status_message = f"❌ Error saving: {e}"
            self._refresh_ui()
            return False

    def _refresh_ui(self) -> None:
        """Refresh all UI components"""
        self.query_one("#stats", Static).update(self._get_stats_text())
        self.query_one("#violation-info", Static).update(self._get_violation_text())
        self.query_one("#code-preview", Static).update(self._get_code_preview())
        self.query_one("#status", Static).update(self._get_status())
        self._update_editor_content()

        # Clear status message after showing
        if self.status_message:
            import asyncio

            async def clear_status():
                await asyncio.sleep(3)
                self.status_message = ""
                self.query_one("#status", Static).update(self._get_status())

            asyncio.create_task(clear_status())

    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()
