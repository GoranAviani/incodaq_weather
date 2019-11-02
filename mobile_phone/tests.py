from django.test import TestCase

# Create your tests here.
from .views import is_mobile_still_validated


class MobileValidation(TestCase):
    
    def test_mobile_number_not_digit(self):
        result = is_mobile_still_validated("073123123", "abc")
        self.assertEqual(result, (False))

        result = is_mobile_still_validated("073123123", "a123bc")
        self.assertEqual(result, (False))

        result = is_mobile_still_validated("073123123", "123.4")
        self.assertEqual(result, (False))

    def test_mobile_number_short(self):
        result = is_mobile_still_validated("073123123", "073")
        self.assertEqual(result, (False))

    def test_mobile_numbers_not_same(self):
        result = is_mobile_still_validated("073123123", "0731231234")
        self.assertEqual(result, (False))

