Overview
--------

FixSim is an example project for FIX protocol client and server implementations.
It can be used for testing your client or server and you might
find a need to add new feature or change fixsim's behavior. FixSim also can be used
just as example for implementing acceptors and initiators.

Configuration
-------------

FixSim consists of two scripts fixsim-client.py and fixsim-server.py. Each
script uses two configuration files, one for FIX Session settings in ini format
and one for business logic in YAML. You can find example configurations with
comments in project tree. For example server and client may be started by commands:

```
python fixsim-server --acceptor_config fixsim-server.conf.ini --config
fixsim-server.conf.yaml
```
```
python fixsim-client --initiator_config fixsim-client.conf.ini --config
fixsim-client.conf.yaml
```

FixSim depends on twisted but you can easily purge it from poject by replacing reactor infinite loop by differrent infinite loop in main thread and implementing something like twisted.internet.task.LoopingCall which is used for periodical sending snapshots and subscribing to instruments.

FixSim supports only FIX44 now  

Workflow
--------

FixSim business logic is pretty simple. Server receives client session and stores it. Client subscribes to the one or more instrument (like EUR/USD, USD/CAD etc) and server starts sending market data snapshots to client. Client can create a new orderfor each snapshot and send it to acceptor or skip this snapshot (see skip_snapshot_chance attr in client yaml config). Order is created for one randomly selected quote from previously received snapshot. For each such order acceptor can create filled or rejected execution report(see reject rate in server yaml config) 


