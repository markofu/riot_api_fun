# Riot API Fun Tool

## Description

This tool runs and pulls down metadata from the Riot API regarding Riot InfoSec folk before posting that information in friendly format to Slack.

## SetUp && Requirements

- **Python 2.7**
- **Non-Standard Modules**
  - Slackclient
  - Docopt
- **Required Accounts**
  - League of Legends
  - Slack Accounts 
- **Auth Requirements**
  - Riot API Key (via https://developer.riotgames.com/docs/api-keys)
  - Slack Web Token via (https://api.slack.com/web) and click on "Generate Test Tokens".
- **Usage**
  - Documented in the tool as per ```python level_check.py -h```

## ToDo

- Move to Lambda with KMS Integration
- Add RDS functionality for storage
- Add interesting stats to report on once people get to L30
- Keep it fun, it's not about tracking, okie dokie!

