"""
Project: Veridion Entity Resolution Challenge
Author: Mihai Graur
Description: Unit tests for the entity resolution comparison logic,
             ensuring correctness of the matching algorithm across multiple scenarios.
"""

import sys
# Prevent Python from creating .pyc files
sys.dont_write_bytecode = True
sys.path.append("src")

from compare_companies import is_duplicate_enhanced

# Test fuzzy matching for name similarity with different formats
def test_google_duplicate():
    company1 = {
        "company_name": "Google Inc.",
        "company_legal_names": "",
        "company_commercial_names": "Google",
        "main_country_code": "us",
        "product_type": "search"
    }

    company2 = {
        "company_name": "Google Incorporated",
        "company_legal_names": "Google Inc.",
        "company_commercial_names": "",
        "main_country_code": "us",
        "product_type": "search"
    }

    assert is_duplicate_enhanced(company1, company2) == True

# Negative test: completely different companies
def test_apple_vs_google():
    company1 = {
        "company_name": "Apple Inc.",
        "main_country_code": "us",
        "product_type": "hardware"
    }

    company2 = {
        "company_name": "Google Inc.",
        "main_country_code": "us",
        "product_type": "search"
    }

    assert is_duplicate_enhanced(company1, company2) == False

# Should be different: country codes differ despite name similarity
def test_valantic_vs_valantic_erp():
    company1 = {
        "company_name": "Valantic",
        "company_legal_names": "",
        "company_commercial_names": "",
        "main_country_code": "at",
        "product_type": "information technology and services"
    }

    company2 = {
        "company_name": "valantic ERP Consulting GmbH",
        "company_legal_names": "",
        "company_commercial_names": "",
        "main_country_code": "de",
        "product_type": "information technology and services"
    }

    assert is_duplicate_enhanced(company1, company2) == False

# Very different company names
def test_valantic_vs_dabero():
    company1 = {
        "company_name": "Valantic",
        "main_country_code": "at",
        "product_type": "information technology and services"
    }

    company2 = {
        "company_name": "Dabero Service Group GmbH",
        "main_country_code": "de",
        "product_type": "information technology and services"
    }

    assert is_duplicate_enhanced(company1, company2) == False

# Different domain/industry
def test_valantic_vs_punkt_komma():
    company1 = {
        "company_name": "Valantic",
        "main_country_code": "at",
        "product_type": "information technology and services"
    }

    company2 = {
        "company_name": "Punkt & Komma GmbH",
        "main_country_code": "at",
        "product_type": "marketing and advertising"
    }

    assert is_duplicate_enhanced(company1, company2) == False

# Same product, same country, but different names
def test_valantic_erp_vs_dabero():
    company1 = {
        "company_name": "valantic ERP Consulting GmbH",
        "main_country_code": "de",
        "product_type": "information technology and services"
    }

    company2 = {
        "company_name": "Dabero Service Group GmbH",
        "main_country_code": "de",
        "product_type": "information technology and services"
    }

    assert is_duplicate_enhanced(company1, company2) == False

# Match on domain and address
def test_cordenpharma_gmbh_vs_cordenpharma():
    company1 = {
        "company_name": "Corden Pharma GmbH",
        "company_legal_names": "CordenPharma GmbH",
        "company_commercial_names": "CordenPharma",
        "main_country_code": "de",
        "main_country": "germany",
        "main_postcode": "71672",
        "main_city": "marbach am neckar",
        "main_region": "baden-württemberg",
        "product_type": "manufacturing",
        "primary_phone": "",
        "website_domain": "cordenpharma.com"
    }

    company2 = {
        "company_name": "CordenPharma GmbH",
        "company_legal_names": "",
        "company_commercial_names": "",
        "main_country_code": "de",
        "main_country": "germany",
        "main_postcode": "71672",
        "main_city": "marbach am neckar",
        "main_region": "baden-württemberg",
        "product_type": "manufacturing",
        "primary_phone": "",
        "website_domain": "cordenpharma.com"
    }

    assert is_duplicate_enhanced(company1, company2) == True

