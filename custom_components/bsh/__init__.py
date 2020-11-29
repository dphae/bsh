import asyncio
import logging
import time
import calendar
import voluptuous as vol
import json
import homeassistant.helpers.config_validation as cv
from aiohttp import ClientSession, ClientResponse, CookieJar
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_time_interval
from datetime import datetime, timedelta
from .const import DOMAIN

SET_TEMPERATURE_SERVICE_SCHEMA = vol.Schema({
    vol.Required('temperature'): cv.template
})

logger = logging.getLogger(__name__)

@asyncio.coroutine
async def async_setup(hass, config):
    conf = config.get(DOMAIN, {})
    cookie_jar = CookieJar()
    entities = {}
    entities_values = {}
    billing = conf['billing']

    hass.data[DOMAIN] = {
        'entities_values': entities_values,
        'entities': entities
    }

    session = ClientSession(cookie_jar=cookie_jar)
    response = await session.post(
        'https://sh.od.ua/auth.php',
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://sh.od.ua/login/'
        },
        data = {
            'componentAction': '',
            'user[login]': '',
            'user[username]': conf['username'],
            'user[password]': conf['password'],
            'user[remember]': ''
        }
    )
    await response.release()
    await session.close()

    @callback
    async def service_update(call):
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        yesterday_ms = round(datetime.timestamp(yesterday) * 1000)
        now_seconds = round(datetime.timestamp(now))
        now_ms = now_seconds * 1000
        hour_start_ms = (datetime.timestamp(now) - 3600) * 1000
        tick_start_ms = (datetime.timestamp(now) - conf['interval']) * 1000
        day_start_ms = datetime.timestamp(datetime(now.year, now.month, now.day)) * 1000
        day_start_hours = round((now_ms - day_start_ms) / 3600 / 1000, 3)
        month_past = (now - datetime(now.year, now.month, 1)).total_seconds()
        month_rest = (datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]) - now).total_seconds() + 86400

        session = ClientSession(cookie_jar=cookie_jar)
        
        ### electricity ###

        response = await session.get('https://sh.od.ua/user/light/indicators/')
        response_json = await response.json(content_type=None)
        await response.release()

        entities_values['current energy'] = float(response_json['current'])
        entities_values['this month start energy'] = None if response_json['last'] == '-----' else float(response_json['last'])
        entities_values['this month energy'] = float(response_json['beforelast'])
        entities_values['this month energy cost'] = round(billing['electricity'] * entities_values['this month energy'], 2)

        response = await session.get('https://sh.od.ua/user/indicators/energy-day/')
        response_json = await response.json(content_type=None)
        await response.release()
        response_values = list(filter(lambda x: x[1], response_json))
        entities_values['last tick energy'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > tick_start_ms, response_values))), 3)
        entities_values['last hour energy'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > hour_start_ms, response_values))), 3)
        entities_values['last 24h energy'] = round(sum(map(lambda x: x[1], response_values)), 3)
        entities_values['this day energy'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > day_start_ms, response_values))), 3)

        entities_values['last hour energy cost'] = round(billing['electricity'] * entities_values['last hour energy'], 2)
        entities_values['last 24h energy cost'] = round(billing['electricity'] * entities_values['last 24h energy'], 2)

        entities_values['this month energy estimate'] = round(entities_values['this month energy'] + entities_values['last 24h energy'] * (month_rest / 3600 / 24), 3)
        entities_values['this month energy cost estimate'] = round(billing['electricity'] * entities_values['this month energy estimate'], 2)

        entities_values['last tick power'] = round(entities_values['last tick energy'] * 1000 * 3600 / conf['interval'])
        entities_values['last hour power'] = round(entities_values['last hour energy'] * 1000)
        entities_values['last 24h power'] = round(entities_values['last 24h energy'] * 1000 / 24)
        entities_values['this day power'] = round(entities_values['this day energy'] * 1000 / day_start_hours)
        entities_values['this month power'] = round(entities_values['this month energy'] * 1000 / (month_past / 3600))

        response = await session.get('https://sh.od.ua/user/indicators/indicators/')
        response_json = await response.json(content_type=None)
        await response.release()
        entities_values['current voltage'] = float(response_json['voltage'])
        
        response = await session.post(
            'https://sh.od.ua/user/light/data-graph-voltage/',
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://sh.od.ua/user/light/'
            },
            data = {
                'start': now.strftime('%Y-%m-%d'),
                'end': now.strftime('%Y-%m-%d')
            }
        )
        response_values = await response.json(content_type=None)
        await response.release()
        entities_values['this day min voltage'] = min(map(lambda x: x[1], response_values))
        entities_values['this day max voltage'] = max(map(lambda x: x[1], response_values))

        ### heating ###

        response = await session.get('https://sh.od.ua/user/heating/indicators/')
        response_json = await response.json(content_type=None)
        await response.release()
        entities_values['current heat energy'] = float(response_json['current'])
        entities_values['this month start heat energy'] = float(response_json['last'])
        entities_values['this month heat energy'] = float(response_json['beforelast'])
        entities_values['this month heat energy cost'] = round(billing['heating'] * entities_values['this month heat energy'], 2)

        #response = await session.get('https://sh.od.ua/user/indicators/heating-day/')
        response = await session.post(
            'https://sh.od.ua/user/heating/data-graph/',
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://sh.od.ua/user/heating/'
            },
            data = {
                'start': yesterday.strftime('%Y-%m-%d'),
                'end': now.strftime('%Y-%m-%d')
            }
        )
        response_json = await response.json(content_type=None)
        await response.release()
        response_values = list(filter(lambda x: x[1] and x[0] > yesterday_ms, response_json))
        entities_values['last tick heat energy'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > tick_start_ms, response_values))), 3)
        entities_values['last hour heat energy'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > hour_start_ms, response_values))), 3)
        entities_values['last 24h heat energy'] = round(sum(map(lambda x: x[1], response_values)), 3)
        entities_values['this day heat energy'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > day_start_ms, response_values))), 3)
        
        entities_values['last hour heat energy cost'] = round(billing['heating'] * entities_values['last hour heat energy'], 2)
        entities_values['last 24h heat energy cost'] = round(billing['heating'] * entities_values['last 24h heat energy'], 2)

        entities_values['this month heat energy estimate'] = round(entities_values['this month heat energy'] + entities_values['last 24h heat energy'] * (month_rest / 3600 / 24), 3)
        entities_values['this month heat energy cost estimate'] = round(billing['heating'] * entities_values['this month heat energy estimate'], 2)

        response = await session.get('https://sh.od.ua/user/tempcontrol/get-valve/')
        response_json = await response.json(content_type=None)
        await response.release()
        entities_values['heat energy valve'] = bool(response_json)

        response = await session.get('https://sh.od.ua/user/tempcontrol/sensors/')
        response_json = await response.json(content_type=None)
        await response.release()
        entities_values['current temperature'] = float(response_json['temp1'])

        response = await session.get('https://sh.od.ua/user/tempcontrol/get-temp/')
        response_json = await response.json(content_type=None)
        await response.release()
        entities_values['target day temperature'] = response_json

        response = await session.get('https://sh.od.ua/user/tempcontrol/get-temp-nm/')
        response_json = await response.json(content_type=None)
        await response.release()
        entities_values['target night temperature'] = response_json

        ### water ###

        response = await session.get('https://sh.od.ua/user/water/indicators/')
        response_json = await response.json(content_type=None)
        await response.release()
        entities_values['current hot water'] = float(response_json['hot_current'])
        entities_values['this month start hot water'] = float(response_json['hot_last'])
        entities_values['this month hot water'] = float(response_json['hot_beforelast'])
        entities_values['this month hot water cost'] = round(billing['hot_water'] * entities_values['this month hot water'], 2)

        entities_values['current cold water'] = float(response_json['cold_current'])
        entities_values['this month start cold water'] = float(response_json['cold_last'])
        entities_values['this month cold water'] = float(response_json['cold_beforelast'])
        entities_values['this month cold water cost'] = round(billing['cold_water'] * entities_values['this month cold water'], 2)

        response = await session.get('https://sh.od.ua/user/indicators/hot-water-day/')
        response_json = await response.json(content_type=None)
        await response.release()
        response_values = list(filter(lambda x: x[1], response_json))
        entities_values['last tick hot water'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > tick_start_ms, response_values))), 3)
        entities_values['last hour hot water'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > hour_start_ms, response_values))), 3)
        entities_values['last 24h hot water'] = round(sum(map(lambda x: x[1], response_values)), 3)
        entities_values['this day hot water'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > day_start_ms, response_values))), 3)
        
        entities_values['last hour hot water cost'] = round(billing['hot_water'] * entities_values['last hour hot water'], 2)
        entities_values['last 24h hot water cost'] = round(billing['hot_water'] * entities_values['last 24h hot water'], 2)

        entities_values['this month hot water estimate'] = round(entities_values['this month hot water'] + entities_values['last 24h hot water'] * (month_rest / 3600 / 24), 3)
        entities_values['this month hot water cost estimate'] = round(billing['hot_water'] * entities_values['this month hot water estimate'], 2)


        response = await session.get('https://sh.od.ua/user/indicators/cold-water-day/')
        response_json = await response.json(content_type=None)
        await response.release()
        response_values = list(filter(lambda x: x[1], response_json))
        entities_values['last tick cold water'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > tick_start_ms, response_values))), 3)
        entities_values['last hour cold water'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > hour_start_ms, response_values))), 3)
        entities_values['last 24h cold water'] = round(sum(map(lambda x: x[1], response_values)), 3)
        entities_values['this day cold water'] = round(sum(map(lambda x: x[1], filter(lambda x: x[0] > day_start_ms, response_values))), 3)
        
        entities_values['last hour cold water cost'] = round(billing['cold_water'] * entities_values['last hour cold water'], 2)
        entities_values['last 24h cold water cost'] = round(billing['cold_water'] * entities_values['last 24h cold water'], 2)

        entities_values['this month cold water estimate'] = round(entities_values['this month cold water'] + entities_values['last 24h cold water'] * (month_rest / 3600 / 24), 3)
        entities_values['this month cold water cost estimate'] = round(billing['cold_water'] * entities_values['this month cold water estimate'], 2)

        await session.close()

        ### billing ###
        
        entities_values['last hour total cost'] = round(
            entities_values['last hour energy cost'] +
            entities_values['last hour heat energy cost'] +
            entities_values['last hour hot water cost'] +
            entities_values['last hour cold water cost']
        , 2)
        entities_values['last 24h total cost'] = round(
            entities_values['last 24h energy cost'] +
            entities_values['last 24h heat energy cost'] +
            entities_values['last 24h hot water cost'] +
            entities_values['last 24h cold water cost']
        , 2)
        entities_values['this month total cost'] = round(
            entities_values['this month energy cost'] +
            entities_values['this month heat energy cost'] +
            entities_values['this month hot water cost'] +
            entities_values['this month cold water cost']
        , 2)
        entities_values['this month total cost estimate'] = round(
            entities_values['this month energy cost estimate'] + 
            entities_values['this month heat energy cost estimate'] + 
            entities_values['this month hot water cost estimate'] +
            entities_values['this month cold water cost estimate']
        , 2)

        # force update everything
        for entity in entities.values():
            entity.schedule_update_ha_state()

        entities_values['last update duration'] = round(time.time() - now_seconds, 3)

        #logger.debug(dict(sorted(entities_values.items())))
        logger.debug(json.dumps(entities_values, indent=4, sort_keys=True))

    @callback
    async def service_set_day_temperature(call):
        temperature = call.data['temperature']
        temperature.hass = hass

        session = ClientSession(cookie_jar=cookie_jar)
        response = await session.post(
            'https://sh.od.ua/user/tempcontrol/set-temp/',
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://sh.od.ua/user/tempcontrol/'
            },
            data = {
                'temp': temperature.async_render(parse_result=False)
            }
        )
        await response.release()

        response = await session.get('https://sh.od.ua/user/tempcontrol/get-temp/')
        entities_values['target day temperature'] = await response.json(content_type=None)
        entities['target day temperature'].schedule_update_ha_state()
        await response.release()

        await session.close()

    @callback
    async def service_set_night_temperature(call):
        temperature = call.data['temperature']
        temperature.hass = hass

        session = ClientSession(cookie_jar=cookie_jar)
        response = await session.post(
            'https://sh.od.ua/user/tempcontrol/set-temp-nm/',
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://sh.od.ua/user/tempcontrol/'
            },
            data = {
                'temp': temperature.async_render(parse_result=False)
            }
        )
        await response.release()

        response = await session.get('https://sh.od.ua/user/tempcontrol/get-temp-nm/')
        entities_values['target night temperature'] = await response.json(content_type=None)
        entities['target night temperature'].schedule_update_ha_state()
        await response.release()

        await session.close()

    hass.services.async_register(DOMAIN, 'update', service_update)
    hass.services.async_register(
        DOMAIN,
        'set_day_temperature',
        service_set_day_temperature,
        schema = SET_TEMPERATURE_SERVICE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN,
        'set_night_temperature',
        service_set_night_temperature,
        schema = SET_TEMPERATURE_SERVICE_SCHEMA
    )

    if ( response.cookies.get('NRGNSID') ):
        logger.info('auth is successfull')

        await service_update(None)

        update_interval = timedelta(seconds=conf['interval'])
        async_track_time_interval(hass, service_update, update_interval)

        for component in ['sensor']:
            await hass.helpers.discovery.async_load_platform(component, DOMAIN, {}, config)

        return True
    else:
        logger.error('auth has failed!')
        return False


# hub.update() is a sync function.
#result = await hass.async_add_executor_job(hub.update)

# track_time_interval(hass, refresh, SCAN_INTERVAL)

# https://aarongodfrey.dev/programming/restoring-an-entity-in-home-assistant/
