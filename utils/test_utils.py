from django.test import TestCase
from unittest.mock import patch
from utils.utils import get_latlng_range, get_distance, addr_to_lat_lng, calculate_seulsegown_score
import json
import math
import requests


class CalculateScoreTest(TestCase):
    def test_calculate_score(self):
        jumpos = [
            {'distance': 100},
            {'distance': 250},
            {'distance': 350},
            {'distance': 500}
        ]
        self.assertEqual(calculate_seulsegown_score(jumpos), 6)

    def test_max_score(self):
        jumpos = [
            {'distance': 50},
            {'distance': 100},
            {'distance': 150},
            {'distance': 200},
            {'distance': 250},
            {'distance': 300},
            {'distance': 350},
            {'distance': 400},
            {'distance': 450},
            {'distance': 500},
        ]
        self.assertEqual(calculate_seulsegown_score(jumpos), 10)

    def test_min_score(self):
        jumpos = [
            {'distance': 500},
            {'distance': 600},
            {'distance': 700},
        ]
        self.assertEqual(calculate_seulsegown_score(jumpos), 0)


class GetLatLngRangeTest(TestCase):
    def test_get_latlng_range(self):

        seoul_latlng = (37.566826004661, 126.978652258309)
        distance = 0.3  # km
        expected_min_latlng = (37.56412803984325, 126.97524849954188)
        expected_max_latlng = (37.56952396947876, 126.98205601707612)

        result_min_latlng, result_max_latlng = get_latlng_range(seoul_latlng, distance)

        self.assertAlmostEqual(result_min_latlng[0], expected_min_latlng[0], places=2)
        self.assertAlmostEqual(result_min_latlng[1], expected_min_latlng[1], places=2)
        self.assertAlmostEqual(result_max_latlng[0], expected_max_latlng[0], places=2)
        self.assertAlmostEqual(result_max_latlng[1], expected_max_latlng[1], places=2)


class GetDistanceTest(TestCase):
    def test_get_distance(self):

        store_a_latlng = (37.5838711265173, 126.997717557893) # 이마트24 R종로성대점
        store_b_latlng = (37.5832620762326, 127.00044833319) # CU 대학로2호점
        expected_distance = 0.25  # km

        result_distance = get_distance(*store_a_latlng, *store_b_latlng)

        self.assertAlmostEqual(result_distance, expected_distance, places=2)


class AddrToLatLngTestCase(TestCase):
    def setUp(self):
        self.mock_result = {
            'documents': [
                {
                    'address': {
                        'x': '126.977829174031',
                        'y': '37.5663174209601'
                    }
                }
            ]
        }

    @patch('requests.get')
    def test_addr_to_lat_lng(self, mock_get):

        mock_get.return_value.ok = True
        mock_get.return_value.text = json.dumps(self.mock_result)

        address = '서울특별시 중구 세종대로 110 (태평로1가)'
        expected_lng_lat = (126.977829174031, 37.5663174209601)

        result_lng_lat = addr_to_lat_lng(address)
        self.assertEqual(result_lng_lat, expected_lng_lat)
