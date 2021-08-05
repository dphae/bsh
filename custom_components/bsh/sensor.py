from homeassistant.const import (
    STATE_OFF,
    STATE_ON,
    TEMP_CELSIUS,
    POWER_WATT,
    ENERGY_KILO_WATT_HOUR,
    ELECTRIC_POTENTIAL_VOLT,
    TIME_SECONDS,
    VOLUME_CUBIC_METERS
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import BinarySensorEntity
import logging
from .const import DOMAIN

ENERGY_GCAL = 'Gcal'
MONEY_UAH = 'UAH'

sensors = [
    {
        'key': 'last 24h power',
        'unit': POWER_WATT,
        'icon': 'mdi:flash-circle'
    },
    {
        'key': 'last hour power',
        'unit': POWER_WATT,
        'icon': 'mdi:flash-circle'
    },
    {
        'key': 'last tick power',
        'unit': POWER_WATT,
        'icon': 'mdi:flash-circle'
    },
    {
        'key': 'this day power',
        'unit': POWER_WATT,
        'icon': 'mdi:flash-circle'
    },
    {
        'key': 'this month power',
        'unit': POWER_WATT,
        'icon': 'mdi:flash-circle'
    },
    
    {
        'key': 'current heat energy',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },
    {
        'key': 'last 24h heat energy',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },
    {
        'key': 'last 24h heat energy cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last hour heat energy',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },
    {
        'key': 'last hour heat energy cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last tick heat energy',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },
    {
        'key': 'this day heat energy',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },
    {
        'key': 'this month heat energy',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },
    {
        'key': 'this month heat energy cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month heat energy cost estimate',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month heat energy estimate',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },
    {
        'key': 'this month start heat energy',
        'unit': ENERGY_GCAL,
        'icon': 'mdi:radiator'
    },

    {
        'key': 'current energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },
    {
        'key': 'last 24h energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },
    {
        'key': 'last 24h energy cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last hour energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },
    {
        'key': 'last hour energy cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last tick energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },
    {
        'key': 'this day energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },
    {
        'key': 'this month energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },
    {
        'key': 'this month energy cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month energy cost estimate',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month energy estimate',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },
    {
        'key': 'this month start energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'icon': 'mdi:power-plug'
    },

    {
        'key': 'current temperature',
        'unit': TEMP_CELSIUS
    },
    {
        'key': 'target day temperature',
        'unit': TEMP_CELSIUS
    },
    {
        'key': 'target night temperature',
        'unit': TEMP_CELSIUS
    },

    {
        'key': 'last 24h total cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last hour total cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month total cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month total cost estimate',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },

    {
        'key': 'last update duration',
        'unit': TIME_SECONDS,
        'icon': 'mdi:timer'
    },

    {
        'key': 'current voltage',
        'unit': ELECTRIC_POTENTIAL_VOLT,
        'icon': 'mdi:flash'
    },
    {
        'key': 'this day max voltage',
        'unit': ELECTRIC_POTENTIAL_VOLT,
        'icon': 'mdi:flash'
    },
    {
        'key': 'this day min voltage',
        'unit': ELECTRIC_POTENTIAL_VOLT,
        'icon': 'mdi:flash'
    },

    {
        'key': 'current cold water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'last 24h cold water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'last 24h cold water cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last hour cold water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'last hour cold water cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last tick cold water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'this day cold water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'this month cold water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'this month cold water cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month cold water cost estimate',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month cold water estimate',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'this month start cold water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },


    {
        'key': 'current hot water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'last 24h hot water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'last 24h hot water cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last hour hot water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'last hour hot water cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'last tick hot water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'this day hot water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },

    {
        'key': 'this month hot water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'this month hot water cost',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month hot water cost estimate',
        'unit': MONEY_UAH,
        'icon': 'mdi:currency-usd'
    },
    {
        'key': 'this month hot water estimate',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    },
    {
        'key': 'this month start hot water',
        'unit': VOLUME_CUBIC_METERS,
        'icon': 'mdi:water'
    }
]

binary_sensors = [
    {
        'key': 'heat energy valve',
        'icon_on': 'mdi:toggle-switch',
        'icon_off': 'mdi:toggle-switch-off',
        'class': 'heat'
    }
]

logger = logging.getLogger(__name__)


class Sensor(Entity):
    def __init__(self, data, config):
        config['name'] = 'BSH ' + config['key']
        self._data = data
        self._config = config

    @property
    def name(self):
        return self._config['name']

    @property
    def state(self):
        return self._data[self._config['key']]

    @property
    def unit_of_measurement(self):
        return self._config['unit']

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return self._config.get('icon')


class BinarySensor(BinarySensorEntity):
    def __init__(self, data, config):
        config['name'] = 'BSH ' + config['key']
        self._data = data
        self._config = config

    @property
    def name(self):
        return self._config['name']

    @property
    def is_on(self):
        return bool(self._data[self._config['key']])

    @property
    def device_class(self):
        return None

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return self._config.get('icon_on') if self.is_on else self._config.get('icon_off')

    @property
    def device_class(self):
        return self._config.get('class')


def setup_platform(hass, config, add_entities, discovery_info=None):
    entities_values = hass.data[DOMAIN]['entities_values']
    entities = hass.data[DOMAIN]['entities']

    for sensor in sensors:
        entities[sensor['key']] = Sensor(entities_values, sensor)

    for sensor in binary_sensors:
        entities[sensor['key']] = BinarySensor(entities_values, sensor)

    add_entities(entities.values())
