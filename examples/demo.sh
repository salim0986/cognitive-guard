#!/usr/bin/env bash
# Demo script to showcase Cognitive Guard features

set -e

echo "🧠 Cognitive Guard Demo"
echo "======================"
echo ""

# Check if cognitive-guard is installed
if ! command -v cognitive-guard &> /dev/null; then
    echo "❌ cognitive-guard not found. Installing..."
    pip install -e .
fi

echo "📦 Step 1: Initialize Cognitive Guard"
echo "--------------------------------------"
cognitive-guard init --force
echo ""

echo "📊 Step 2: Scan Example Code"
echo "-----------------------------"
cognitive-guard scan --json > scan_results.json
echo ""

echo "📈 Results Summary:"
cat scan_results.json | python3 -m json.tool
echo ""

echo "🎯 Step 3: Check Violations"
echo "----------------------------"
cognitive-guard check || true
echo ""

echo "📚 Step 4: View Documentation"
echo "------------------------------"
echo "Coverage Report:"
cognitive-guard stats || echo "No stats available yet"
echo ""

echo "✅ Demo Complete!"
echo ""
echo "Try these commands:"
echo "  - cognitive-guard tui        (Interactive documentation assistant)"
echo "  - cognitive-guard check      (Check current code)"
echo "  - cognitive-guard stats      (View your achievements)"
