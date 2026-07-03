import unittest
from validator import (
    validate_required,
    validate_customer_id,
    validate_email,
    validate_date
)


class TestValidator(unittest.TestCase):

    # --- validate_required ---
    def test_required_with_valid_value_returns_none(self):
        self.assertIsNone(validate_required("test", "필드"))

    def test_required_with_empty_string_returns_error(self):
        self.assertIsNotNone(validate_required("", "필드"))

    def test_required_with_whitespace_returns_error(self):
        self.assertIsNotNone(validate_required("   ", "필드"))

    def test_required_with_none_returns_error(self):
        self.assertIsNotNone(validate_required(None, "필드"))

    # --- validate_customer_id ---
    def test_customer_id_valid_returns_none(self):
        self.assertIsNone(validate_customer_id("C001"))
        self.assertIsNone(validate_customer_id("C999"))

    def test_customer_id_empty_returns_error(self):
        self.assertIsNotNone(validate_customer_id(""))

    def test_customer_id_lowercase_c_returns_error(self):
        self.assertIsNotNone(validate_customer_id("c001"))

    def test_customer_id_too_few_digits_returns_error(self):
        self.assertIsNotNone(validate_customer_id("C01"))

    def test_customer_id_too_many_digits_returns_error(self):
        self.assertIsNotNone(validate_customer_id("C0001"))

    def test_customer_id_no_letter_prefix_returns_error(self):
        self.assertIsNotNone(validate_customer_id("001"))

    def test_customer_id_c000_returns_error(self):
        self.assertIsNotNone(validate_customer_id("C000"))

    def test_customer_id_special_chars_returns_error(self):
        self.assertIsNotNone(validate_customer_id("C@01"))

    # --- validate_email ---
    def test_email_valid_returns_none(self):
        self.assertIsNone(validate_email("test@example.com"))

    def test_email_no_at_returns_error(self):
        self.assertIsNotNone(validate_email("testexample.com"))

    def test_email_multiple_at_returns_error(self):
        self.assertIsNotNone(validate_email("test@test@example.com"))

    def test_email_empty_local_returns_error(self):
        self.assertIsNotNone(validate_email("@example.com"))

    def test_email_empty_domain_returns_error(self):
        self.assertIsNotNone(validate_email("test@"))

    def test_email_no_dot_in_domain_returns_error(self):
        self.assertIsNotNone(validate_email("test@examplecom"))

    def test_email_empty_string_returns_error(self):
        self.assertIsNotNone(validate_email(""))

    def test_email_whitespace_returns_error(self):
        self.assertIsNotNone(validate_email("   "))

    # --- validate_date ---
    def test_date_valid_returns_none(self):
        self.assertIsNone(validate_date("2026-06-09"))

    def test_date_invalid_format_returns_error(self):
        self.assertIsNotNone(validate_date("2026/06/09"))

    def test_date_wrong_order_returns_error(self):
        self.assertIsNotNone(validate_date("09-06-2026"))

    def test_date_february_29_leap_year_returns_none(self):
        self.assertIsNone(validate_date("2024-02-29"))

    def test_date_february_29_non_leap_year_returns_error(self):
        self.assertIsNotNone(validate_date("2025-02-29"))

    def test_date_month_13_returns_error(self):
        self.assertIsNotNone(validate_date("2026-13-01"))

    def test_date_day_32_returns_error(self):
        self.assertIsNotNone(validate_date("2026-01-32"))

    def test_date_empty_returns_error(self):
        self.assertIsNotNone(validate_date(""))


if __name__ == '__main__':
    unittest.main()