import unittest

import numpy as np

from kappaschedules.cosine_decreasing import CosineDecreasing
from kappaschedules.cosine_increasing import CosineIncreasing


class TestCosineDecreasing(unittest.TestCase):
    def test_decreasing(self):
        sched = CosineDecreasing()
        expected = [
            1.0,
            0.9755282581475768,
            0.9045084971874737,
            0.7938926261462366,
            0.6545084971874737,
            0.5,
            0.3454915028125263,
            0.20610737385376354,
            0.09549150281252627,
            0.02447174185242318,
            0.0,
        ]
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

    def test_increasing(self):
        sched = CosineIncreasing()
        expected = [
            0.0,
            0.024471741852423234,
            0.09549150281252633,
            0.2061073738537635,
            0.34549150281252633,
            0.5,
            0.6545084971874737,
            0.7938926261462366,
            0.9045084971874737,
            0.9755282581475768,
            1.0,
        ]
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

    def test_increasing_absmin(self):
        sched = CosineIncreasing(start_value=1e-5)
        expected = [
            1e-05,
            0.02448149713500471,
            0.0955005478974982,
            0.20611531278002496,
            0.3454980478974982,
            0.500005,
            0.6545119521025018,
            0.7938946872199751,
            0.9045094521025019,
            0.9755285028649954,
            1.0,
        ]
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)
