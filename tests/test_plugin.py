import pytest
from platzky.plugin.plugin import ConfigPluginError

from platzky_umami.plugin import UmamiPlugin

WEBSITE_ID = "1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d"


def test_plugin_instantiates():
    plugin = UmamiPlugin({"website_id": WEBSITE_ID})

    assert isinstance(plugin, UmamiPlugin)


def test_accepted_page_sections_is_head_only():
    plugin = UmamiPlugin({"website_id": WEBSITE_ID})

    assert plugin.accepted_page_sections == frozenset({"head"})


def test_get_head_html_defaults_to_umami_cloud():
    plugin = UmamiPlugin({"website_id": WEBSITE_ID})

    head = plugin.get_head_html()

    assert (
        f'<script defer src="https://cloud.umami.is/script.js" data-website-id="{WEBSITE_ID}">'
        in head
    )
    assert head.endswith("<!-- End Umami Analytics -->")


def test_get_head_html_uses_self_hosted_script_url():
    plugin = UmamiPlugin(
        {"website_id": WEBSITE_ID, "script_url": "https://analytics.example.com/script.js"}
    )

    head = plugin.get_head_html()

    assert 'src="https://analytics.example.com/script.js"' in head
    assert "cloud.umami.is" not in head


def test_get_head_html_escapes_script_url_query_string():
    plugin = UmamiPlugin(
        {"website_id": WEBSITE_ID, "script_url": "https://analytics.example.com/s.js?a=1&b=2"}
    )

    head = plugin.get_head_html()

    assert 'src="https://analytics.example.com/s.js?a=1&amp;b=2"' in head


def test_get_body_html_is_empty():
    plugin = UmamiPlugin({"website_id": WEBSITE_ID})

    assert plugin.get_body_html() == ""


def test_website_id_is_normalised():
    plugin = UmamiPlugin({"website_id": WEBSITE_ID.upper()})

    assert f'data-website-id="{WEBSITE_ID}"' in plugin.get_head_html()


@pytest.mark.parametrize(
    "config",
    [
        {},
        {"website_id": ""},
        {"website_id": "not-a-uuid"},
        {"website_id": '"><script>alert(1)</script>'},
        {"website_id": WEBSITE_ID, "script_url": "javascript:alert(1)"},
        {"website_id": WEBSITE_ID, "script_url": "not a url"},
    ],
)
def test_rejects_invalid_config(config: dict[str, str]):
    with pytest.raises(ConfigPluginError):
        UmamiPlugin(config)
