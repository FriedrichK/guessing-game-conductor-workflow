from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import (
    AuthenticationSettings,
)

from includes import settings

conductor_configuration = Configuration(
    server_api_url=settings.CONDUCTOR_API_URL,
    # authentication_settings=AuthenticationSettings(
    #    key_id='key',
    #    key_secret='secret'
    # ),
    debug=True,
)
