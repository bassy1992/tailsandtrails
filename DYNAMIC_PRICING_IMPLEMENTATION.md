# 🎯 Dynamic Pricing System Implementation

## Overview

The dynamic pricing system allows tour destinations to have different prices based on the number of people in a group. This is a common pricing strategy where larger groups often get discounts per person.

## Features

✅ **Group-based pricing tiers**
✅ **Automatic price calculation**
✅ **Admin interface for managing pricing**
✅ **API endpoints for frontend integration**
✅ **Fallback to base price when no tiers exist**
✅ **Management commands for bulk setup**

## Database Schema

### PricingTier Model

```python
class PricingTier(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='pricing_tiers')
    min_people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_people = models.PositiveIntegerField(blank=True, null=True)  # NULL = unlimited
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Example Pricing Tiers

| Min People | Max People | Price per Person | Description |
|------------|------------|------------------|-------------|
| 1          | 1          | GH₵500.00       | Solo traveler |
| 2          | 3          | GH₵475.00       | Small group (5% discount) |
| 4          | 6          | GH₵450.00       | Medium group (10% discount) |
| 7          | 10         | GH₵425.00       | Large group (15% discount) |
| 11         | NULL       | GH₵400.00       | Extra large group (20% discount) |

## API Endpoints

### 1. Destination List/Detail
```
GET /api/destinations/
GET /api/destinations/{id}/
```

**Response includes:**
```json
{
  "id": 1,
  "name": "Kakum National Park",
  "price": 150.00,
  "has_tiered_pricing": true,
  "pricing_tiers": [
    {
      "id": 1,
      "min_people": 1,
      "max_people": 1,
      "price_per_person": "150.00",
      "group_size_display": "1 person"
    },
    {
      "id": 2,
      "min_people": 2,
      "max_people": 3,
      "price_per_person": "142.50",
      "group_size_display": "2-3 people"
    }
  ]
}
```

### 2. Dynamic Pricing Endpoint
```
GET /api/destinations/{id}/pricing/?group_size={number}
```

**Example Request:**
```
GET /api/destinations/1/pricing/?group_size=4
```

**Response:**
```json
{
  "destination_id": 1,
  "destination_name": "Kakum National Park",
  "group_size": 4,
  "price_per_person": "135.00",
  "total_price": "540.00",
  "base_price": "150.00",
  "has_tiered_pricing": true,
  "pricing_tiers": [
    {
      "id": 3,
      "min_people": 4,
      "max_people": 6,
      "price_per_person": "135.00",
      "group_size_display": "4-6 people",
      "total_price": "540.00"
    }
  ]
}
```

## Admin Interface

### Managing Pricing Tiers

1. **Navigate to Django Admin** → Destinations → Destinations
2. **Edit a destination** and scroll to the "Pricing Tiers" inline section
3. **Add pricing tiers** with min/max people and price per person
4. **Leave max_people blank** for unlimited group size

### Bulk Management

Use the dedicated **PricingTier admin** for bulk operations:
- **Filter by destination category**
- **Search by destination name**
- **Bulk edit pricing tiers**

## Management Commands

### Setup Pricing Tiers

```bash
# Set up pricing tiers for all destinations
python manage.py setup_pricing_tiers

# Set up for specific destination
python manage.py setup_pricing_tiers --destination-id 1

# Overwrite existing tiers
python manage.py setup_pricing_tiers --overwrite
```

## Frontend Integration

### JavaScript Example

```javascript
async function calculatePricing(destinationId, groupSize) {
    const response = await fetch(`/api/destinations/${destinationId}/pricing/?group_size=${groupSize}`);
    const pricing = await response.json();
    
    return {
        pricePerPerson: pricing.price_per_person,
        totalPrice: pricing.total_price,
        hasTieredPricing: pricing.has_tiered_pricing
    };
}

// Usage
const pricing = await calculatePricing(1, 4);
console.log(`Price for 4 people: GH₵${pricing.totalPrice}`);
```

### React Component Example

```jsx
function PricingCalculator({ destinationId }) {
    const [groupSize, setGroupSize] = useState(1);
    const [pricing, setPricing] = useState(null);
    
    useEffect(() => {
        if (destinationId && groupSize) {
            fetch(`/api/destinations/${destinationId}/pricing/?group_size=${groupSize}`)
                .then(res => res.json())
                .then(setPricing);
        }
    }, [destinationId, groupSize]);
    
    return (
        <div>
            <input 
                type="number" 
                value={groupSize} 
                onChange={(e) => setGroupSize(e.target.value)}
                min="1"
            />
            {pricing && (
                <div>
                    <p>Price per person: GH₵{pricing.price_per_person}</p>
                    <p>Total price: GH₵{pricing.total_price}</p>
                </div>
            )}
        </div>
    );
}
```

## Model Methods

### Destination Model

```python
# Get price for specific group size
price = destination.get_price_for_group(group_size=4)

