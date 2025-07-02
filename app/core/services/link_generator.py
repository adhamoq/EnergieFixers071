"""
Link generator service to produce pre-filled KoboToolbox URLs.
"""
import urllib.parse
from config import Config

class LinkGeneratorService:
    """Generate pre-filled KoboToolbox form links"""

    def __init__(self):
        self.default_form_url = "https://ee-eu.kobotoolbox.org/x/Evnz0R4w"

    @staticmethod
    def validate_url(url: str):
        return any(
            domain in url.lower()
            for domain in [
                "kobotoolbox.org",
                "kf.kobotoolbox.org",
                "ee-eu.kobotoolbox.org",
            ]
        )

    def generate_link(self, form_url: str, fields: dict | None = None):
        if not fields:
            return form_url
        params = []
        group = "introductie"
        for key, val in fields.items():
            if val:
                params.append(
                    f"d[{group}/{key}]=" + urllib.parse.quote_plus(str(val).strip())
                )
        return form_url + "?" + "&".join(params) if params else form_url

    @staticmethod
    def default_fields():
        return {"adres": "", "afspraakTijd": "", "uitvoerders": ""}