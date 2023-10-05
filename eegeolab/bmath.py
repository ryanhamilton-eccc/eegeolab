from typing import Any
import ee


# TODO add NDVI, SAVI, Tasseled cap, phase, amplitude


class NDVI:
    def __init__(self, nir: str, red: str, name: str = None) -> None:
        self.nir = nir
        self.red = red
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = "NDVI" if name is None else name

    def __call__(self, image: ee.Image) -> Any:
        return image.addBands(self.compute(image=image))

    def compute(self, image: ee.Image) -> ee.Image:
        """Computes the NDVI for the input Image

        Args:
            image (ee.Image): Image to calculate NDVI

        Returns:
            ee.Image: a Image that represents the NDVI values
        """
        return image.normalizedDifference([self.nir, self.red]).rename(self.name)


class SAVI:
    def __init__(self, nir: str, red: str, L: float = 0.5, name: str = None) -> None:
        self.nir = nir
        self.red = red
        self.L = L
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = "SAVI" if name is None else name

    def __call__(self, image: ee.Image) -> Any:
        return image.addBands(self.compute(image=image))

    def compute(self, image: ee.Image) -> ee.Image:
        return image.expression(
            "(1 + L) * (NIR - RED) / (NIR + RED + L)",
            {
                "NIR": image.select(self.nir),
                "RED": image.select(self.red),
                "L": self.L,
            },
        ).rename(self.name)
