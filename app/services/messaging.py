from typing import Optional, Dict, Any

from app.core.logger import _logger as logger
from app.core.config import settings
from thirdparty.whatsapp.whatsapp import WhatsappClient


class MessagingService:
    """
    Messaging service.
    """

    def __init__(self):
        self.client = WhatsappClient(access_token=settings.WHATSAPP_ACCESS_TOKEN, phone_number_id=settings.WHATSAPP_PHONE_NUMBER_ID)



    def send_template_message(self,
                              to_phone_number: str,
                              template_name: str,
                              language_code: str = "en_US",
                              template_components: Optional[Any] = None):
        """
        Send a template message to a WhatsApp number

        Args:
            to_phone_number (str): Recipient's phone number with country code
            template_name (str): Name of the template to use
            language_code (str): Language code for the template
            template_components (Dict, optional): Additional template components

        Returns:
            Dict: API response
        """
        try:
            logger.info(f"Sending template message to {to_phone_number}")

            if to_phone_number.startswith('+'):
                to_phone_number = to_phone_number[1:]

            payload ={
                    "messaging_product": "whatsapp",
                    "to": f"{to_phone_number}",
                    "type": "template",
                    "template": {
                        "name": template_name,
                        "language": {
                            "code": language_code
                        }
                    }
                }

            if template_components:
                payload["template"].update(template_components)

            resp = self.client.send_raw_message(payload=payload)

            if resp.get("error"):
                logger.error(f"Failed to send template message: {resp}")
                raise Exception(f"Failed to send template message: {resp}")
            return resp

        except Exception as e:
            logger.error(f"Failed to send template message: {str(e)}")
            raise Exception(f"Failed to send template message: {str(e)}")








