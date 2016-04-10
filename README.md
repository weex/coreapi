## Bitcoin Core API Endpoint

This service provides access to a number of the functions provided by a full node running Bitcoin Core 0.11.2.

Example of getting the current network difficulty:

    21 buy —maxprice 99 url http://10.244.34.100:8332/api/getdifficulty

Here's a list of available commands that you can run through this tool. Each one costs 99 sat to run.

### requiring no arguments
            getbestblockhash   
            getblockchaininfo
            getblockcount
            getchaintips
            getdifficulty
            getmempoolinfo
            getmininginfo
            getrawmempool
            getnetworkhashps  (optional block number)

### requiring one argument

            validateaddress
            sendrawtransaction
            gettxout
            getblock
            estimatefee
            estimatepriority
            decoderawtransaction
            decodescript
            getrawtransaction

### requires three arguments

            verifymessage

To keep the interface simple, additional arguments can be added as arg1, arg2, arg3, etc.

    21 buy —maxprice 99 url http://10.244.34.100:8332/api/getnetworkhashps?arg1=300000

This would get the estimated hash rate of the network at block 300,000.

For more information on the argument(s) for each command, visit https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list They should be provided in the same order as specified by Bitcoin Core.
