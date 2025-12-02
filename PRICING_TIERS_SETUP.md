# Tiered Pricing Setup Guide

## What Was Added

A new `PricingTier` model that allows destinations to have group-based pricing:
- 1 person = GH₵1,200
- 2 people = GH₵2,100 (not GH₵2,400)
- 3+ people = Custom pricing

## Files Changed

### Backend (Django)
1. **Tback/destinations/models.py** - Added `PricingTier` model and `get_price_for_group()` method
2. **Tback/destinations/admin.py** - Added admin interface for managing pricing tiers
3. **Tback/destinations/migrations/0004_pricingtier.py** - Database migration (auto-generated)
4. **Tback/setup_pricing_tiers.py** - Script to populate pricing data

## Deploy to Railway

### Step 1: Push Code to GitHub
```bash
git add Tback/destinations/models.py Tback/destinations/admin.py Tback/destinations/migrations/0004_pricingtier.py Tback/setup_pricing_tiers.py PRICING_TIERS_SETUP.md
git commit -m "Add tiered pricing model for destinations"
git push origin main
```

### Step 2: Railway Will Auto-Deploy
Railway will automatically:
1. Detect the push
2. Run migrations (`python manage.py migrate`)
3. Restart the server

### Step 3: Set Up Pricing via Railway CLI or Django Admin

#### Option A: Using Railway CLI
```bash
# Connect to Railway
railway link

# Run the pricing setup script
railway run python Tback/setup_pricing_tiers.py
```

#### Option B: Using Django Admin (Recommended)
1. Go to: https://tailsandtrails-production.up.railway.app/admin/
2. Login with your superuser credentials
3. Navigate to: **Destinations > Pricing tiers**
4. Click "Add Pricing Tier"
5. For **Tent Xcape**, add:
   - Min people: 1, Max people: 1, Total price: 1200.00
   - Min people: 2, Max people: 2, Total price: 2100.00
   - Min people: 3, Max people: 3, Total price: 2850.00
   - Min people: 4, Max people: 4, Total price: 3400.00
   - Min people: 5, Max people: 10, Total price: 4000.00

#### Option C: Using Railway Shell
```bash
railway run bash
cd Tback
python setup_pricing_tiers.py
exit
```

## How It Works

### Backend
The `Destination` model now has a `get_price_for_group(num_people)` method:
```python
# Example usage
destination = Destination.objects.get(slug='tent-xcape')
price_for_2 = destination.get_price_for_group(2)  # Returns 2100.00
price_for_1 = destination.get_price_for_group(1)  # Returns 1200.00
```

### Frontend Integration (Next Step)
The frontend will need to be updated to:
1. Fetch pricing tiers from the API
2. Calculate total based on number of adults
3. Display the correct price

## API Response Example

After updating the serializer, the API will return:
```json
{
  "id": 1,
  "name": "Tent Xcape",
  "price": "350.00",
  "pricing_tiers": [
    {
      "min_people": 1,
      "max_people": 1,
      "total_price": "1200.00",
      "price_per_person": "1200.00"
    },
    {
      "min_people": 2,
      "max_people": 2,
      "total_price": "2100.00",
      "price_per_person": "1050.00"
    }
  ]
}
```

## Testing

1. Check Django admin: https://tailsandtrails-production.up.railway.app/admin/destinations/pricingtier/
2. Verify pricing tiers are created
3. Test the `get_price_for_group()` method in Django shell

## Next Steps

1. ✅ Deploy backend changes to Railway
2. ⏳ Update API serializers to include pricing_tiers
3. ⏳ Update frontend to use tiered pricing
4. ⏳ Test booking flow with new pricing
