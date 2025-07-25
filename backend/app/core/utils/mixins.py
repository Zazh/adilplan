import os
from PIL import Image

class WebPImageMixin:
    webp_quality = 90   # Можно менять в наследниках

    def make_webp(self, field_name):
        image_field = getattr(self, field_name, None)
        if not image_field or not image_field.name:
            return
        src_path = image_field.path
        webp_path = os.path.splitext(src_path)[0] + ".webp"
        try:
            with Image.open(src_path) as im:
                im.save(webp_path, "WEBP", quality=self.webp_quality)
        except Exception as e:
            print(f"Ошибка при конвертации в webp: {e}")

    def get_webp_url(self, field_name):
        image_field = getattr(self, field_name, None)
        if not image_field or not image_field.name:
            return ""
        url = image_field.url
        return os.path.splitext(url)[0] + ".webp"
