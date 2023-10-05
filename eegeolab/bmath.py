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


class TasseledCap:
    def __init__(
        self, blue: str, green: str, red: str, nir: str, swir1: str, swir2: str
    ) -> None:
        self.blue = blue
        self.green = green
        self.red = red
        self.nir = nir
        self.swir1 = swir1
        self.swir2 = swir2

    def __call__(self, image: ee.Image) -> Any:
        return image.addBands(self.compute(image=image))

    def compute(self, image: ee.Image) -> ee.Image:
        image = image.select(list(self.__dict__.values()))
        co_array = [
            [0.3037, 0.2793, 0.4743, 0.5585, 0.5082, 0.1863],
            [-0.2848, -0.2435, -0.5436, 0.7243, 0.0840, -0.1800],
            [0.1509, 0.1973, 0.3279, 0.3406, -0.7112, -0.4572],
        ]

        co = ee.Array(co_array)

        arrayImage1D = image.toArray()
        arrayImage2D = arrayImage1D.toArray(1)

        components_image = (
            ee.Image(co)
            .matrixMultiply(arrayImage2D)
            .arrayProject([0])
            .arrayFlatten([["Brightness", "Greenness", "Wetness"]])
        )

        return components_image


class Phase:
    def __init__(
        self, mode: int, sin_prefix: str = None, cos_prefix: str = None
    ) -> None:
        self.mode = mode
        self.sin_prefix = sin_prefix
        self.cos_prefix = cos_prefix

    def __call__(self, image: ee.Image) -> Any:
        return image.addBands(self.compute(image=image))

    @property
    def sin_prefix(self):
        return self._sin_prefix

    @sin_prefix.setter
    def sin_prefix(self, prefix: str):
        if prefix is None:
            self._sin_prefix = "sin"
        else:
            self._sin_prefix = prefix

    @property
    def cos_prefix(self):
        return self._cos_prefix

    @cos_prefix.setter
    def cos_prefix(self, prefix: str):
        if prefix is None:
            self._cos_prefix = "cos"
        else:
            self._cos_prefix = prefix

    def compute(self, image: ee.Image) -> ee.Image:
        from math import pi

        cos, sin = f"{self.cos_prefix}_{self.mode}", f"{self.sin_prefix}_{self.mode}"
        return (
            image.select(sin).atan2(cos).unitScale(-pi, pi).rename(f"phase_{self.mode}")
        )


class Amplitude:
    def __init__(
        self, mode: int, sin_prefix: str = None, cos_prefix: str = None
    ) -> None:
        self.mode = mode
        self.sin_prefix = sin_prefix
        self.cos_prefix = cos_prefix

    def __call__(self, image: ee.Image) -> Any:
        return image.addBands(self.compute(image=image))

    @property
    def sin_prefix(self):
        return self._sin_prefix

    @sin_prefix.setter
    def sin_prefix(self, prefix: str):
        if prefix is None:
            self._sin_prefix = "sin"
        else:
            self._sin_prefix = prefix

    @property
    def cos_prefix(self):
        return self._cos_prefix

    @cos_prefix.setter
    def cos_prefix(self, prefix: str):
        if prefix is None:
            self._cos_prefix = "cos"
        else:
            self._cos_prefix = prefix

    def compute(self, image: ee.Image) -> ee.Image:
        from math import pi

        cos, sin = f"{self.cos_prefix}_{self.mode}", f"{self.sin_prefix}_{self.mode}"
        return image.select(sin).hypot(cos).rename(f"amp_{self.mode}")
