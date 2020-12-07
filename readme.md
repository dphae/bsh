Budova Smart Home
=================

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

Home Assistant integration for https://sh.od.ua/.
It provides a lot of sensors for electricity, hot/cold water and heating monitoring. Allows to set target day and night temperature.
Some sensors:

<p align="center">
  <img src="https://raw.githubusercontent.com/dphae/bsh/main/images/screenshots/hot-water.png">
</p>


## Installation

### Manual

Copy `bsh` directory to your Home Assistant `config/custom_components` directory.

### HACS

In [HACS](https://hacs.xyz/) settings add a custom repository https://github.com/dphae/bsh with `Integration` category.
Then the `bsh` custom component will be installable through HACS and you will be able to follow the future updates.


## Configuration

Add the following to your `configuration.yaml`:

```yaml
bsh:
    username: username@budova.com
    password: YOURPASSWORD
    interval: 300
    billing:
        electricity: 1.68
        cold_water: 26.724
        hot_water: 96.004
        heating: 1185.00

input_number:
    bsh_day_temperature:
        name: BSH day temperature
        min: 12
        max: 24
        step: 1
        unit_of_measurement: °C
        icon: mdi:thermometer
    bsh_night_temperature:
        name: BSH night temperature
        min: 12
        max: 24
        step: 1
        unit_of_measurement: °C
        icon: mdi:thermometer
```

Add the following to your `automations.yaml`:

```yaml
- id: '1604273337828'
  alias: set day temperature
  trigger:
    - platform: state
      entity_id: sensor.bsh_target_day_temperature
  action:
    - service: input_number.set_value
      data:
          entity_id: input_number.bsh_day_temperature
          value: "{{ states('sensor.bsh_target_day_temperature') | int }}"

- id: '1604273722071'
  alias: day temperature slider moved
  trigger:
    - platform: state
      entity_id: input_number.bsh_day_temperature
  action:
    - service: bsh.set_day_temperature
      data:
          temperature: "{{ states('input_number.bsh_day_temperature') | int }}"

- id: '1604273337829'
  alias: set night temperature
  trigger:
    - platform: state
      entity_id: sensor.bsh_target_night_temperature
  action:
    - service: input_number.set_value
      data:
          entity_id: input_number.bsh_night_temperature
          value: "{{ states('sensor.bsh_target_night_temperature') | int }}"

- id: '1604273722072'
  alias: night temperature slider moved
  trigger:
    - platform: state
      entity_id: input_number.bsh_night_temperature
  action:
    - service: bsh.set_night_temperature
      data:
          temperature: "{{ states('input_number.bsh_night_temperature') | int }}"
```


Add the following to your `ui-lovelace.yaml`:

```yaml
title: Omega
views:
  - path: default_view
    title: Home
    cards:
      - type: vertical-stack
        cards:
          - title: General
            type: entities
            entities:
              - sensor.bsh_last_hour_total_cost
              - sensor.bsh_last_24h_total_cost
              - sensor.bsh_this_month_total_cost
              - sensor.bsh_this_month_total_cost_estimate
              - type: divider
              - entity: sensor.bsh_last_update_duration
                secondary_info: last-changed
          - type: history-graph
            hours_to_show: 3
            entities:
              - sensor.bsh_last_24h_total_cost
              - sensor.bsh_last_hour_total_cost
          - title: Temperature
            type: entities
            entities:
              - input_number.bsh_day_temperature
              - input_number.bsh_night_temperature
              - type: divider
              - sensor.bsh_current_temperature
              - sensor.bsh_target_day_temperature
              - sensor.bsh_target_night_temperature
          - type: history-graph
            hours_to_show: 3
            entities:
              - sensor.bsh_current_temperature

      - type: vertical-stack
        cards:
          - title: Electricity
            type: entities
            entities:
              - sensor.bsh_current_voltage
              - sensor.bsh_this_day_min_voltage
              - sensor.bsh_this_day_max_voltage
              - type: divider
              - sensor.bsh_last_tick_power
              - sensor.bsh_last_hour_power
              - sensor.bsh_this_day_power
              - sensor.bsh_last_24h_power
              - sensor.bsh_this_month_power
              - type: divider
              - sensor.bsh_last_tick_energy
              - sensor.bsh_last_hour_energy
              - sensor.bsh_this_day_energy
              - sensor.bsh_last_24h_energy
              - sensor.bsh_this_month_energy
              - sensor.bsh_this_month_energy_estimate
              - sensor.bsh_this_month_start_energy
              - sensor.bsh_current_energy
              - type: divider
              - sensor.bsh_last_hour_energy_cost
              - sensor.bsh_last_24h_energy_cost
              - sensor.bsh_this_month_energy_cost
              - sensor.bsh_this_month_energy_cost_estimate
          - type: history-graph
            hours_to_show: 3
            entities:
              - sensor.bsh_current_voltage
              - sensor.bsh_this_day_min_voltage
              - sensor.bsh_this_day_max_voltage
              - sensor.bsh_last_tick_power
              - sensor.bsh_last_hour_power
              - sensor.bsh_last_24h_power
    
      - type: vertical-stack
        cards:
          - title: Hot water
            type: entities
            entities:
              - sensor.bsh_last_tick_hot_water
              - sensor.bsh_last_hour_hot_water
              - sensor.bsh_this_day_hot_water
              - sensor.bsh_last_24h_hot_water
              - sensor.bsh_this_month_hot_water
              - sensor.bsh_this_month_hot_water_estimate
              - sensor.bsh_this_month_start_hot_water
              - sensor.bsh_current_hot_water
              - type: divider
              - sensor.bsh_last_hour_hot_water_cost
              - sensor.bsh_last_24h_hot_water_cost
              - sensor.bsh_this_month_hot_water_cost
              - sensor.bsh_this_month_hot_water_cost_estimate
          - type: history-graph
            hours_to_show: 3
            entities:
              - sensor.bsh_last_24h_hot_water

      - type: vertical-stack
        cards:
          - title: Cold water
            type: entities
            entities:
              - sensor.bsh_last_tick_cold_water
              - sensor.bsh_last_hour_cold_water
              - sensor.bsh_this_day_cold_water
              - sensor.bsh_last_24h_cold_water
              - sensor.bsh_this_month_cold_water
              - sensor.bsh_this_month_cold_water_estimate
              - sensor.bsh_this_month_start_cold_water
              - sensor.bsh_current_cold_water
              - type: divider
              - sensor.bsh_last_hour_cold_water_cost
              - sensor.bsh_last_24h_cold_water_cost
              - sensor.bsh_this_month_cold_water_cost
              - sensor.bsh_this_month_cold_water_cost_estimate
          - type: history-graph
            hours_to_show: 3
            entities:
              - sensor.bsh_last_24h_cold_water

      - type: vertical-stack
        cards:
          - title: Heating
            type: entities
            state_color: true
            entities:
              - sensor.bsh_heat_energy_valve
              - type: divider
              - sensor.bsh_last_tick_heat_energy
              - sensor.bsh_last_hour_heat_energy
              - sensor.bsh_this_day_heat_energy
              - sensor.bsh_last_24h_heat_energy
              - sensor.bsh_this_month_heat_energy
              - sensor.bsh_this_month_heat_energy_estimate
              - sensor.bsh_this_month_start_heat_energy
              - sensor.bsh_current_heat_energy
              - type: divider
              - sensor.bsh_last_hour_heat_energy_cost
              - sensor.bsh_last_24h_heat_energy_cost
              - sensor.bsh_this_month_heat_energy_cost
              - sensor.bsh_this_month_heat_energy_cost_estimate
          - type: history-graph
            hours_to_show: 3
            entities:
              - sensor.bsh_last_24h_heat_energy
```

