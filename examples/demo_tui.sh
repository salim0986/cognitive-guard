#!/bin/bash
# Demo script to show TUI functionality

echo "========================================="
echo "Cognitive Guard TUI Demo"
echo "========================================="
echo ""
echo "Step 1: Scanning for violations..."
echo ""

cd "$(dirname "$0")"
source ../.venv/bin/activate

cognitive-guard scan

echo ""
echo "Step 2: You can now launch the interactive TUI with:"
echo "  cognitive-guard tui"
echo ""
echo "The TUI will allow you to:"
echo "  • View each violation one by one"
echo "  • See a code preview of the function"
echo "  • Get a docstring template"
echo "  • Edit and save the docstring directly to the file"
echo "  • Navigate with buttons or keyboard shortcuts:"
echo "    - Ctrl+S: Save"
echo "    - Ctrl+N: Next"
echo "    - Ctrl+P: Previous"
echo "    - Q: Quit"
echo ""
echo "========================================="
