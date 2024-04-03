# Synthetix Funding Rate Arbitrage
![Funding Rate Arbitrage Bot Template](https://github.com/50shadesofgwei/SynthetixFundingRateArbitrage/assets/111451828/eb931108-bdbb-4741-b2bc-def2de8e3370)

![Static Badge](https://img.shields.io/badge/Telegram-blue?link=https%3A%2F%2Ft.me%2F%2BualID7ueKuJjMWJk) ![Static Badge](https://img.shields.io/badge/License-MIT-green)

Backend for a historical funding rate watcher. Opportunities for arbitrage are queried periodically using the same engine found in [the main repository](https://github.com/50shadesofgwei/SynthetixFundingRateArbitrage), but with all tx execution logic taken out. Opportunity data is logged to an SQLite3 database to be accessed via a Flask server to build an interactive frontend.

## Console Scripts
The bot can be controlled via the CLI using the following commands:
- `project-run2` (Starts the bot)

