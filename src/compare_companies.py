"""
Project: Veridion Entity Resolution Challenge
Author: Mihai Graur
Description: Contains all logic for comparing two company entries and determining
             whether they represent the same entity using fuzzy string matching
             and rule-based field comparisons.
"""

import pandas as pd
from thefuzz import fuzz

# Normalize string values for consistent comparisons
def normalize(text):
    if pd.isna(text):
        return ""
    return str(text).lower().strip().replace(".", "").replace(",", "")

# Utility: Extract and normalize a field from both rows
def extract_normalized_fields(row1, row2, field):
    return normalize(row1.get(field, "")), normalize(row2.get(field, ""))

# Compare names using all three name-related fields with tailored fuzziness
def compare_names_flexibly(name1, name2, legal1, legal2, commercial1, commercial2):
    comparisons = [
        (name1, name2, ["partial_token_sort_ratio", "partial_ratio"]),
        (name1, legal2, ["partial_ratio"]),
        (legal1, name2, ["partial_ratio"]),
        (legal1, legal2, ["ratio", "partial_ratio"]),
        (commercial1, commercial2, ["token_set_ratio", "partial_ratio"]),
        (name1, commercial2, ["token_set_ratio"]),
        (commercial1, name2, ["token_set_ratio"]),
        (legal1, commercial2, ["token_sort_ratio"]),
        (commercial1, legal2, ["token_sort_ratio"]),
    ]

    # Block match if all name fields are missing
    if not any([name1, name2, legal1, legal2, commercial1, commercial2]):
        return False

    for n1, n2, methods in comparisons:
        if not n1 or not n2:
            continue

        max_score = 0
        for method in methods:
            if method == "ratio":
                score = fuzz.ratio(n1, n2)
            elif method == "partial_ratio":
                score = fuzz.partial_ratio(n1, n2)
            elif method == "token_sort_ratio":
                score = fuzz.token_sort_ratio(n1, n2)
            elif method == "token_set_ratio":
                score = fuzz.token_set_ratio(n1, n2)
            elif method == "partial_token_sort_ratio":
                score = fuzz.partial_token_sort_ratio(n1, n2)
            else:
                continue

            max_score = max(max_score, score)

        if max_score > 90:
            return True

    return False


# Check for exact match on useful "almost unique" fields like domain or phone
def exact_field_match(val1, val2):
    return val1 and val1 == val2

# Main function to decide whether two companies are duplicates
def is_duplicate_enhanced(row1, row2):
    # Extract name-related fields
    name1, name2             = extract_normalized_fields(row1, row2, "company_name")
    legal1, legal2           = extract_normalized_fields(row1, row2, "company_legal_names")
    commercial1, commercial2 = extract_normalized_fields(row1, row2, "company_commercial_names")

    # Extract other identity fields
    country_code1, country_code2 = extract_normalized_fields(row1, row2, "main_country_code")
    country_text1, country_text2 = extract_normalized_fields(row1, row2, "main_country")
    region1, region2             = extract_normalized_fields(row1, row2, "main_region")
    product1, product2           = extract_normalized_fields(row1, row2, "product_type")

    phone1, phone2   = extract_normalized_fields(row1, row2, "primary_phone")
    domain1, domain2 = extract_normalized_fields(row1, row2, "website_domain")
    url1, url2       = extract_normalized_fields(row1, row2, "website_url")

    postcode1, postcode2       = extract_normalized_fields(row1, row2, "main_postcode")
    city1, city2               = extract_normalized_fields(row1, row2, "main_city")
    raw_address1, raw_address2 = extract_normalized_fields(row1, row2, "main_address_raw_text")

    # Rule 1: Exact match on domain or URL
    if exact_field_match(domain1, domain2) or exact_field_match(url1, url2):
        return True

    # Rule 2: Fuzzy name match + country + product match
    if compare_names_flexibly(name1, name2, legal1, legal2, commercial1, commercial2):
        country_match = (
            (country_code1 and country_code1 == country_code2) or
            (country_text1 and country_text1 == country_text2)
        )
        product_match = product1 and product1 == product2
        if country_match and product_match:
            return True

    # Rule 3: Fallback match based on name + location or phone
    address_match = (
        (postcode1 and postcode1 == postcode2) or
        (city1 and city1 == city2) or
        (raw_address1 and raw_address1 == raw_address2) or
        (region1 and region1 == region2)
    )
    phone_match = phone1 and phone1 == phone2

    if compare_names_flexibly(name1, name2, legal1, legal2, commercial1, commercial2):
        if phone_match or address_match:
            return True

    # If there is no match
    return False
