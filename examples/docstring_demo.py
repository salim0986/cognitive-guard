"""
Visual demonstration of docstrings in action
"""

# =============================================================================
# EXAMPLE 1: WITHOUT DOCSTRING (BAD)
# =============================================================================

def process_order(items, user, promo, shipping):
    # Complex logic with Brain Score: 18
    total = 0
    for item in items:
        if item.is_available():
            price = item.price
            if promo and promo.is_valid(user):
                if promo.type == "percent":
                    price *= (1 - promo.value / 100)
                elif promo.type == "fixed":
                    price -= promo.value
            if user.is_premium():
                price *= 0.95
            total += price
    
    if shipping == "express":
        total += 15.99
    elif shipping == "standard":
        total += 5.99
    
    return {"total": total, "tax": total * 0.08, "final": total * 1.08}

# Problems:
# - What does this function return?
# - What are valid values for 'shipping'?
# - What's the promo object structure?
# - Does it handle errors?
# - Can it fail?
# 
# User experience:
# - Has to read 20 lines to understand
# - Guesses parameter values
# - Doesn't know return value structure
# - No IDE help


# =============================================================================
# EXAMPLE 2: WITH DOCSTRING (GOOD) - Cognitive Guard Approved! ✅
# =============================================================================

def process_order_documented(items, user, promo, shipping):
    """
    Calculate the total order amount with discounts and shipping.
    
    Applies multiple discount layers in this order:
    1. Promotional discount (if valid)
    2. Premium member discount (5% off)
    3. Calculates tax (8%)
    4. Adds shipping cost
    
    Args:
        items (list[Product]): List of products to purchase.
            Each product must have .price and .is_available() method.
        user (User): User placing the order.
            Premium members (.is_premium() == True) get 5% discount.
        promo (PromoCode | None): Optional promo code to apply.
            Must have .is_valid(user), .type ('percent' or 'fixed'), .value
        shipping (str): Shipping method.
            Valid options: 'express' (+$15.99), 'standard' (+$5.99), 'pickup' (free)
    
    Returns:
        dict: Order totals with structure:
            {
                'total': float,      # Subtotal after all discounts
                'tax': float,        # Tax amount (8% of total)
                'final': float       # Total + tax
            }
    
    Raises:
        ValueError: If shipping method is invalid
        ProductUnavailableError: If any item is unavailable
    
    Examples:
        >>> items = [Product(price=100), Product(price=50)]
        >>> user = User(premium=True)
        >>> result = process_order_documented(items, user, None, 'standard')
        >>> result['final']
        153.63  # (150 * 0.95 + 5.99) * 1.08
    
    Note:
        Complexity score: 18
        Consider extracting discount calculation to separate function.
    """
    # Same complex logic as above
    total = 0
    for item in items:
        if item.is_available():
            price = item.price
            if promo and promo.is_valid(user):
                if promo.type == "percent":
                    price *= (1 - promo.value / 100)
                elif promo.type == "fixed":
                    price -= promo.value
            if user.is_premium():
                price *= 0.95
            total += price
    
    if shipping == "express":
        total += 15.99
    elif shipping == "standard":
        total += 5.99
    elif shipping != "pickup":
        raise ValueError(f"Invalid shipping method: {shipping}")
    
    return {"total": total, "tax": total * 0.08, "final": total * 1.08}


# =============================================================================
# HOW USERS BENEFIT
# =============================================================================

def demo_user_experience():
    """
    Demonstration of how docstrings help users.
    
    Try this in your IDE:
    1. Type: process_order(
       - IDE shows: process_order(items, user, promo, shipping)
       - No parameter hints, no description ❌
    
    2. Type: process_order_documented(
       - IDE shows full docstring with:
         * Function description
         * Each parameter explained with types
         * Return value structure
         * Example usage
         * Error conditions ✅
    
    3. Hover over function name:
       - Without docstring: Just the signature
       - With docstring: Full documentation popup!
    
    4. Call help():
       >>> help(process_order)
       process_order(items, user, promo, shipping)  # That's it!
       
       >>> help(process_order_documented)
       process_order_documented(items, user, promo, shipping)
           Calculate the total order amount with discounts and shipping.
           [... full docstring displayed ...]
    """
    pass


