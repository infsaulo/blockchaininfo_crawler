import pytest
from utils import calculate_precision, calculate_average_precision

class TestUtils:
    relevant_entries = [1,2,4,6,8,9,10]
    retrieved_entries = [1,2,4,8,9,13,6]

    def test_calculate_precision(self):
        precision_value = calculate_precision(self.relevant_entries, self.retrieved_entries)
        assert precision_value >= 0.85 and precision_value <= 0.858

    def test_calculate_average_precision(self):
        average_precision = calculate_average_precision(self.relevant_entries, self.retrieved_entries)
        assert average_precision >= 0.89 and average_precision <= 0.892
