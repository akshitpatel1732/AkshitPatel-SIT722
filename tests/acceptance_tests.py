# File: tests/acceptance_tests.py

import argparse
import httpx
import sys
import random
import time

# Helper to exit the script on failure
def fail_test(message):
    print(f"ACCEPTANCE TEST FAILED: {message}")
    sys.exit(1)

def main(product_url, order_url, customer_url):
    print("--- Starting End-to-End Acceptance Tests ---")
    
    # Use a random number to ensure test data is unique for each run
    run_id = random.randint(1000, 9999)
    customer_id = None
    product_id = None
    
    try:
        client = httpx.Client(timeout=10)

        # --- Step 1: Create a new Customer ---
        print(f"\n[1/4] Creating a new customer...")
        customer_data = {
            "email": f"testuser{run_id}@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": f"User{run_id}",
            "phone_number": "0987654321",
            "shipping_address": "Deakin University",
        }
        response = client.post(f"{customer_url}/customers/", json=customer_data)
        if response.status_code != 201:
            fail_test(f"Failed to create customer. Status: {response.status_code}, Body: {response.text}")
        customer_id = response.json()["customer_id"]
        print(f"Customer created successfully with ID: {customer_id}")

        # --- Step 2: Create a new Product ---
        print(f"\n[2/4] Creating a new product...")
        product_data = {
            "name": f"Acceptance Test Widget {run_id}",
            "description": "A product for our E2E test.",
            "price": 19.99,
            "stock_quantity": 50
        }
        response = client.post(f"{product_url}/products/", json=product_data)
        if response.status_code != 201:
            fail_test(f"Failed to create product. Status: {response.status_code}, Body: {response.text}")
        product_id = response.json()["product_id"]
        print(f"Product created successfully with ID: {product_id}")
        
        # --- Step 3: Place an Order ---
        print(f"\n[3/4] Placing an order for the new product...")
        order_data = {
            "user_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "price_at_purchase": 19.99
                }
            ]
        }
        response = client.post(f"{order_url}/orders/", json=order_data)
        if response.status_code != 201:
            fail_test(f"Failed to create order. Status: {response.status_code}, Body: {response.text}")
        order_id = response.json()["order_id"]
        print(f"Order placed successfully with ID: {order_id}")

        # --- Step 4: Verify the Order Status and Stock Deduction ---
        print(f"\n[4/4] Verifying order status and stock deduction...")
        # Give a moment for any backend processing if needed
        time.sleep(2)
        
        # Verify order status is 'confirmed'
        response = client.get(f"{order_url}/orders/{order_id}")
        if response.status_code != 200 or response.json()["status"] != "confirmed":
            fail_test(f"Order status verification failed. Expected 'confirmed', got '{response.json().get('status')}'.")
        print("Order status is 'confirmed' as expected.")

        # Verify product stock has been deducted
        response = client.get(f"{product_url}/products/{product_id}")
        new_stock = response.json()["stock_quantity"]
        if new_stock != 48: # Initial stock was 50, ordered 2
            fail_test(f"Stock deduction verification failed. Expected 48, found {new_stock}.")
        print(f"Product stock correctly deducted to {new_stock}.")

    except httpx.RequestError as e:
        fail_test(f"A network error occurred: {e}")
    finally:
        # --- Cleanup Phase ---
        print("\n--- Starting Cleanup ---")
        if product_id:
            print(f"Deleting product {product_id}...")
            client.delete(f"{product_url}/products/{product_id}")
        if customer_id:
            print(f"Deleting customer {customer_id}...")
            client.delete(f"{customer_url}/customers/{customer_id}")
        print("Cleanup complete.")
    
    print("\n--- All Acceptance Tests Passed! ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E2E Acceptance Tests.")
    parser.add_argument("--product-url", required=True)
    parser.add_argument("--order-url", required=True)
    parser.add_argument("--customer-url", required=True)
    args = parser.parse_args()
    
    main(args.product_url, args.order_url, args.customer_url)