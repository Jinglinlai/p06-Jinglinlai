import unittest

from thumbor.ext.filters import _round_corner

WIDTH = 40
HEIGHT = 40
RADIUS = 10
BLUE = (0, 0, 255)


class RoundCornerFringeTestCase(unittest.TestCase):
    def apply_transparent(self):
        data = bytes([0, 0, 255, 255]) * (WIDTH * HEIGHT)
        result = _round_corner.apply(
            1,
            "RGBA",
            RADIUS,
            RADIUS,
            0,
            0,
            0,
            WIDTH,
            HEIGHT,
            data,
            1,
        )
        return bytes(result)

    def pixel(self, data, x, y):
        i = 4 * (y * WIDTH + x)
        return data[i], data[i + 1], data[i + 2], data[i + 3]

    def test_edge_pixels_keep_their_color(self):
        data = self.apply_transparent()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r, g, b, a = self.pixel(data, x, y)
                if a == 255:
                    self.assertEqual(
                        (r, g, b),
                        BLUE,
                        f"opaque pixel at {x},{y} lost its color",
                    )

    def test_edge_pixels_are_partly_transparent(self):
        data = self.apply_transparent()
        partial = [
            self.pixel(data, x, y)
            for y in range(HEIGHT)
            for x in range(WIDTH)
            if 0 < self.pixel(data, x, y)[3] < 255
        ]
        self.assertTrue(partial, "no anti-aliased edge pixel found")

    def test_corner_pixel_is_transparent(self):
        data = self.apply_transparent()
        self.assertEqual(self.pixel(data, 0, 0)[3], 0)
