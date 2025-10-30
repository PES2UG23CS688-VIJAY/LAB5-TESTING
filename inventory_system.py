"""Inventory management system module.

This module defines an InventoryManager class for adding,
removing, and tracking inventory items with JSON-based
storage and secure, PEP8-compliant code.
"""

import json
import logging



class InventoryManager:
    """Inventory management system with static analysis issues fixed."""

    def __init__(self, file_name="inventory.json"):
        self.file_name = file_name
        self.stock_data = {}
        logging.basicConfig(
            filename="inventory.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def add_item(self, item, qty):
        """Add an item with the specified quantity."""
        if not isinstance(item, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(qty, int):
            raise TypeError("Quantity must be an integer.")
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")

        current_qty = self.stock_data.get(item, 0)
        self.stock_data[item] = current_qty + qty
        logging.info("Added %d of %s", qty, item)

    def remove_item(self, item, qty):
        """Remove quantity of an item from stock."""
        if not isinstance(item, str) or not isinstance(qty, int):
            raise TypeError("Invalid item name or quantity type.")

        if item not in self.stock_data:
            logging.warning(
                "Attempted to remove non-existent item: %s", item
            )
            return

        self.stock_data[item] -= qty
        if self.stock_data[item] <= 0:
            del self.stock_data[item]
            logging.info(
                "Removed all of %s (now zero or negative)",
                item,
            )
        else:
            logging.info("Removed %d of %s", qty, item)

    def get_qty(self, item):
        """Return current quantity of an item."""
        return self.stock_data.get(item, 0)

    def load_data(self):
        """Load stock data from JSON file."""
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                self.stock_data = json.load(file)
            logging.info(
                "Data loaded successfully from %s",
                self.file_name,
            )
        except FileNotFoundError:
            logging.warning(
                "File %s not found, starting with empty data.",
                self.file_name,
            )
            self.stock_data = {}
        except json.JSONDecodeError:
            logging.error(
                "Invalid JSON format in %s.",
                self.file_name,
            )
            self.stock_data = {}

    def save_data(self):
        """Save stock data to JSON file."""
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self.stock_data, file, indent=4)
        logging.info(
            "Data saved successfully to %s",
            self.file_name,
        )

    def print_data(self):
        """Print all items and their quantities."""
        print("Items Report")
        for item, qty in self.stock_data.items():
            print(f"{item} -> {qty}")

    def check_low_items(self, threshold=5):
        """Return list of items below threshold quantity."""
        return [
            item for item, qty in self.stock_data.items()
            if qty < threshold
        ]


def main():
    """Main function to demonstrate inventory operations."""
    inv = InventoryManager()
    inv.load_data()

    try:
        inv.add_item("apple", 10)
        inv.add_item("banana", 2)
        inv.remove_item("apple", 3)
        inv.remove_item("orange", 1)  # Not in stock
    except (TypeError, ValueError) as e:
        logging.error("Error: %s", e)

    print("Apple stock:", inv.get_qty("apple"))
    print("Low items:", inv.check_low_items())
    inv.save_data()
    inv.print_data()


if __name__ == "__main__":
    main()
