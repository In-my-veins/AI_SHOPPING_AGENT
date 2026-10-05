"""
Reviews API - reads from the `reviews` table in the store.db and returns
aggregated rating information for products.
"""

import sqlite3
import os
from langchain.tools import tool

DB_PATH = os.path.join(os.path.dirname(__file__), "store.db")

@tool
def get_product_rating(product_id: int) -> dict:
    """Return average rating and review count for a single product."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ?",
        (product_id,),
    )

    row = cursor.fetchone()
    conn.close()

    avg = round(row[0], 2) if row and row[0] is not None else 0.0
    count = row[1] if row else 0

    return {
        "product_id": product_id,
        "average_rating": avg,
        "review_count": count
    }
 
@tool 
def get_ratings_for_products(product_ids: list[int]) -> list[dict]:
    """Return average rating and review count for multiple products."""

    results = []

    for product_id in product_ids:
        result = get_product_rating.invoke({
        "product_id": product_id
        })
        results.append(result)
        
    return results    
    

if __name__ == "__main__":
    result = get_product_rating.invoke({
    "product_id": 1
})

    print("Single product rating:")
    print(
        f"  Product {result['product_id']}: "
        f"{result['average_rating']} stars "
        f"({result['review_count']} reviews)"
    )

    print("\nMultiple product ratings:")

    results = get_ratings_for_products.invoke({
    "product_ids": [1, 3, 5, 7]
})

    for result in results:
        print(
            f"  Product {result['product_id']}: "
            f"{result['average_rating']} stars "
            f"({result['review_count']} reviews)"
        )




       