# Check if destination has tiered pricing
has_tiers = destination.has_tiered_pricing

# Get all active pricing tiers
tiers = destination.get_pricing_tiers_display()
```

### PricingTier Model

```python
# Display group size range
tier.group_size_display  # "4-6 people" or "7+ people"
```

## Business Logic

### Price Calculation Algorithm

1. **Find matching tier** where `min_people <= group_size <= max_people`
2. **If multiple tiers match**, use the first one (ordered by min_people)
3. **If no tier matches**, fall back to base destination price
4. **Calculate total** = price_per_person × group_size

### Validation Rules

- **min_people** must be ≥ 1
- **max_people** must be ≥ min_people (if specified)
- **price_per_person** must be ≥ 0
- **No overlapping tiers** for the same destination

## Testing

### Run Tests

```bash
# Test pricing functionality
python test_pricing_tiers.py

# Test API endpoints
python test_pricing_api.py

# View demo in browser
open pricing_demo.html
```

### Test Cases

1. **Single person pricing**
2. **Group discounts**
3. **Maximum group size limits**
4. **Fallback to base price**
5. **API error handling**

## Migration Commands

```bash
# Create and apply migrations
python manage.py makemigrations destinations
python manage.py migrate

# Setup sample data
python manage.py setup_pricing_tiers
```

## Common Use Cases

### 1. Tour Operator Discounts
- Solo travelers pay full price
- Couples get 5% discount
- Groups of 4-8 get 15% discount
- Large groups (9+) get 25% discount

### 2. Accommodation-Based Pricing
- 1-2 people: Single room rate
- 3-4 people: Double room rate
- 5+ people: Group accommodation rate

### 3. Transportation Efficiency
- 1-3 people: Private car
- 4-7 people: Minivan
- 8+ people: Bus (lowest per-person cost)

## Best Practices

### 1. Pricing Strategy
- **Start with base price** for single travelers
- **Offer meaningful discounts** for larger groups (5-25%)
- **Consider operational costs** (transportation, guides, etc.)
- **Set reasonable maximum group sizes**

### 2. Admin Management
- **Use clear tier descriptions** ("Small group", "Family", etc.)
- **Avoid overlapping tiers**
- **Regular price reviews** and updates
- **Test pricing changes** before going live

### 3. Frontend UX
- **Show all pricing tiers** for transparency
- **Highlight current selection**
- **Real-time price updates** as group size changes
- **Clear total price display**

## Troubleshooting

### Common Issues

1. **No pricing tiers showing**
   - Check if `is_active=True` on pricing tiers
   - Verify destination has pricing tiers created

2. **Wrong price calculation**
   - Check tier min/max people ranges
   - Verify no overlapping tiers exist

3. **API errors**
   - Ensure destination exists and is active
   - Validate group_size parameter is positive integer

### Debug Commands

```python
# Check destination pricing
destination = Destination.objects.get(id=1)
print(f"Has tiered pricing: {destination.has_tiered_pricing}")
print(f"Price for 4 people: {destination.get_price_for_group(4)}")

# List all pricing tiers
for tier in destination.pricing_tiers.all():
    print(f"{tier.group_size_display}: GH₵{tier.price_per_person}")
```

## Future Enhancements

### Potential Features
- **Seasonal pricing** (peak/off-peak rates)
- **Dynamic pricing** based on demand
- **Early bird discounts**
- **Last-minute deals**
- **Corporate group rates**
- **Multi-destination package pricing**

---

## Summary

The dynamic pricing system provides a flexible and powerful way to implement group-based pricing for tour destinations. It includes:

- ✅ **Complete database schema** with proper relationships
- ✅ **Admin interface** for easy management
- ✅ **RESTful API endpoints** for frontend integration
- ✅ **Management commands** for bulk operations
- ✅ **Comprehensive testing** and documentation
- ✅ **Real-world examples** and best practices

The system is production-ready and can be easily extended for additional pricing strategies as your business grows.