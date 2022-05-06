# LedFxHassio
Home Assistant (hass.io) custom component for LedFx

[![Validate with hassfest](https://github.com/AlgorithmicEntropy/LedFxHassio/actions/workflows/hassfest.yml/badge.svg)](https://github.com/AlgorithmicEntropy/LedFxHassio/actions/workflows/hassfest.yml)

#### Description
Alows basic control of ledFx via homeassistant.

#### Installation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

The easiest way to install it is through [HACS (Home Assistant Community Store)](https://hacs.xyz/), add this repository as a custom one in the HACS settings and download the integration.

If you want to install it manually,  
Download the custom_components/ledfx_remote folder and place into your $homeassistant_config_dir/custom_components directory.

Once downloaded restart your Home Assistant installation.
After the restart you should be able to add it from the integrations screen.

#### Configuration

The integration provides a config flow, in which you need to enter the IP address (host) and port of your LedFx installation.
No further changes are required.
