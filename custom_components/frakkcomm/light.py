"""Platform for light FrakkComm éjjelifény integration."""
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from homeassistant.components.light import (
    LightEntity,
    ATTR_BRIGHTNESS,
    ATTR_WHITE_VALUE,
    ATTR_COLOR_NAME,
    ATTR_RGB_COLOR,
    ATTR_HS_COLOR,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR
)

from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_PORT,
    CONF_NAME
)

from .const import (
    DOMAIN,
    CONF_LAMPA_ID
)

_LOGGER = logging.getLogger(__name__)

# CONF_MIN_BRIGHTNESS = 'min_brightness'
# CONF_MAX_BRIGHTNESS = 'max_brightness'

# Validation of the user's configuration
# More info: https://developers.home-assistant.io/docs/en/development_validation.html
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=1001): cv.port,
    vol.Required(CONF_LAMPA_ID): int,
    vol.Required(CONF_NAME): cv.string,

    # vol.Optional(CONF_MIN_BRIGHTNESS, default=0): int,
    # vol.Optional(CONF_MAX_BRIGHTNESS, default=255): int,

    # not needed for now
    # vol.Optional(CONF_USERNAME, default='admin'): cv.string,
    # vol.Optional(CONF_PASSWORD, default='admin'): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Ejjelifeny platform."""
    import frakkcomm

    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    lampa_id = config[CONF_LAMPA_ID]
    name = config[CONF_NAME]

    # min_brightness = config[CONF_MIN_BRIGHTNESS]
    # max_brightness = config[CONF_MAX_BRIGHTNESS]

    # username = config[CONF_USERNAME]
    # password = config.get(CONF_PASSWORD)

    # Setup connection with device
    feny_eszkoz = frakkcomm.Ejjelifeny(host, port, lampa_id, name, 0,
        255)


    # Add devices
    # create an object using the class below,
    # and pass the custom object from above
    add_entities([Ejjelifeny(feny_eszkoz)])


class Ejjelifeny(LightEntity):
    """Representation of an Ejjelifeny."""

    def __init__(self, light):
        """Initialize an Ejjelifeny."""
        self._light = light
        self._eszkoz_id = light.eszkoz_id
        self._name = light.name
        self._state = None
        self._brightness = 255
        self._hs_color = [0, 0]
        self._white_value = 255

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def eszkoz_id(self):
        return self._eszkoz_id

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def hs_color(self):
        """Return the hue and saturation color value [float, float]."""
        return self._hs_color

    # @property
    # def state(self):
    #     return self._state

    @property
    def white_value(self):
        """Return the white value of this light between 0..255."""
        return self._white_value

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def supported_features(self):
        """Flag supported features.
        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        More info: https://developers.home-assistant.io/docs/en/entity_light.html#support-feature
        Combine multiple supported features with bitwise "OR" operation
        """
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR


    def turn_on(self, **kwargs):
        import time
        import random

        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """

        # Random várjon 0-2mp között valamennyit.
        # Azért kell hogy egyszerre több lámpát fel lehessen kapcsolni
        time.sleep(random.randint(0, 200) / 100)

        ledConfig = {
            "white": False,
            "blue": False
        }

        desired_brightness = kwargs.get(ATTR_BRIGHTNESS, self.brightness)
        desired_color = kwargs.get(ATTR_HS_COLOR, self.hs_color)
        # desired_color = kwargs.get(ATTR_COLOR_NAME, "white")    # régi

        isBlue = desired_color[0] >= 200 and desired_color[0] <= 260 and desired_color[1] >= 0
        isWhite = desired_color[1] < 100

        if isBlue == True:
            ledConfig["blue"] = True
        if isWhite == True:
            ledConfig["white"] = True


        # ledConfig[desired_color] = (
        #                desired_color == "white" or
        #                desired_color == "blue"
        # )

        # Need for the UI to work
        self._brightness = desired_brightness
        self._state = True
        self._hs_color = desired_color

        self._light.controlLight(ledConfig, desired_brightness)


    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.turnOffLight()

        # Need for the UI to work
        # self._brightness = 0
        self._state = False

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        status = self._light.getStatus()
        # TODO: implement light status (v2-es kommunikació szükséges?)
