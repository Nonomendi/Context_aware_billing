import json
import os 

# Set up absolute pathing to prevent folder mismatch issues
FILE_PATH = os.path.join(os.path.dirname(__file__), "database.json")

def read_database():
    """Opens the database file, reads it, and returns the data inside it."""
    with open(FILE_PATH, "r") as file:
        return json.load(file)
    

def save_database(data):
    """Takes updated data and writes it back to the file."""
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=2)
        

def get_customer_details(customer_id: str) -> dict | str:
    """
    Fetches the account status and billing details for a specific customer.

    Args:
        customer_id: The unique identifier for the customer (e.g., 'CUST-101').
    """
    db = read_database()
    for customer in db["customers"]:
        if customer["customer_id"].lower() == customer_id.lower():
            return customer
    return "Customer not found."


def update_customer_tier(customer_id: str, new_tier: str, new_rate: float) -> str:
    """
    Updates a customer's subscription tier level and monthly rate.

    Args:
        customer_id: The unique identifier for the customer (e.g., 'CUST-101').
        new_tier: The name of the target plan tier (e.g., 'Premium').
        new_rate: The numeric billing price for the tier (e.g., 350.00).
    """
    db = read_database()
    for customer in db["customers"]:
        if customer["customer_id"].lower() == customer_id.lower():
            old_tier = customer.get("customer_tier", "Unknown")
            customer["customer_tier"] = new_tier
            customer["monthly_rate"] = new_rate
            customer["system_notes"] += f" | Tier updated from {old_tier} to {new_tier} via AI Agent."
            save_database(db)
            return f"Successfully updated {customer_id} to {new_tier}."
        
    return "Customer not found."

if __name__ == "__main__":
    print("---Reading Customer---")
    print(get_customer_details("CUST-101"))
    
    print("\n---Updating Customer ---")
    print(update_customer_tier("CUST-101", "Premium", 350.00))