# Destinations API Endpoints

## Base URL: `http://127.0.0.1:8000/api`

### Categories
- **GET** `/categories/` - List all destination categories
  ```json
  [
    {
      "id": 1,
      "name": "Heritage",
      "slug": "heritage",
      "description": "Historical and cultural heritage sites"
    }
  ]
  ```

### Destinations
- **GET** `/destinations/` - List all destinations with filtering
  - Query parameters:
    - `search` - Search by name, location, description
    - `category` - Filter by category ID
    - `duration` - Filter by duration (1_day, 2_days, etc.)
    - `price_category` - Filter by price range (budget, mid, luxury)
    - `duration_category` - Filter by duration category (day, weekend, week)
    - `ordering` - Sort by price, rating, created_at
  
  ```json
  [
    {
      "id": 1,
      "name": "Cape Coast Castle Heritage Tour",
      "slug": "cape-coast-castle-heritage-tour",
      "location": "Cape Coast",
      "description": "Explore the historic Cape Coast Castle...",
      "image": "https://images.pexels.com/...",
      "price": "450.00",
      "duration": "2_days",
      "duration_display": "2 Days",
      "max_group_size": 15,
      "rating": "4.80",
      "reviews_count": 124,
      "category": {
        "id": 1,
        "name": "Heritage",
        "slug": "heritage",
        "description": "Historical and cultural heritage sites"
      },
      "highlights": [
        {"highlight": "UNESCO World Heritage Site"},
        {"highlight": "Guided Historical Tour"}
      ],
      "includes": [
        {"item": "Transport"},
        {"item": "Accommodation"}
      ],
      "price_category": "mid",
      "is_featured": true
    }
  ]
  ```

- **GET** `/destinations/{slug}/` - Get destination details
  - Returns detailed information including images and all related data

### Reviews
- **GET** `/destinations/{destination_id}/reviews/` - Get destination reviews
  ```json
  [
    {
      "id": 1,
      "rating": 5,
      "title": "Amazing experience!",
      "comment": "The tour was fantastic...",
      "user_name": "John",
      "is_verified": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
  ```

### Statistics
- **GET** `/stats/` - Get destination statistics
  ```json
  {
    "total_destinations": 9,
    "categories_count": 5,
    "featured_destinations": 4
  }
  ```

### Bookings (Authenticated Users Only)
- **GET** `/bookings/` - List user's bookings
- **POST** `/bookings/` - Create new booking
- **GET** `/bookings/{id}/` - Get booking details
- **PUT** `/bookings/{id}/` - Update booking

## Example API Calls

### Get all destinations
```bash
curl http://127.0.0.1:8000/api/destinations/
```

### Search destinations
```bash
curl "http://127.0.0.1:8000/api/destinations/?search=castle"
```

### Filter by category
```bash
curl "http://127.0.0.1:8000/api/destinations/?category=1"
```

### Filter by price range
```bash
curl "http://127.0.0.1:8000/api/destinations/?price_category=budget"
```

### Get destination details
```bash
curl http://127.0.0.1:8000/api/destinations/cape-coast-castle-heritage-tour/
```

### Get statistics
```bash
curl http://127.0.0.1:8000/api/stats/
```