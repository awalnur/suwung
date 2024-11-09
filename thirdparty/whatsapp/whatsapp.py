from typing import Dict

import requests


class WhatsappClient:
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id

        self.base_url = f"https://graph.facebook.com/v20.0/450374314817408/messages"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def send_raw_message(self, payload: Dict):
        """
        Send raw message to WhatsApp API

        Args:
            payload (Dict): Raw API payload

        Returns:
            Dict: API response
        """

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()