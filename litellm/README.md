# litellm

## Provider Specific Configuration

Pass provider specific configuration in litellm_params with extra_body.

[Openrouter provider config](https://openrouter.ai/docs/features/provider-routing)

```json
{
  "extra_body": {
    "provider": {
      "order": [
        "Chutes"
      ],
      "allow_fallbacks": false
    }
  },
}
```

## Gemini include thoughts summary

- [Gemini thinking config](https://cloud.google.com/vertex-ai/generative-ai/docs/migrate/openai/examples#sample_curl_requests)
- [LiteLLM config](https://docs.litellm.ai/docs/providers/vertex#thinking--reasoning_content)

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

```json
{"thinking": {"type": "enabled"}}
```

