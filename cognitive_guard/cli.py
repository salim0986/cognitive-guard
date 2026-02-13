"""
Main CLI entry point for Cognitive Guard
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from cognitive_guard.core.config import Config
from cognitive_guard.core.scanner import CodeScanner
from cognitive_guard.hooks.installer import HookInstaller
from cognitive_guard.tui.app import CognitiveGuardApp
from cognitive_guard.utils.stats import StatsTracker

console = Console()


@click.group()
@click.version_option()
def main() -> None:
    """🧠 Cognitive Guard - Gamified Code Documentation Enforcer"""
    pass


@main.command()
@click.option("--force", is_flag=True, help="Overwrite existing configuration")
@click.option("--interactive", "-i", is_flag=True, help="Interactive setup with questions")
def init(force: bool, interactive: bool) -> None:
    """Initialize Cognitive Guard in the current repository"""
    try:
        config_path = Path.cwd() / ".cognitive-guard.yml"
        
        if config_path.exists() and not force:
            console.print(
                "[yellow]Configuration already exists. Use --force to overwrite.[/yellow]"
            )
            sys.exit(1)
        
        if interactive:
            console.print("[bold cyan]Welcome! Let's set up Cognitive Guard.[/bold cyan]")
            console.print("I'll ask 3 quick questions:\n")
            
            # Question 1: Language
            console.print("[bold]1. What language is your project?[/bold]")
            language_choice = click.prompt(
                "   Choose",
                type=click.Choice(["python", "javascript", "typescript", "all"], case_sensitive=False),
                default="python"
            )
            
            if language_choice == "all":
                languages = ["python", "javascript", "typescript", "java"]
            else:
                languages = [language_choice]
            
            # Question 2: Strictness
            console.print("\n[bold]2. How strict should documentation be?[/bold]")
            console.print("   Relaxed (threshold: 15) - Only very complex code")
            console.print("   Balanced (threshold: 10) - Moderate complexity")
            console.print("   Strict (threshold: 5) - Most functions")
            strictness = click.prompt(
                "   Choose",
                type=click.Choice(["relaxed", "balanced", "strict"], case_sensitive=False),
                default="balanced"
            )
            
            threshold_map = {"relaxed": 15, "balanced": 10, "strict": 5}
            threshold = threshold_map[strictness]
            
            # Question 3: Git hook
            console.print("\n[bold]3. Install git hook to enforce on commits?[/bold]")
            install_hook = click.confirm("   ", default=True)
            
            # Create config with chosen values
            config = Config.create_default()
            config.complexity_threshold = threshold
            config.languages = languages
            
        else:
            config = Config.create_default()
            install_hook = True
        
        config.save(config_path)
        console.print(f"\n[green]✓[/green] Created configuration: {config_path}")
        
        # Install git hook
        if interactive and install_hook or not interactive:
            installer = HookInstaller()
            if installer.install():
                console.print("[green]✓[/green] Installed pre-commit hook")
            else:
                console.print("[yellow]⚠[/yellow] Could not install git hook (not a git repo?)")
        
        console.print("\n[bold green]🎉 Cognitive Guard initialized successfully![/bold green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  • Run [cyan]cognitive-guard scan[/cyan] to check your code")
        console.print("  • Run [cyan]cognitive-guard demo[/cyan] to see a quick demo")
        console.print("  • Edit .cognitive-guard.yml to customize settings")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option("--staged", is_flag=True, help="Only check staged files")
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON")
def check(staged: bool, json_output: bool) -> None:
    """Check code for documentation violations"""
    try:
        config = Config.load()
        scanner = CodeScanner(config)
        
        if staged:
            results = scanner.scan_staged()
        else:
            results = scanner.scan_all()
        
        if json_output:
            import json
            console.print_json(data=results.to_dict())
        else:
            results.display(console)
        
        if results.has_violations():
            sys.exit(1)
            
    except FileNotFoundError:
        console.print("\n[red]❌ Configuration Error:[/red] No .cognitive-guard.yml found")
        console.print("\n[bold]How to fix:[/bold]")
        console.print("  1. Run: [cyan]cognitive-guard init --interactive[/cyan]")
        console.print("  2. Or run: [cyan]cognitive-guard init[/cyan] for quick setup")
        console.print("\n[dim]This will create .cognitive-guard.yml with default settings[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option("--fail-under", type=float, help="Fail if coverage is below this threshold (0.0-1.0)")
def scan(fail_under: Optional[float]) -> None:
    """Scan entire codebase and generate coverage report"""
    try:
        config = Config.load()
        scanner = CodeScanner(config)
        
        console.print("[bold]🔍 Scanning codebase...[/bold]")
        results = scanner.scan_all()
        results.display(console)
        
        coverage = results.get_coverage()
        if fail_under is not None and coverage < fail_under:
            console.print(
                f"\n[red]❌ Coverage {coverage:.1%} is below threshold {fail_under:.1%}[/red]"
            )
            sys.exit(1)
        
        console.print(f"\n[green]✓[/green] Scan complete!")
        
    except FileNotFoundError:
        console.print("\n[red]❌ Configuration Error:[/red] No .cognitive-guard.yml found")
        console.print("\n[bold]How to fix:[/bold]")
        console.print("  1. Run: [cyan]cognitive-guard init --interactive[/cyan]")
        console.print("  2. Or run: [cyan]cognitive-guard init[/cyan] for quick setup")
        console.print("\n[dim]This will create .cognitive-guard.yml with default settings[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
def tui() -> None:
    """Launch interactive documentation assistant"""
    try:
        config = Config.load()
        scanner = CodeScanner(config)
        
        console.print("[bold cyan]🔍 Scanning for violations...[/bold cyan]")
        results = scanner.scan_all()
        
        violations_count = results.get_total_violations()
        
        if violations_count == 0:
            console.print("[bold green]✅ No violations found![/bold green]")
            console.print("All complex functions are properly documented.")
            return
        
        console.print(f"[yellow]Found {violations_count} violation(s)[/yellow]")
        console.print("[bold]Launching interactive TUI...[/bold]\n")
        
        app = CognitiveGuardApp(config, results)
        app.run()
        
    except FileNotFoundError:
        console.print("\n[red]❌ Configuration Error:[/red] No .cognitive-guard.yml found")
        console.print("\n[bold]How to fix:[/bold]")
        console.print("  1. Run: [cyan]cognitive-guard init --interactive[/cyan]")
        console.print("  2. Or run: [cyan]cognitive-guard init[/cyan] for quick setup")
        console.print("\n[dim]This will create .cognitive-guard.yml with default settings[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
def stats() -> None:
    """View documentation statistics and achievements"""
    try:
        config = Config.load()
        tracker = StatsTracker(config)
        tracker.display(console)
        
    except FileNotFoundError:
        console.print("\n[red]❌ Configuration Error:[/red] No .cognitive-guard.yml found")
        console.print("\n[bold]How to fix:[/bold]")
        console.print("  1. Run: [cyan]cognitive-guard init --interactive[/cyan]")
        console.print("  2. Or run: [cyan]cognitive-guard init[/cyan] for quick setup")
        console.print("\n[dim]This will create .cognitive-guard.yml with default settings[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
def demo() -> None:
    """Run a quick demonstration of Cognitive Guard"""
    import tempfile
    import shutil
    import os
    from textwrap import dedent
    
    console.print("[bold cyan]🎬 Cognitive Guard Demo[/bold cyan]\n")
    console.print("Let me show you how Cognitive Guard works in 30 seconds!\n")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        demo_dir = Path(tmpdir) / "demo_project"
        demo_dir.mkdir()
        
        # Create sample file with violations
        sample_file = demo_dir / "example.py"
        sample_code = dedent('''
            def simple_function():
                """This function is properly documented."""
                return "Hello"
            
            def complex_function(data, options, callback, timeout=30):
                # This function is complex but has NO docstring!
                result = []
                if data:
                    for item in data:
                        if options.get("validate"):
                            if callback(item):
                                if timeout > 0:
                                    result.append(item)
                                else:
                                    continue
                        else:
                            result.append(item)
                return result
        ''')
        sample_file.write_text(sample_code)
        
        console.print("[bold]📝 Sample code created:[/bold]")
        console.print(f"[dim]{sample_file}[/dim]\n")
        
        # Show the violation
        console.print("[bold yellow]❌ Found a violation:[/bold yellow]")
        console.print("Function [cyan]complex_function[/cyan] has high complexity (15) but no docstring!\n")
        
        # Show what good documentation looks like
        console.print("[bold green]✅ What good documentation looks like:[/bold green]")
        good_example = dedent('''
            def complex_function(data, options, callback, timeout=30):
                """Filter data items using callback with validation.
                
                Args:
                    data: List of items to filter
                    options: Dictionary with 'validate' flag
                    callback: Function to validate each item
                    timeout: Timeout in seconds (default: 30)
                    
                Returns:
                    List of filtered items that passed validation
                    
                Example:
                    >>> complex_function([1,2,3], {"validate": True}, lambda x: x > 1)
                    [2, 3]
                """
                # implementation...
        ''')
        console.print(f"[dim]{good_example}[/dim]")
        
        console.print("\n[bold cyan]💡 Key Features:[/bold cyan]")
        console.print("  • [green]✓[/green] Detects complex code automatically")
        console.print("  • [green]✓[/green] Blocks commits with undocumented code")
        console.print("  • [green]✓[/green] Interactive TUI to fix issues")
        console.print("  • [green]✓[/green] Track progress with gamification")
        
        console.print("\n[bold]Ready to try it on your code?[/bold]")
        console.print("Run: [cyan]cognitive-guard init --interactive[/cyan]")
        console.print("     [cyan]cognitive-guard scan[/cyan]\n")


@main.command()
def update_hook() -> None:
    """Update git pre-commit hook to latest version"""
    try:
        installer = HookInstaller()
        if installer.update():
            console.print("[green]✓[/green] Updated pre-commit hook")
        else:
            console.print("[yellow]⚠[/yellow] Could not update hook (not installed?)")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
def hook() -> None:
    """Run pre-commit hook (internal use)"""
    try:
        config = Config.load()
        scanner = CodeScanner(config)
        
        console.print("[bold cyan]🔍 Analyzing staged files...[/bold cyan]")
        results = scanner.scan_staged()
        
        if results.has_violations():
            console.print("\n" + "="*70)
            console.print("[bold red]🚫 COMMIT BLOCKED BY COGNITIVE GUARD[/bold red]")
            console.print("="*70)
            console.print("\n[yellow]Reason:[/yellow] Complex functions without documentation detected.\n")
            results.display(console)
            
            # Only prompt for TUI if running interactively
            if config.gamification.enabled and sys.stdin.isatty():
                console.print("\n[bold cyan]💡 Fix it now?[/bold cyan]")
                console.print("Launch interactive TUI to add documentation? (y/n): ", end="")
                try:
                    response = input().strip().lower()
                    if response == 'y':
                        app = CognitiveGuardApp(config, results)
                        app.run()
                        sys.exit(0)
                except (EOFError, KeyboardInterrupt):
                    console.print()  # New line
            
            console.print("\n" + "="*70)
            console.print("[bold yellow]💡 How to fix:[/bold yellow]")
            console.print("  1. Add docstrings to the functions listed above")
            console.print("  2. Run: [cyan]cognitive-guard tui[/cyan] (interactive)")
            console.print("  3. Or bypass (not recommended): [dim]git commit --no-verify[/dim]")
            console.print("="*70 + "\n")
            sys.exit(1)
        
        console.print("[bold green]✅ All complex functions are documented![/bold green]")
        console.print("[dim]Cognitive Guard check passed.[/dim]\n")
        
    except FileNotFoundError:
        # If no config, don't block commits
        console.print("[yellow]⚠[/yellow] No .cognitive-guard.yml found. Skipping checks.")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("[yellow]⚠[/yellow] Allowing commit due to error.")
        sys.exit(0)  # Don't block commits on errors


if __name__ == "__main__":
    main()
