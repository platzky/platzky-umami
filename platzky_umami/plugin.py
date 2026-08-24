"""Platzky Umami plugin — injects the Umami analytics script into the page head."""

import inspect
from html import escape
from typing import Any
from uuid import UUID

from platzky.plugin.html_injector import HtmlInjectorPluginBase, PageSection
from platzky.plugin.plugin import ConfigPluginError
from pydantic import BaseModel, HttpUrl, ValidationError

CLOUD_SCRIPT_URL = "https://cloud.umami.is/script.js"


class UmamiConfig(BaseModel):
    """Configuration model for the Umami plugin."""

    website_id: UUID
    script_url: HttpUrl = HttpUrl(CLOUD_SCRIPT_URL)


class UmamiPlugin(HtmlInjectorPluginBase):
    """Platzky plugin that injects the Umami analytics script into the page head."""

    accepted_page_sections: frozenset[PageSection] = frozenset({"head"})

    def __init__(self, config: dict[str, Any]) -> None:
        """Validate the plugin configuration."""
        super().__init__(config)
        try:
            self.umami_config = UmamiConfig.model_validate(config)
        except ValidationError as e:
            raise ConfigPluginError(str(e)) from e

    def get_head_html(self) -> str:
        """Return the Umami tracking script tag to inject into the page head."""
        # website_id is a validated UUID, so it needs no escaping; script_url can legitimately
        # carry a query string, whose "&" must not be read as an HTML entity.
        src = escape(str(self.umami_config.script_url), quote=True)
        website_id = str(self.umami_config.website_id)

        return inspect.cleandoc(f"""
            <!-- Umami Analytics -->
            <script defer src="{src}" data-website-id="{website_id}"></script>
            <!-- End Umami Analytics -->
        """)
