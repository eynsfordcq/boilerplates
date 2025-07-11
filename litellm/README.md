# litellm

## Provider Specific Configuration

Pass provider specific configuration in litellm_params with extra_body.

Openrouter provider config

```json
{
  "extra_body": {
    "provider": {
      "order": [
        "openai",
        "together"
      ]
    }
  }
}
```

[Gemini thinking config](https://cloud.google.com/vertex-ai/generative-ai/docs/migrate/openai/examples#sample_curl_requests)

```json
{
  "extra_body": {
    "google": {
      "thinking_config": {
        "include_thoughts": true
      }
    }
  }
}
```

