/**
 * Sample JavaScript file to test Cognitive Guard
 */

/**
 * Simple function with documentation
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 */
function add(a, b) {
    return a + b;
}

/**
 * Calculate discount with multiple conditions
 * @param {number} price - Original price
 * @param {string} customerType - Type of customer (regular, premium, vip)
 * @param {boolean} hasPromo - Whether customer has promo code
 * @returns {number} Final price after discount
 */
function calculateDiscount(price, customerType, hasPromo) {
    let discount = 0;
    
    if (customerType === 'premium') {
        discount = 0.10;
        if (hasPromo) {
            discount += 0.05;
        }
    } else if (customerType === 'vip') {
        discount = 0.20;
        if (hasPromo) {
            discount += 0.10;
        }
    } else {
        if (hasPromo) {
            discount = 0.05;
        }
    }
    
    return price * (1 - discount);
}

// VERY COMPLEX function without JSDoc - should trigger violation!
function veryComplexUndocumented(data, config, options, filters) {
    let result = {};
    let count = 0;
    
    if (data && data.length > 0) {
        for (let item of data) {
            if (config.validate) {
                if (item.type === 'special') {
                    if (options.includeSpecial) {
                        if (filters.priceRange) {
                            if (item.price > filters.priceRange.min) {
                                if (item.price < filters.priceRange.max) {
                                    result[item.id] = item.value * 2;
                                    count++;
                                } else {
                                    result[item.id] = item.value;
                                }
                            }
                        } else {
                            result[item.id] = item.value * 2;
                        }
                    } else {
                        result[item.id] = 0;
                    }
                } else if (item.type === 'regular') {
                    if (options.includeRegular) {
                        if (filters.category) {
                            if (item.category === filters.category) {
                                result[item.id] = item.value;
                                count++;
                            }
                        } else {
                            result[item.id] = item.value;
                        }
                    }
                } else {
                    if (options.includeOther) {
                        result[item.id] = item.value * 0.5;
                    }
                }
            } else {
                result[item.id] = item.value;
            }
        }
    }
    
    return { result, count };
}

/**
 * Process order with shipping calculation
 * @param {Array} items - Array of items to process
 * @param {Object} shipping - Shipping configuration
 * @returns {Object} Processed order details
 */
function processOrder(items, shipping) {
    const total = items.reduce((sum, item) => {
        return sum + item.price * item.quantity;
    }, 0);
    
    let shippingCost = 0;
    if (shipping.method === 'express') {
        shippingCost = 15.99;
    } else if (shipping.method === 'standard') {
        shippingCost = 5.99;
    }
    
    return {
        subtotal: total,
        shipping: shippingCost,
        total: total + shippingCost
    };
}

// Another complex function without docs
function complexArrow(x, y, z, w) {
    if (x > 0) {
        if (y > 0) {
            if (z > 0) {
                if (w > 0) {
                    return x + y + z + w;
                } else {
                    return x + y + z;
                }
            } else {
                if (w > 0) {
                    return x + y + w;
                } else {
                    return x + y;
                }
            }
        } else {
            if (z > 0) {
                if (w > 0) {
                    return x + z + w;
                } else {
                    return x + z;
                }
            } else {
                return x;
            }
        }
    } else {
        return 0;
    }
}

module.exports = {
    add,
    calculateDiscount,
    veryComplexUndocumented,
    processOrder,
    complexArrow
};
