"""
Example Python file demonstrating Cognitive Guard analysis
"""


def simple_function():
    """A simple function that returns a greeting"""
    return "Hello, World!"


def documented_complex_function(data, threshold, options):
    """
    Process data with complex logic and multiple conditions.
    
    This function demonstrates a properly documented complex function
    that would pass Cognitive Guard checks.
    
    Args:
        data: Input data to process
        threshold: Numeric threshold for filtering
        options: Dictionary of processing options
    
    Returns:
        Processed result based on conditions
    
    Example:
        >>> result = documented_complex_function([1, 2, 3], 2, {"mode": "strict"})
    """
    result = []
    
    if options.get("mode") == "strict":
        for item in data:
            if item > threshold:
                if options.get("double"):
                    result.append(item * 2)
                else:
                    result.append(item)
    elif options.get("mode") == "lenient":
        for item in data:
            if item >= threshold:
                result.append(item)
    else:
        result = data
    
    return result


def undocumented_complex_function(x, y, z):
    # ⚠️ This function has high cognitive complexity but NO docstring
    # Cognitive Guard will flag this as a violation!
    
    if x > 0:
        if y > 0:
            if z > 0:
                # Deeply nested logic
                if x > y:
                    if y > z:
                        return x + y + z
                    else:
                        return x + y - z
                else:
                    if x > z:
                        return x - y + z
                    else:
                        return -x + y + z
            else:
                return x + y
        else:
            return x - y
    else:
        return 0


def refactor_candidate(a, b, c, d, e, f):
    """
    This function is so complex it should probably be refactored.
    
    Even with documentation, Brain Score > 20 suggests breaking this
    into smaller, more manageable functions.
    """
    result = 0
    
    if a and b:
        if c or d:
            if e and not f:
                for i in range(a):
                    if i % 2 == 0:
                        if b > i:
                            result += i
                        else:
                            result -= i
                    else:
                        if c > i:
                            result *= 2
            elif f and not e:
                try:
                    result = a / b
                except ZeroDivisionError:
                    result = 0
            else:
                result = a + b + c + d
        else:
            result = a - b
    else:
        result = -1
    
    return result


class ExampleClass:
    """Example class with methods of varying complexity"""
    
    def simple_method(self):
        """A simple method"""
        return True
    
    def complex_method(self, data, filters):
        """
        Apply multiple filters to data with complex logic.
        
        Args:
            data: List of items to filter
            filters: Dictionary of filter conditions
        
        Returns:
            Filtered and processed data
        """
        result = []
        
        for item in data:
            passes = True
            
            if "min_value" in filters and item < filters["min_value"]:
                passes = False
            
            if "max_value" in filters and item > filters["max_value"]:
                passes = False
            
            if "exclude" in filters and item in filters["exclude"]:
                passes = False
            
            if passes:
                if "transform" in filters:
                    result.append(filters["transform"](item))
                else:
                    result.append(item)
        
        return result
