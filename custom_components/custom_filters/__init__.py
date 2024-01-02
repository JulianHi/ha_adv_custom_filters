import json
from typing import Any, cast

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
# noinspection PyProtectedMember
from homeassistant.helpers.template import TemplateEnvironment, _NO_HASS_ENV
from homeassistant.helpers.typing import ConfigType

DOMAIN = 'custom_filters'


def to_my_ascii_json(string):
    return json.dumps(string, ensure_ascii=False)

def finder_t5(string):
    """Convert sring to Finder T5 Value"""

    # Convert decimal string to an integer
    decimal_value = int(string)

    # Extract the 8-bit exponent value and the 24-bit measurement
    exponent_value = 255 - 1 - ((decimal_value >> 24) & 0xFF)
    measurement_value = decimal_value & 0xFFFFFF

    return measurement_value *10**exponent_value


async def async_setup(hass: HomeAssistant, yaml_config: ConfigType):
    _NO_HASS_ENV.filters['to_my_ascii_json'] = to_my_ascii_json
    _NO_HASS_ENV.filters['finder_t5'] = finder_t5
    _NO_HASS_ENV.globals['finder_t5'] = finder_t5

    if DOMAIN in yaml_config and not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(hass.config_entries.flow.async_init(
            DOMAIN, context={'source': SOURCE_IMPORT}
        ))

    return True


async def async_setup_entry(hass: HomeAssistant, _: ConfigEntry):
    for env in hass.data.values():
        if isinstance(env, TemplateEnvironment):
            env.filters['to_my_ascii_json'] = to_my_ascii_json
            env.filters['finder_t5'] = finder_t5
            env.globals['finder_t5'] = finder_t5

    CustomTemplateEnvironment.base_init = cast(Any, TemplateEnvironment.__init__)
    TemplateEnvironment.__init__ = CustomTemplateEnvironment.init

    return True


async def async_unload_entry(*_):
    TemplateEnvironment.__init__ = CustomTemplateEnvironment.base_init
    return True


class CustomTemplateEnvironment:
    base_init = None

    @staticmethod
    def init(*args, **kwargs):
        CustomTemplateEnvironment.base_init(*args, **kwargs)
        env = args[0]
        env.filters['to_my_ascii_json'] = to_my_ascii_json
        env.filters['finder_t5'] = finder_t5
        env.globals['finder_t5'] = finder_t5
