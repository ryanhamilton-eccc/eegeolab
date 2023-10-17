import unittest
import ee
from eegeolab.band_math import NDVI


class TestNDVI(unittest.TestCase):
    def setUp(self):
        ee.Initialize()
        # create an image to test with
        self.image = ee.Image([1, 2]).select([0, 1], ["RED", "NIR"])
        # create an NDVI calculator
        self.ndvi_calc = NDVI(nir="NIR", red="RED")
        self.collection = ee.ImageCollection([self.image, self.image]).select(
            [0, 1], ["RED", "NIR"]
        )

    def test_compute(self):
        # compute the NDVI index
        ndvi_image = self.ndvi_calc.compute(self.image)
        # check that the output is an ee.Image object
        self.assertIsInstance(ndvi_image, ee.Image)
        # check that the output has the expected band name
        self.assertIn(self.ndvi_calc.name, ndvi_image.bandNames().getInfo())

    def test_add(self):
        # add the NDVI band to the image
        image_with_ndvi = self.ndvi_calc.add(self.image)
        # check that the output is an ee.Image object
        self.assertIsInstance(image_with_ndvi, ee.Image)
        # check that the output has the expected band name
        self.assertIn(self.ndvi_calc.name, image_with_ndvi.bandNames().getInfo())

    def test_call(self):
        # add the NDVI band to the image
        map_with_ndvi = self.collection.map(self.ndvi_calc)
        # check that the output is an ee.Image object
        self.assertIsInstance(map_with_ndvi, ee.ImageCollection)
        # check that the output has the expected band name
        self.assertIn(self.ndvi_calc.name, map_with_ndvi.first().bandNames().getInfo())
