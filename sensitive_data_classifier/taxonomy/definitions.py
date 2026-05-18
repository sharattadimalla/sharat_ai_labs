from __future__ import annotations

SENSITIVE_TAGS: list[dict] = [
    # ── PII ──────────────────────────────────────────────────────────────────
    {
        "label": "PII - Full Name",
        "description": (
            "An individual's full name, first name, last name, or any combination "
            "that can identify a natural person."
        ),
        "handling_policy": (
            "Encrypt at rest and in transit; mask in non-production environments; "
            "restrict access to authorized personnel only."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - Email Address",
        "description": (
            "Electronic mail address belonging to an individual, used for personal "
            "or professional communication."
        ),
        "handling_policy": (
            "Encrypt at rest and in transit; mask in non-production environments; "
            "do not share with third parties without consent."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - Phone Number",
        "description": (
            "Telephone number of an individual, including mobile, home, or work numbers, "
            "domestic or international formats."
        ),
        "handling_policy": (
            "Encrypt at rest; mask all but last 4 digits in non-production; "
            "restrict access to authorized systems."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - Social Security Number",
        "description": (
            "US Social Security Number (SSN) or equivalent government-issued "
            "national identification number used for tax and social benefit purposes."
        ),
        "handling_policy": (
            "Tokenize or encrypt; never log in plaintext; mask all but last 4 digits; "
            "audit all access; comply with applicable state breach-notification laws."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - Date of Birth",
        "description": (
            "An individual's date of birth or age, which in combination with other "
            "fields can uniquely identify a person."
        ),
        "handling_policy": (
            "Encrypt at rest; mask full date in non-production (retain only year for analytics); "
            "restrict access."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - Home Address",
        "description": (
            "Residential or mailing address of an individual, including street, city, "
            "state, postal code, or country."
        ),
        "handling_policy": (
            "Encrypt at rest; mask in non-production; do not expose in public APIs; "
            "apply data minimization — store only what is necessary."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - IP Address",
        "description": (
            "Internet Protocol address (IPv4 or IPv6) that can identify a user's device "
            "or network location and is considered personal data under GDPR."
        ),
        "handling_policy": (
            "Anonymize or truncate before storing for analytics; "
            "retain only with legal basis; apply short retention periods."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - National Identification Number",
        "description": (
            "Government-issued national ID number (excluding SSN), such as a national "
            "insurance number, Aadhaar, NRIC, or equivalent."
        ),
        "handling_policy": (
            "Encrypt at rest and in transit; tokenize where possible; "
            "audit all access; comply with local data-protection laws."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - Passport Number",
        "description": (
            "Unique identifier printed on an individual's passport issued by a national "
            "government for international travel and identity verification."
        ),
        "handling_policy": (
            "Encrypt at rest; store only as long as necessary for the stated purpose; "
            "restrict access to identity-verification workflows only."
        ),
        "frameworks": ["PII", "GDPR"],
    },
    {
        "label": "PII - Driver's License Number",
        "description": (
            "Government-issued driver's license number used for identity verification "
            "and eligibility to operate a motor vehicle."
        ),
        "handling_policy": (
            "Encrypt at rest; mask in non-production; "
            "restrict to identity-verification and fraud-prevention use cases."
        ),
        "frameworks": ["PII", "GDPR"],
    },

    # ── PHI ──────────────────────────────────────────────────────────────────
    {
        "label": "PHI - Medical Record Number",
        "description": (
            "Unique identifier assigned to a patient's health record by a healthcare "
            "provider or hospital system."
        ),
        "handling_policy": (
            "HIPAA-compliant encryption at rest and in transit; strict role-based access; "
            "audit all read/write operations; de-identify for analytics."
        ),
        "frameworks": ["PHI", "HIPAA", "GDPR"],
    },
    {
        "label": "PHI - Diagnosis Code",
        "description": (
            "Medical diagnosis represented by a standardized code (ICD-10, ICD-11, SNOMED) "
            "that describes a patient's condition or disease."
        ),
        "handling_policy": (
            "HIPAA-compliant encryption; restrict access to clinical and authorized billing staff; "
            "do not expose in non-clinical analytics without de-identification."
        ),
        "frameworks": ["PHI", "HIPAA", "GDPR"],
    },
    {
        "label": "PHI - Medication Name",
        "description": (
            "Name of a prescribed or administered medication, drug, or pharmaceutical "
            "product associated with a patient."
        ),
        "handling_policy": (
            "HIPAA-compliant encryption; restrict to clinical workflows; "
            "de-identify for population-level analytics."
        ),
        "frameworks": ["PHI", "HIPAA", "GDPR"],
    },
    {
        "label": "PHI - Lab Result",
        "description": (
            "Results from clinical laboratory tests including blood work, urinalysis, "
            "pathology, or other diagnostic tests tied to a patient."
        ),
        "handling_policy": (
            "HIPAA-compliant encryption at rest and in transit; "
            "role-based access limited to treating clinicians; audit trail required."
        ),
        "frameworks": ["PHI", "HIPAA", "GDPR"],
    },
    {
        "label": "PHI - Health Insurance ID",
        "description": (
            "Insurance member ID, policy number, group number, or subscriber identifier "
            "associated with an individual's health insurance coverage."
        ),
        "handling_policy": (
            "Encrypt at rest; mask in non-production; "
            "HIPAA-compliant handling; restrict to billing and claims workflows."
        ),
        "frameworks": ["PHI", "HIPAA", "GDPR"],
    },
    {
        "label": "PHI - Biometric Data",
        "description": (
            "Physiological or behavioral measurements uniquely identifying a person, "
            "such as fingerprints, retinal scans, facial geometry, or voice patterns "
            "collected in a healthcare context."
        ),
        "handling_policy": (
            "Encrypt at rest with strong encryption; never store raw biometrics when a "
            "hash/template suffices; HIPAA and GDPR special-category compliance required."
        ),
        "frameworks": ["PHI", "HIPAA", "GDPR"],
    },

    # ── PCI DSS ───────────────────────────────────────────────────────────────
    {
        "label": "PCI - Card Number (PAN)",
        "description": (
            "Primary Account Number (PAN) on a payment card — the 13-19 digit number "
            "embossed or encoded on credit, debit, or prepaid cards."
        ),
        "handling_policy": (
            "Never store post-authorization without tokenization; "
            "mask all but last 4 digits in any display; never log; "
            "PCI DSS scope — quarterly audits required."
        ),
        "frameworks": ["PCI DSS"],
    },
    {
        "label": "PCI - Card Verification Value (CVV)",
        "description": (
            "Card security code (CVV2, CVC2, CID) printed on a payment card and used "
            "to verify card-not-present transactions."
        ),
        "handling_policy": (
            "Must NEVER be stored after authorization — PCI DSS prohibition; "
            "never log or transmit in plaintext; immediate purge after auth."
        ),
        "frameworks": ["PCI DSS"],
    },
    {
        "label": "PCI - Card Expiration Date",
        "description": (
            "Expiry month and year printed on a payment card, used alongside the PAN "
            "for transaction authorization."
        ),
        "handling_policy": (
            "Do not store unless strictly required; if stored, encrypt; "
            "never display in full; purge when no longer needed."
        ),
        "frameworks": ["PCI DSS"],
    },
    {
        "label": "PCI - Bank Account Number",
        "description": (
            "Unique number identifying a customer's bank account at a financial institution, "
            "used for ACH, wire transfers, and direct deposits."
        ),
        "handling_policy": (
            "Encrypt at rest and in transit; mask all but last 4 digits; "
            "restrict to payment-processing systems; audit all access."
        ),
        "frameworks": ["PCI DSS", "PII"],
    },
    {
        "label": "PCI - Bank Routing Number",
        "description": (
            "ABA routing transit number (RTN) identifying the financial institution for "
            "ACH and wire-transfer transactions."
        ),
        "handling_policy": (
            "Encrypt at rest; restrict to payment-processing workflows; "
            "do not expose in application logs."
        ),
        "frameworks": ["PCI DSS", "PII"],
    },

    # ── GDPR Special Categories ───────────────────────────────────────────────
    {
        "label": "GDPR Special - Racial or Ethnic Origin",
        "description": (
            "Data revealing the racial or ethnic origin of a natural person, "
            "a special category under GDPR Article 9."
        ),
        "handling_policy": (
            "Processing prohibited without explicit consent or a lawful GDPR Art. 9 basis; "
            "encrypt at rest; strict access controls; data minimization required; "
            "retain only as long as legally necessary."
        ),
        "frameworks": ["GDPR Special Category"],
    },
    {
        "label": "GDPR Special - Religious Belief",
        "description": (
            "Data revealing religious or philosophical beliefs of a natural person, "
            "a special category under GDPR Article 9."
        ),
        "handling_policy": (
            "Processing prohibited without explicit consent or a lawful GDPR Art. 9 basis; "
            "encrypt at rest; restrict access; apply data minimization."
        ),
        "frameworks": ["GDPR Special Category"],
    },
    {
        "label": "GDPR Special - Political Opinion",
        "description": (
            "Data revealing political opinions of a natural person, "
            "a special category under GDPR Article 9."
        ),
        "handling_policy": (
            "Processing prohibited without explicit consent or lawful basis; "
            "encrypt at rest; strict access controls; never use for automated profiling."
        ),
        "frameworks": ["GDPR Special Category"],
    },
    {
        "label": "GDPR Special - Sexual Orientation",
        "description": (
            "Data concerning the sexual orientation or gender identity of a natural person, "
            "a special category under GDPR Article 9."
        ),
        "handling_policy": (
            "Processing prohibited without explicit consent or lawful basis; "
            "highest-level encryption; strict need-to-know access; "
            "never infer or share with third parties."
        ),
        "frameworks": ["GDPR Special Category"],
    },
    {
        "label": "GDPR Special - Trade Union Membership",
        "description": (
            "Data revealing whether an individual is a member of a trade union, "
            "a special category under GDPR Article 9."
        ),
        "handling_policy": (
            "Processing prohibited without explicit consent or lawful basis; "
            "encrypt at rest; restrict to HR systems with strict access controls."
        ),
        "frameworks": ["GDPR Special Category"],
    },
    {
        "label": "GDPR Special - Genetic Data",
        "description": (
            "Personal data relating to inherited or acquired genetic characteristics "
            "that gives unique information about a person's physiology or health, "
            "a special category under GDPR Article 9."
        ),
        "handling_policy": (
            "Processing prohibited without explicit consent or lawful basis; "
            "GDPR and HIPAA (if health-related) compliance required; "
            "encrypt at rest; data subject rights must be supported."
        ),
        "frameworks": ["GDPR Special Category", "PHI"],
    },
]
