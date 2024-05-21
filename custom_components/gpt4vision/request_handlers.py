from homeassistant.exceptions import ServiceValidationError
import logging

_LOGGER = logging.getLogger(__name__)


async def handle_localai_request(session, model, message, base64_image, ip_address, port, max_tokens):
    data = {"model": model, "messages": [{"role": "user", "content": [{"type": "text", "text": message},
                                                                      {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}], "max_tokens": max_tokens}
    try:
        response = await session.post(
            f"http://{ip_address}:{port}/v1/chat/completions", json=data)
    except Exception as e:
        _LOGGER.error(f"Request failed: {e}")
        raise ServiceValidationError(f"Request failed: {e}")

    if response.status != 200:
        raise ServiceValidationError(
            f"Request failed with status code {response.status}")
    response_text = (await response.json()).get("choices")[0].get(
        "message").get("content")
    return response_text


async def handle_openai_request(session, model, message, base64_image, api_key, max_tokens):
    headers = {'Content-type': 'application/json',
               'Authorization': 'Bearer ' + api_key}
    data = {"model": model, "messages": [{"role": "user", "content": [{"type": "text", "text": message},
                                                                      {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}], "max_tokens": max_tokens}
    try:
        response = await session.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    except Exception as e:
        _LOGGER.error(f"Request failed: {e}")
        raise ServiceValidationError(f"Request failed: {e}")

    if response.status != 200:
        raise ServiceValidationError(
            (await response.json()).get('error').get('message'))
    response_text = (await response.json()).get(
        "choices")[0].get("message").get("content")
    return response_text