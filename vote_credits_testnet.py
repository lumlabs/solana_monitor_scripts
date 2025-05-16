import subprocess
import sys
import requests
import json

RPC_URL = "https://api.testnet.solana.com"
CLI = "/root/.local/share/solana/install/active_release/bin/solana"


def get_validators(cli, url):
    try:
        cmd = subprocess.run([cli, 'validators', '--url', url, '--output', 'json-compact'],
                             capture_output=True)
        out = cmd.stdout
    except FileNotFoundError as e:
        sys.exit(str(e))
    else:
        return out


def data_to_json(raw_data):
    try:
        obj = json.loads(raw_data)
    except json.JSONDecodeError as e:
        sys.exit(str(e))
    else:
        return obj


def get_validators_from_json(json_object):
    try:
        validators = json_object["validators"]
    except KeyError as e:
        sys.exit(str(e))
    else:
        return validators


if __name__ == '__main__':
    grace = 3.00
    epoch_credits = 0
    v = get_validators(CLI, RPC_URL)
    vobj = data_to_json(v)
    cluster_validator_list = get_validators_from_json(vobj)
    validators_count = len(cluster_validator_list)
    val_cnt = 0
    if validators_count > 0:
        for validator in cluster_validator_list:
            val_ep_creds = int(validator['epochCredits'])
            if val_ep_creds > 0:
                epoch_credits += val_ep_creds
                val_cnt += 1
            # epoch_credits += int(validator['epochCredits'])
    min_epoch_credits = int(round((epoch_credits/val_cnt)*(1 - grace/100)))
    print(min_epoch_credits)
