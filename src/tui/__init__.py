"""Interactive TUI for documentation assistance"""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Button, TextArea, Label
from textual.binding import Binding

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
    }
    
    #stats {
        background: $panel;
        border: solid $primary;
        padding: 1;
        margin: 1;
    }
    
    #violation-list {
        background: $panel;
        border: solid $warning;
        padding: 1;
        margin: 1;
        height: 50%;
    }
    
    #editor {
        background: $panel;
        border: solid $success;
        padding: 1;
        margin: 1;
    }
    
    Button {
        margin: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("s", "save", "Save"),
        Binding("n", "next", "Next"),
    ]
    
    def __init__(self, config: Config, results: ScanResults | None = None):
        super().__init__()
        self.config = config
        self.results = results
        self.current_violation_index = 0
    
    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header()
        
        with Container():
            yield Static("🧠 Cognitive Guard - Interactive Documentation Assistant", id="header")
            
            with Vertical():
                yield Static(self._get_stats_text(), id="stats")
                yield Static(self._get_violation_text(), id="violation-list")
                
                yield TextArea("", id="editor")
                
                with Horizontal():
                    yield Button("Save & Next", variant="success", id="save-next")
                    yield Button("Skip", variant="default", id="skip")
                    yield Button("Exit", variant="error", id="exit")
        
        yield Footer()
    
    def _get_stats_text(self) -> str:
        """Get statistics text"""
        if not self.results:
            return "No violations detected!"
        
        violations = self.results.get_total_violations()
        coverage = self.results.get_coverage()
        
        return f"""
📊 Statistics:
• Total Violations: {violations}
• Coverage: {coverage:.1%}
• Target: {self.config.target_coverage:.1%}
        """.strip()
    
    def _get_violation_text(self) -> str:
        """Get current violation text"""
        if not self.results or not self.results.files:
            return "No violations!"
        
        # Flatten all violations
        all_violations = []
        for file_result in self.results.files:
            for violation in file_result.violations:
                all_violations.append((file_result.file_path, violation))
        
        if not all_violations:
            return "No violations!"
        
        if self.current_violation_index >= len(all_violations):
            return "All violations processed!"
        
        file_path, violation = all_violations[self.current_violation_index]
        
        return f"""
🚫 Violation {self.current_violation_index + 1}/{len(all_violations)}

File: {file_path}
Function: {violation.name}
Line: {violation.line_number}
Brain Score: {violation.complexity} {violation.emoji}
Severity: {violation.severity}

📝 Please add a docstring for this function.
        """.strip()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "exit":
            self.exit()
        elif event.button.id == "skip":
            self.action_next()
        elif event.button.id == "save-next":
            self.action_save()
            self.action_next()
    
    def action_next(self) -> None:
        """Move to next violation"""
        self.current_violation_index += 1
        self.refresh()
    
    def action_save(self) -> None:
        """Save current documentation"""
        # Implementation would save the docstring to the file
        pass
    
    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()
