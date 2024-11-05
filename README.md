# PazGas Power

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Integration to integrate with [PazGas Power][pazgas_power]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | `True` or `False` entities.
`sensor` | Show info from PazGas Power API.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `pazgas_power`.
1. Download _all_ the files from the `custom_components/pazgas_power/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "PazGas Power"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[pazgas_power]: https://www.pazgas.co.il/hashmal/
[buymecoffee]: https://www.buymeacoffee.com/GuyKh
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/GuyKh/pazgas-power-custom-component.svg?style=for-the-badge
[commits]: https://github.com/GuyKh/pazgas-power-custom-component/commits/main
[exampleimg]: example.png
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/GuyKh/pazgas-power-custom-component.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Guy%20Khmelnitsky%20%40GuyKh-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/GuyKh/pazgas-power-custom-component.svg?style=for-the-badge
[releases]: https://github.com/GuyKh/pazgas-power-custom-component/releases
