from django.test import TestCase

# Create your tests here.
from .views import is_mobile_still_validated


class MobileValidation(TestCase):
    
    def test_mobile_short(self):
        result = is_mobile_still_validated("073123123", "073")
        self.assertEqual(result, (False))

