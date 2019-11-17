from django.test import TestCase

# Create your tests here.
from .processing import split_by_char, rounding_number


class ProcessingFile(TestCase):
    
    def test_split_by_char_all_cheks_passed(self):
        result = split_by_char("15:33", ":")
        self.assertEqual(result, ("stringWasSplitted", ["15","33"]))

        result = split_by_char("15:00", ":")
        self.assertEqual(result, ("stringWasSplitted", ["15","00"]))

        result = split_by_char("15,00", ",")
        self.assertEqual(result, ("stringWasSplitted", ["15","00"]))

    def test_split_by_char_all_not_string(self):
        result = split_by_char(13, ",")
        self.assertEqual(result, ("error", ""))

        result = split_by_char(["13:00"], ",")
        self.assertEqual(result, ("error", ""))

    def test_split_by_char_all_empty_separator(self):
        result = split_by_char("13:00", "")
        self.assertEqual(result, ("error", ""))

    def test_split_by_char_separator_not_in_string(self):
        result = split_by_char("13:00", ",")
        self.assertEqual(result, ("error", ""))

        result = split_by_char("13:00", " ")
        self.assertEqual(result, ("error", ""))

class RoundingTemperatureNumbers(TestCase):
    def test_rounding_number(self):
        result = rounding_number(13)
        self.assertEqual(result, 13)

    def test_rounding_up_number(self):
        result = rounding_number(13.4)
        self.assertEqual(result, 13.5)

    def test_rounding_up_number(self):
        result = rounding_number(13.7)
        self.assertEqual(result, 13.5)