# =============================================================================
# REAL-WORLD SCENARIO
# =============================================================================

# Scenario: New developer joins your team

# WITHOUT DOCSTRING:
# Day 1: "How do I calculate order totals?"
# You: "Use process_order function"
# Them: "What parameters does it need?"
# You: "Items, user, promo, and shipping"
# Them: "What's the promo object?"
# You: "It has type, value, and is_valid method"
# Them: "What shipping values are valid?"
# You: "express, standard, or pickup"
# Them: "What does it return?"
# You: "A dict with total, tax, and final"
# Them: "Can it throw errors?"
# You: "Yes, if product unavailable or invalid shipping"
# 
# Time wasted: 30 minutes of back-and-forth
# Result: They might still get it wrong

# WITH DOCSTRING:
# Day 1: "How do I calculate order totals?"
# You: "Use process_order_documented function"
# Them: [Hovers in IDE, reads docstring]
# Them: "Got it! Thanks!"
# 
# Time wasted: 30 seconds
# Result: They understand it perfectly

# =============================================================================
# IDE INTEGRATION EXAMPLE
# =============================================================================

"""
When you type in VSCode, PyCharm, etc:

process_order_documented(
                        ^
                        Cursor here shows:

┌─────────────────────────────────────────────────────────┐
│ process_order_documented                                │
│ (items, user, promo, shipping)                          │
│                                                         │
│ Calculate the total order amount with discounts        │
│ and shipping.                                           │
│                                                         │
│ Args:                                                   │
│   items (list[Product]): List of products to purchase  │
│   user (User): User placing the order                  │
│   promo (PromoCode | None): Optional promo code        │
│   shipping (str): 'express', 'standard', or 'pickup'   │
│                                                         │
│ Returns:                                                │
│   dict: Order totals with 'total', 'tax', 'final'      │
└─────────────────────────────────────────────────────────┘

This appears automatically as you type!
No need to:
- Read the source code
- Ask someone
- Guess parameter types
- Trial and error
"""


# =============================================================================
# COMPARISON SUMMARY
# =============================================================================

"""
┌──────────────────────┬────────────────────┬──────────────────────┐
│ Aspect               │ Without Docstring  │ With Docstring       │
├──────────────────────┼────────────────────┼──────────────────────┤
│ IDE tooltip          │ Just signature     │ Full documentation   │
│ help() output        │ Minimal            │ Complete guide       │
│ Understanding time   │ 10-30 minutes      │ 30 seconds           │
│ Mistakes made        │ High (guessing)    │ Low (clear docs)     │
│ Questions to team    │ Many               │ Few                  │
│ Onboarding speed     │ Slow               │ Fast                 │
│ Code reviews         │ "What does this    │ "Logic looks good"   │
│                      │  parameter do?"    │                      │
│ Maintenance          │ Hard               │ Easy                 │
│ API documentation    │ Manual effort      │ Auto-generated       │
└──────────────────────┴────────────────────┴──────────────────────┘
"""

# =============================================================================
# WHY COGNITIVE GUARD EXISTS
# =============================================================================

"""
Cognitive Guard's Philosophy:

1. Simple code (Score ≤ 10): Self-explanatory
   def add(a, b):
       return a + b  # No docstring needed

2. Complex code (Score > 10): Brain needs help!
   def process_order(...):
       # 50 lines of if/else/loops
       # DOCSTRING REQUIRED ✅

The more complex the code, the more important the documentation.

Result:
- Developers understand complex functions instantly
- Code reviews focus on logic, not "what does this do?"
- New team members productive faster
- Fewer bugs from misunderstanding
- Professional, maintainable codebase

That's why Cognitive Guard blocks commits for undocumented complex code!
"""


if __name__ == "__main__":
    # Try these in your Python interpreter:
    print("Try these commands:")
    print("1. help(process_order)")
    print("2. help(process_order_documented)")
    print("3. print(process_order.__doc__)")
    print("4. print(process_order_documented.__doc__)")
    print("\nSee the difference? That's the power of docstrings! 🚀")
