from flask import Flask
from flask import request 

from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

import os
import json
import requests

from settings import *

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

commands  = {'getbestblockhash': 0,   # requiring no arguments
             'getblockchaininfo': 0,
             'getblockcount': 0,
             'getchaintips': 0,
             'getdifficulty': 0,
             'getmempoolinfo': 0,
             'getmininginfo': 0,
             'getrawmempool': 0,
             'validateaddress': 0,
             'getnetworkhashps': 0,
             'sendrawtransaction': 1, # requiring one argument
             'gettxout': 1,
             'getblock': 1,
             'estimatefee': 1,
             'estimatepriority': 1,
             'decoderawtransaction': 1,
             'decodescript': 1,
             'getrawtransaction': 1,
             'verifymessage': 3,      # three required args
             }

@app.route('/')
@app.route('/info')
@app.route('/help')
def home():
    '''Document the API so that other services could consume automatically.'''
    home_obj = [{"name": "Bitcoin Core API",
                 "service_version": "1",
                 "api_version": "1",
                 "description": "Provides paid access to a subset of Bitcoin Core RPC commands.",
                 "endpoints" : [
                                {"route": "/api/<method>",
                                    "args": None,
                                 "per-req": PRICE,
                                 "description": "Accepts any of the following methods: %s" % ', '.join(commands),
                                 "returns": [{"name": "various",
                                              "description": "JSON output of each method."},
                                            ],
                                },
                                {"route": "/info",
                                 "args": None,
                                 "per-req": 0,
                                 "description": "This listing of endpoints provided by this server. "\
                                    "Available at /info."
                                }],
                }
               ]

    body = json.dumps(home_obj, indent=2)

    return (body, 200, {'Content-length': len(body),
                        'Content-type': 'application/json',
                       }
           )


@app.route('/api/<cmd>')
#@payment.required(PRICE)
def call_core(cmd):
    res = {}
    if cmd in commands:
        res = json_rpc(cmd)
    else:
        res = {'result': 'error',
               'message': 'Invalid command'}
    body = json.dumps(res)
    return (body, 200, {'Content-length': len(body),
                        'Content-type': 'application/json',
                       }
           )


def json_rpc(command):
    url = "http://%s:%s@%s:%s/" % (RPCUSER, RPCPASS, SERVER, RPCPORT)
    headers = {'content-type': 'application/json'}
    payload = {
        "method": cmd,
        "jsonrpc": "2.0",
        "id": 0}
    out = requests.post(url, data=json.dumps(payload), headers=headers).json()

    try:
        res = json.loads(out)
    except:
        res = {"output": out}
    res['result'] = 'success'
    return res


if __name__ == '__main__':
    if DEBUG:
        app.debug = True
    app.run(host='0.0.0.0', port=PORT)
