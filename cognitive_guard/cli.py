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
def init(force: bool) -> None:
    """Initialize Cognitive Guard in the current repository"""
    try:
        config = Config.create_default()
        config_path = Path.cwd() / ".cognitive-guard.yml"
        
        if config_path.exists() and not force:
            console.print(
                "[yellow]Configuration already exists. Use --force to overwrite.[/yellow]"
            )
            sys.exit(1)
        
        config.save(config_path)
        console.print(f"[green]✓[/green] Created configuration: {config_path}")
        
        # Install git hook
        installer = HookInstaller()
        if installer.install():
            console.print("[green]✓[/green] Installed pre-commit hook")
        else:
            console.print("[yellow]⚠[/yellow] Could not install git hook (not a git repo?)")
        
        console.print("\n[bold green]🎉 Cognitive Guard initialized successfully![/bold green]")
        console.print("Edit .cognitive-guard.yml to customize settings.")
        
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
        console.print("[red]Error:[/red] No .cognitive-guard.yml found. Run 'cognitive-guard init' first.")
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
        console.print("[red]Error:[/red] No .cognitive-guard.yml found. Run 'cognitive-guard init' first.")
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
        console.print("[red]Error:[/red] No .cognitive-guard.yml found. Run 'cognitive-guard init' first.")
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
        console.print("[red]Error:[/red] No .cognitive-guard.yml found. Run 'cognitive-guard init' first.")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


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
