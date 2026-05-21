FEW_SHOT_EXAMPLES = [
    {
        "field": "customer_id",
        "data_type": "string",
        "sample_values": ["C-001", "C-002"],
        "glossary_terms": [
            {
                "term": "Customer ID",
                "definition": "Unique identifier assigned to each customer account in the CRM system.",
            }
        ],
        "description": "A unique system-assigned identifier that distinguishes each customer account within the CRM platform.",
        "rationale": "Directly matched to glossary term 'Customer ID'; sample values confirm the alphanumeric format.",
        "confidence": 0.95,
    },
    {
        "field": "order_total",
        "data_type": "decimal",
        "sample_values": ["249.99", "89.00"],
        "glossary_terms": [
            {
                "term": "Order Total",
                "definition": "The final monetary amount charged to the customer for a completed order, inclusive of taxes and discounts.",
            }
        ],
        "description": "The final monetary amount charged to the customer for a completed order, including applicable taxes and any applied discounts.",
        "rationale": "Matched to glossary term 'Order Total'; decimal sample values confirm a monetary field.",
        "confidence": 0.92,
    },
    {
        "field": "ship_date",
        "data_type": "date",
        "sample_values": ["2024-03-15"],
        "glossary_terms": [
            {
                "term": "Shipment Date",
                "definition": "The date on which an order is dispatched from the fulfillment center to the carrier.",
            }
        ],
        "description": "The date on which the order was dispatched from the fulfillment center and handed to the carrier for delivery.",
        "rationale": "Field name 'ship_date' maps directly to glossary term 'Shipment Date'.",
        "confidence": 0.90,
    },
]
