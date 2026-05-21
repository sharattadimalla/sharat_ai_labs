import csv
import os

from graph.pipeline import run_dataset
from models.schemas import Dataset, DataElement
from output.writer import write_csv

GLOSSARY_TERMS = [
    {"term": "Order ID", "definition": "Unique identifier assigned to each customer order placed through the platform.", "domain": "Orders", "examples": "ORD-10021"},
    {"term": "Customer Email", "definition": "The primary email address associated with a customer's account, used for order notifications and account management.", "domain": "Customers", "examples": "jane@example.com"},
    {"term": "Product SKU", "definition": "Stock Keeping Unit — a unique alphanumeric code assigned to each product variant for inventory tracking.", "domain": "Catalog", "examples": "SKU-9981-BLU"},
    {"term": "Payment Amount", "definition": "The total monetary value charged to the customer for a transaction, inclusive of taxes and fees.", "domain": "Payments", "examples": "249.99"},
    {"term": "Shipment Date", "definition": "The date on which an order is dispatched from the fulfillment center to the carrier.", "domain": "Logistics", "examples": "2024-03-15"},
    {"term": "Discount Code", "definition": "An alphanumeric promotional code applied by a customer to receive a price reduction on their order.", "domain": "Promotions", "examples": "SAVE20"},
    {"term": "Return Reason", "definition": "The customer-provided explanation for returning a product, used to categorize and analyze return trends.", "domain": "Returns", "examples": "Defective product"},
    {"term": "Order Status", "definition": "The current fulfillment state of an order (e.g., Pending, Shipped, Delivered, Cancelled).", "domain": "Orders", "examples": "Shipped"},
    {"term": "Customer ID", "definition": "Unique identifier assigned to each customer account in the CRM system.", "domain": "Customers", "examples": "C-001"},
    {"term": "Order Total", "definition": "The final monetary amount charged to the customer for a completed order, inclusive of taxes and discounts.", "domain": "Orders", "examples": "499.95"},
    {"term": "Billing Address", "definition": "The customer's registered address used for payment verification and invoicing.", "domain": "Payments", "examples": "123 Main St, Springfield"},
    {"term": "Shipping Address", "definition": "The destination address to which an order is delivered.", "domain": "Logistics", "examples": "456 Oak Ave, Portland"},
    {"term": "Product Category", "definition": "A hierarchical classification used to group products of the same type within the catalog.", "domain": "Catalog", "examples": "Electronics > Laptops"},
    {"term": "Payment Method", "definition": "The financial instrument or service used by a customer to complete a transaction (e.g., credit card, PayPal, bank transfer).", "domain": "Payments", "examples": "Credit Card"},
    {"term": "Refund Amount", "definition": "The monetary value returned to the customer following a return or cancellation.", "domain": "Returns", "examples": "89.00"},
]

DATASET = Dataset(
    name="E-Commerce Orders",
    elements=[
        DataElement(name="order_id", data_type="string", sample_values=["ORD-10021", "ORD-10022"]),
        DataElement(name="customer_email", data_type="string", sample_values=["jane@example.com"]),
        DataElement(name="product_sku", data_type="string", sample_values=["SKU-9981-BLU", "SKU-0042-RED"]),
        DataElement(name="payment_amount", data_type="decimal", sample_values=["249.99", "89.00"]),
        DataElement(name="ship_date", data_type="date", sample_values=["2024-03-15"]),
        DataElement(name="discount_code", data_type="string", sample_values=["SAVE20", "WELCOME10"]),
        DataElement(name="return_reason", data_type="string", sample_values=["Defective product", "Wrong size"]),
        DataElement(name="internal_flag", data_type="boolean", sample_values=["true", "false"]),
    ],
)


def _write_sample_glossary() -> str:
    path = os.path.join(os.path.dirname(__file__), "data", "sample_glossary.csv")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["term", "definition", "domain", "examples"])
        writer.writeheader()
        writer.writerows(GLOSSARY_TERMS)
    return path


def main():
    glossary_path = _write_sample_glossary()
    print(f"Glossary: {glossary_path} ({len(GLOSSARY_TERMS)} terms)")
    print(f"Dataset:  {DATASET.name!r} ({len(DATASET.elements)} elements)\n")
    print("-" * 70)

    result = run_dataset(DATASET, glossary_path)

    for r in result.results:
        if r.skipped:
            print(f"[SKIPPED] {r.name}")
            print(f"  Reason:      {r.ai_rationale}")
        else:
            print(f"[{r.ai_confidence_score:.2f}] {r.name}")
            print(f"  Description: {r.ai_generated_description}")
            print(f"  Rationale:   {r.ai_rationale}")
        print()

    output_path = write_csv(result)

    total = len(result.results)
    described = sum(1 for r in result.results if not r.skipped)
    skipped = total - described
    print("-" * 70)
    print(f"Total: {total}  |  Described: {described}  |  Skipped: {skipped}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
