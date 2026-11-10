from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def make_binary_alpha_gif():
    # Top half is opaque white (index 1), bottom half is index 0,
    # which is marked as the transparent entry.
    src = Image.new("P", (20, 20), 0)
    src.putpalette([0, 0, 0, 255, 255, 255] + [0, 0, 0] * 254)
    src.paste(1, (0, 0, 20, 10))
    buffer = BytesIO()
    src.save(buffer, "GIF", transparency=0)
    return buffer.getvalue()


def test_resized_gif_keeps_its_transparent_pixels():
    config = Config(
        PILLOW_PRESERVE_INDEXED_MODE=True, ALLOW_ANIMATED_GIFS=False
    )
    engine = Engine(Context(config=config))
    engine.extension = ".gif"
    engine.image = engine.create_image(make_binary_alpha_gif())
    engine.resize(10, 10)

    result = engine.read(".gif")
    out = Image.open(BytesIO(result))

    assert "transparency" in out.info
    alpha = out.convert("RGBA").getchannel("A")
    assert alpha.getextrema()[0] == 0
