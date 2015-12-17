import os
import json
from subprocess import check_output
from jsonrpc import 
import requests

from flask import Flask
from flask import request 

from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

from settings import *

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


commands  = ['getbestblockhash',
             'getblockchaininfo',
             'getblockcount',
             'getchaintips',
             'getdifficulty',
             'getmempoolinfo',
             'gettxoutsetinfo',
             'getmininginfo'
            ]

@app.route('/')
@app.route('/info')
@app.route('/help')
def home():
    '''Document the API so that other services could consume automatically.'''
    home_obj = [{"name": "basic template",
                 "service_version": "1",
                 "api_version": "1",
                 "description": "Describe your service in a couple of sentences or less.",
                 "endpoints" : [
                                {"route": "/example",
                                 "args": [{"name": "first_arg",
                                           "description": "Describe the first argument to this endpoint."},
                                           ],  
                                 "per-req": PRICE,
                                 "description": "Briefly describe this endpoint.",
                                 "returns": [{"name": "first_return",
                                              "description": "Describe the first piece of data your service returns."},
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

@app.route('/core/<cmd>')
#@payment.required(PRICE)
def call_core(cmd):
    # do stuff
    res = {}
    if cmd in commands:
        print("Ran %s" % (cmd,))
        #out = check_output(['bitcoin-cli', cmd], universal_newlines=False)

        url = "http://%s:%s/" % (SERVER,RPCPORT)
        headers = {'content-type': 'application/json'}

        # Example echo method
        payload = {
            "method": cmd,
            #"params": ["echome!"],
            "jsonrpc": "2.0",
            "id": 0,
        }
        res = requests.post(
            url, data=json.dumps(payload), headers=headers).json()

        print(res)
        #assert response["result"] == "echome!"
        #assert response["jsonrpc"]
        #assert response["id"] == 0

        try:
            res = json.loads(out)
        except:
            res = {"output": out}
        res['result'] = 'success'
    else:
        res = {'result': 'error',
                'message': 'Invalid command. In other words, nope.'}

    body = json.dumps(res)

    return (body, 200, {'Content-length': len(body),
                        'Content-type': 'application/json',
                       }
           )

if __name__ == '__main__':
    if DEBUG:
        app.debug = True
    app.run(host='0.0.0.0', port=PORT)
