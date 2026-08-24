# platzky-umami

Platzky plugin that injects the [Umami](https://umami.is) analytics script into the page
`<head>`. Umami is a privacy-focused, cookie-free analytics tool, so no consent banner is
needed for a default install.

## Installation

```sh
pip install platzky_umami
```

## Getting the website ID

In your Umami dashboard go to **Settings → Websites → Edit** for the site you want to track.
The **Website ID** is a UUID such as `1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d`. It is public —
it ends up in the page source — so it is not a secret.

## Activation

Add the plugin to the `plugins` mapping in your Platzky database configuration. The key must
match the entry-point name declared in `pyproject.toml` (`umami`):

```json
{
    "plugins": {
        "umami": {
            "is_active": true,
            "config": {
                "website_id": "1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d"
            },
            "allowed_page_sections": ["head"]
        }
    }
}
```

`allowed_page_sections` is the admin-side allowlist and is required: the engine injects only
the intersection of it and what the plugin declares. This plugin declares `head` only, so
omitting `allowed_page_sections` (or leaving it empty) loads the plugin but injects nothing.

That configuration renders into every page's `<head>`:

```html
<!-- Umami Analytics -->
<script defer src="https://cloud.umami.is/script.js" data-website-id="1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d"></script>
<!-- End Umami Analytics -->
```

## Configuration

| Key | Required | Default | Description |
|---|---|---|---|
| `website_id` | yes | — | Website ID from the Umami dashboard. Must be a UUID. |
| `script_url` | no | `https://cloud.umami.is/script.js` | Tracker script URL. Point it at your own instance when self-hosting. |

### Self-hosted Umami

```json
{
    "plugins": {
        "umami": {
            "is_active": true,
            "config": {
                "website_id": "1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d",
                "script_url": "https://analytics.example.com/script.js"
            },
            "allowed_page_sections": ["head"]
        }
    }
}
```

An invalid `website_id` or `script_url` raises `ConfigPluginError` at startup rather than
shipping a broken script tag.

## Development

```sh
poetry install
make dev            # lint, then pyright
make lint-check     # CI gate
make coverage       # branch coverage, fails under 90%
```
