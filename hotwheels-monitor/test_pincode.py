#!/usr/bin/env python3
"""
Test script to verify pincode functionality
"""

from firstcry_scraper import FirstCryScraper

def test_pincode():
    scraper = FirstCryScraper()
    
    print("🔍 Testing pincode 401209...")
    products = scraper.search_hotwheels(pincode="401209", max_pages=1)
    
    if products:
        print(f"✅ Found {len(products)} products for pincode 401209:")
        for i, product in enumerate(products[:3], 1):  # Show first 3
            stock_status = "✅ In Stock" if product['in_stock'] else "❌ Out of Stock"
            print(f"{i}. {product['title']}")
            print(f"   Price: {product['price']}")
            print(f"   Status: {stock_status}")
            print()
    else:
        print("❌ No products found for pincode 401209")

if __name__ == "__main__":
    test_pincode()