# Match by domain and product type
def test_cordenpharma_gmbh_vs_international():
    company1 = {
        "company_name": "CordenPharma GmbH",
        "company_legal_names": "CordenPharma GmbH",
        "company_commercial_names": "CordenPharma",
        "main_country_code": "de",
        "main_country": "germany",
        "main_postcode": "71672",
        "main_city": "marbach am neckar",
        "main_region": "baden-württemberg",
        "product_type": "manufacturing",
        "primary_phone": "",
        "website_domain": "cordenpharma.com"
    }

    company2 = {
        "company_name": "CordenPharma International GmbH",
        "company_legal_names": "CordenPharma International GmbH",
        "company_commercial_names": "",
        "main_country_code": "de",
        "main_country": "germany",
        "main_postcode": "",
        "main_city": "",
        "main_region": "",
        "product_type": "manufacturing",
        "primary_phone": "",
        "website_domain": "cordenpharma.com"
    }

    assert is_duplicate_enhanced(company1, company2) == True

# Fallback case for same domain, no matching address
def test_cordenpharma_vs_international():
    company1 = {
        "company_name": "CordenPharma GmbH",
        "company_legal_names": "",
        "company_commercial_names": "",
        "main_country_code": "de",
        "main_country": "germany",
        "main_postcode": "71672",
        "main_city": "marbach am neckar",
        "main_region": "baden-württemberg",
        "product_type": "manufacturing",
        "primary_phone": "",
        "website_domain": "cordenpharma.com"
    }

    company2 = {
        "company_name": "CordenPharma International GmbH",
        "company_legal_names": "CordenPharma International GmbH",
        "company_commercial_names": "",
        "main_country_code": "de",
        "main_country": "germany",
        "main_postcode": "",
        "main_city": "",
        "main_region": "",
        "product_type": "manufacturing",
        "primary_phone": "",
        "website_domain": "cordenpharma.com"
    }

    assert is_duplicate_enhanced(company1, company2) == True

# Should NOT match: all name fields missing and address inconsistent
def test_missing_names_grouped_by_address_and_domain():
    company1 = {
        "company_name": "",
        "company_legal_names": "",
        "company_commercial_names": "",
        "main_country_code": "TW",
        "main_country": "Taiwan",
        "main_city": "Taichung",
        "main_postcode": "43770",
        "main_region": "Taichung",
        "website_domain": "",
        "all_domains": ""
    }

    company2 = {
        "company_name": "",
        "company_legal_names": "",
        "company_commercial_names": "",
        "main_country_code": "TW",
        "main_country": "Taiwan",
        "main_city": "",
        "main_postcode": "",
        "main_region": "",
        "website_domain": "",
        "all_domains": "redsakura.com.tw"
    }

    assert is_duplicate_enhanced(company1, company2) == False

# Should match: no names, but same domain and phone number
def test_no_name_fields_but_same_domain_and_phone():
    company1 = {
        "company_name": "",
        "company_legal_names": "",
        "company_commercial_names": "",
        "website_domain": "example.com",
        "primary_phone": "+123456789",
        "main_country_code": "us",
        "product_type": "software"
    }

    company2 = {
        "company_name": "",
        "company_legal_names": "",
        "company_commercial_names": "",
        "website_domain": "example.com",
        "primary_phone": "+123456789",
        "main_country_code": "us",
        "product_type": "software"
    }

    assert is_duplicate_enhanced(company1, company2) == True

# Running tests
test_google_duplicate()
test_apple_vs_google()
print("Basic company comparison tests passed.")

test_valantic_vs_valantic_erp()
test_valantic_vs_dabero()
test_valantic_vs_punkt_komma()
test_valantic_erp_vs_dabero()
print("Valantic group tests passed.")

test_cordenpharma_gmbh_vs_cordenpharma()
test_cordenpharma_gmbh_vs_international()
test_cordenpharma_vs_international()
print("CordenPharma tests passed.")

test_missing_names_grouped_by_address_and_domain()
test_no_name_fields_but_same_domain_and_phone()
print("Edge case tests passed.")
