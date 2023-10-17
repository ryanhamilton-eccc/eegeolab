# eegeolab/bandmath/ndvi.py
"""
Provides a class and methods for calculating NDVI

this module allows a user to construct a NDVI calculator object to compute NDVI as well as provides 
functionality to map the calculator to and Image Collection, add to a indvivual image, and compute
the index

Examples:
    >>> from band_math import NDVI
    >>> import ee
    >>> ee.Initialize()
    >>> ndvi_calc = NDVI(nir='B4', red='B4')
    >>> ndvi_calc.compute(image)
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import ee


class BandMathatics:
    """Abstract Base Class for Band Math Calculators"""

    def __call__(self, image: ee.Image) -> ee.Image:
        """Makes the calculator callable, class camp be mapped as an algo to an Image Collection

        Args:
            image (ee.Image): Image to compute index

        Returns:
            ee.Image: the origianl image with the index image appended to it
        """
        return self.add(image)

    @abstractmethod
    def compute(self, image: ee.Image) -> ee.Image:
        """Computes the index for the defined image, based on the equation

        Args:
            image (ee.Image): Image to compute index from

        Returns:
            ee.Image: the index image
        """
        pass

    def add(self, image: ee.Image) -> ee.Image:
        """Adds the computed index to the defined image, calls the compute method

        Args:
            image (ee.Image): Image to compute index from

        Returns:
            ee.Image: the original image with the index band appended to it.
        """
        return image.addBands(self.compute(image))


class NDVI:
    def __init__(self, nir: str, red: str, name: str = None) -> None:
        """NDVI Calculator Class

        Args:
            nir (str): Near Infrared Band name
            red (str): Red Band name
            name (str, optional): Name of the index. Defaults to NDVI.
        """
        self.nir = nir
        self.red = red
        self.name = name

    def __call__(self, image: ee.Image) -> ee.Image:
        """Makes the calculator callable, class camp be mapped as an algo to an Image Collection

        Args:
            image (ee.Image): Image to compute NDVI

        Returns:
            ee.Image: the origianl image with the ndvi image appended to it
        """
        return self.add(image)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, __value: str):
        self._name = "NDVI" if __value is None else __value

    def compute(self, image: ee.Image) -> ee.Image:
        """Computes the Normalized  Difference Vegetation Index for the defined image

        Args:
            image (ee.Image): Image to compute ndvi from

        Returns:
            ee.Image: a ndvi image from the input image
        """
        return image.normalizedDifference([self.nir, self.red]).rename(self.name)

    def add(self, image: ee.Image) -> ee.Image:
        """Adds the computed index to the defined image, calls the compute method

        Args:
            image (ee.Image): Image to compute ndvi from

        Returns:
            ee.Image: the original image with the NDVI band appended to it.
        """
        return image.addBands(self.compute(image))
