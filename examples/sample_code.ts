/**
 * Sample TypeScript file to test Cognitive Guard
 */

interface User {
    id: number;
    name: string;
    type: 'regular' | 'premium' | 'vip';
}

interface Product {
    id: string;
    price: number;
    quantity: number;
}

/**
 * Simple function with proper documentation
 * @param a First number
 * @param b Second number
 * @returns Sum of two numbers
 */
function add(a: number, b: number): number {
    return a + b;
}

/**
 * Calculate user discount based on type and promo
 * @param user - User object with type information
 * @param hasPromo - Whether user has a promo code
 * @returns Discount rate as decimal (e.g., 0.15 for 15%)
 */
function getUserDiscount(user: User, hasPromo: boolean): number {
    let discount = 0;
    
    if (user.type === 'premium') {
        discount = 0.10;
        if (hasPromo) {
            discount += 0.05;
        }
    } else if (user.type === 'vip') {
        discount = 0.20;
        if (hasPromo) {
            discount += 0.10;
        }
    } else {
        if (hasPromo) {
            discount = 0.05;
        }
    }
    
    return discount;
}

// Complex function WITHOUT documentation - should be flagged!
function processUserOrders(
    users: User[],
    orders: Map<number, Product[]>,
    applyDiscounts: boolean
): Map<number, number> {
    const results = new Map<number, number>();
    
    for (const user of users) {
        const userOrders = orders.get(user.id);
        
        if (userOrders && userOrders.length > 0) {
            let total = 0;
            
            for (const product of userOrders) {
                let price = product.price * product.quantity;
                
                if (applyDiscounts) {
                    if (user.type === 'premium') {
                        price *= 0.9;
                    } else if (user.type === 'vip') {
                        price *= 0.8;
                    }
                }
                
                total += price;
            }
            
            results.set(user.id, total);
        } else {
            results.set(user.id, 0);
        }
    }
    
    return results;
}

/**
 * Calculate order total with tax
 * @param products Array of products in the order
 * @param taxRate Tax rate as decimal (e.g., 0.08 for 8%)
 * @returns Object with subtotal, tax, and total
 */
function calculateOrderTotal(
    products: Product[],
    taxRate: number
): { subtotal: number; tax: number; total: number } {
    const subtotal = products.reduce((sum, p) => {
        return sum + (p.price * p.quantity);
    }, 0);
    
    const tax = subtotal * taxRate;
    const total = subtotal + tax;
    
    return { subtotal, tax, total };
}

/// This is a TSDoc triple-slash comment
/// It also counts as documentation!
/// @param value - Input value to process
/// @returns Processed value
function processWithTSDoc(value: number): number {
    if (value > 100) {
        if (value > 500) {
            if (value > 1000) {
                return value * 0.5;
            } else {
                return value * 0.7;
            }
        } else {
            return value * 0.9;
        }
    } else {
        return value;
    }
}

// Generic function without docs - should be flagged if complex
function transform<T>(
    items: T[],
    predicate: (item: T) => boolean,
    mapper: (item: T) => T
): T[] {
    const result: T[] = [];
    
    for (const item of items) {
        if (predicate(item)) {
            const mapped = mapper(item);
            if (mapped !== null && mapped !== undefined) {
                result.push(mapped);
            }
        }
    }
    
    return result;
}

export {
    add,
    getUserDiscount,
    processUserOrders,
    calculateOrderTotal,
    processWithTSDoc,
    transform
};
