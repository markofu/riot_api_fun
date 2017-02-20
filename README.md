# Riot API Fun Tool

## Description

This tool runs and pulls down metadata from the Riot API regarding Riot InfoSec folk before posting that information in friendly format to Slack.

## SetUp && Requirements

- *Python 2.7*
- *Non-Standard Modules* :: Slackclient & Docopt
- *Accounts* :: League of Legends and Slack Accounts are required
- *Auth Requirements* :: Riot API Key (via https://developer.riotgames.com/docs/api-keys) and Slack Web Token via (https://api.slack.com/web) and click on "Generate Test Tokens".
- *Usage :: Documented in the tool* ```python level_check.py```

## ToDo

- Move to Lambda with KMS Integration
- Add RDS functionality for storage
- Add interesting stats to report on once people get to L30
- Keep it fun, it's not about tracking, okie dokie!

