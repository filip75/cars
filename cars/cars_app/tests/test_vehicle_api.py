from unittest import TestCase
from unittest.mock import patch

from cars_app.vehicle_api import get_models_of_a_make, vehicle_exists

FIAT_API_RESPONSE = {
    "Count": 10,
    "Message": "Response returned successfully",
    "SearchCriteria": "Make:fiat",
    "Results": [
        {"Make_ID": 492, "Make_Name": "FIAT", "Model_ID": 2037, "Model_Name": "500L"},
        {"Make_ID": 492, "Make_Name": "FIAT", "Model_ID": 2055, "Model_Name": "500"},
        {
            "Make_ID": 492,
            "Make_Name": "FIAT",
            "Model_ID": 3490,
            "Model_Name": "Freemont",
        },
        {"Make_ID": 492, "Make_Name": "FIAT", "Model_ID": 10396, "Model_Name": "500X"},
        {
            "Make_ID": 492,
            "Make_Name": "FIAT",
            "Model_ID": 11448,
            "Model_Name": "124 Spider",
        },
        {
            "Make_ID": 492,
            "Make_Name": "FIAT",
            "Model_ID": 14603,
            "Model_Name": "Spider 2000",
        },
        {
            "Make_ID": 492,
            "Make_Name": "FIAT",
            "Model_ID": 14604,
            "Model_Name": "X 1\/9",
        },
        {"Make_ID": 492, "Make_Name": "FIAT", "Model_ID": 14605, "Model_Name": "Brava"},
        {
            "Make_ID": 492,
            "Make_Name": "FIAT",
            "Model_ID": 14606,
            "Model_Name": "Strada",
        },
        {
            "Make_ID": 492,
            "Make_Name": "FIAT",
            "Model_ID": 25128,
            "Model_Name": "Ducato",
        },
    ],
}


class VehicleApiTest(TestCase):
    def test_get_models_of_a_make(self):
        with patch("cars_app.vehicle_api.requests") as requests:
            get_models_of_a_make("Fiat")

            requests.get.assert_called_with(
                "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/Fiat?format=json"
            )

    def test_vehicle_exists_positive(self):
        with patch("cars_app.vehicle_api.get_models_of_a_make") as get_models:
            get_models.return_value = FIAT_API_RESPONSE

            self.assertTrue(vehicle_exists("Fiat", "500"))

    def test_vehicle_exists_negative(self):
        with patch("cars_app.vehicle_api.get_models_of_a_make") as get_models:
            get_models.return_value = FIAT_API_RESPONSE

            self.assertFalse(vehicle_exists("Fiat", "126"))
