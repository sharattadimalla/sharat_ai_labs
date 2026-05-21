from graph.pipeline import run_dataset
from models.schemas import Dataset, DataElement

dataset = Dataset(
    name="HR & Payments System",
    elements=[
        DataElement(
            name="employee_email",
            data_type="string",
            description="Work email address of the employee",
            sample_values=["jane.doe@company.com"],
        ),
        DataElement(
            name="ssn",
            data_type="string",
            description="Social security number for payroll and tax purposes",
            sample_values=["123-45-6789"],
            format="XXX-XX-XXXX",
        ),
        DataElement(
            name="card_pan",
            data_type="string",
            description="Primary account number on the employee's corporate credit card",
            sample_values=["4111111111111111"],
            format="16-digit numeric",
        ),
        DataElement(
            name="diagnosis_code",
            data_type="string",
            description="ICD-10 diagnosis code from the employee health insurance claim",
            sample_values=["J45.20"],
        ),
        DataElement(
            name="date_of_birth",
            data_type="date",
            description="Employee date of birth used for benefits eligibility",
            sample_values=["1985-04-23"],
            format="YYYY-MM-DD",
        ),
        DataElement(
            name="religion",
            data_type="string",
            description="Employee's declared religion for holiday scheduling purposes",
            sample_values=["Islam", "Christianity"],
        ),
        DataElement(
            name="department_code",
            data_type="string",
            description="Internal department identifier for organizational reporting",
            sample_values=["ENG-42", "HR-07"],
        ),
        DataElement(
            name="ip_address",
            data_type="string",
            description="IP address logged when the employee accessed the HR portal",
            sample_values=["192.168.1.105"],
        ),
        DataElement(
            name="product_sku",
            data_type="string",
            description="Stock keeping unit for an inventory item",
            sample_values=["SKU-9981-BLU"],
        ),
    ],
)


def main():
    print(f"Classifying dataset: {dataset.name!r} ({len(dataset.elements)} elements)\n")
    print("-" * 70)

    result = run_dataset(dataset)

    for r in result.results:
        flag = "NEEDS REVIEW" if r.needs_review else "OK"
        print(f"[{flag}] [{r.confidence_level}] {r.data_element_name}")
        print(f"  Label:  {r.predicted_sensitive_data_label}")
        print(f"  Score:  {r.confidence_score:.2f}")
        print(f"  Reason: {r.ai_reasoning}")
        print(f"  Policy: {r.recommended_handling_policy}")
        print()

    total = len(result.results)
    sensitive = sum(1 for r in result.results if r.predicted_sensitive_data_label != "Not Sensitive")
    needs_review = sum(1 for r in result.results if r.needs_review)

    print("-" * 70)
    print(f"Total: {total}  |  Sensitive: {sensitive}  |  Needs review: {needs_review}")


if __name__ == "__main__":
    main()
