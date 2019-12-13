from chapter9.simulatedclock import SimulatedRealClock
import threading
from time import sleep
from datetime import datetime, timedelta

class TimeOut(threading.Thread):
    def __init__(self,sim_real_clock,time_to_stop,fun):
        super().__init__()
        self.time_to_stop=time_to_stop
        self.sim_real_clock=sim_real_clock
        self.callback=fun
        self.disabled=False
    def run(self):
        while not self.disabled and\
                self.sim_real_clock.getTime() < self.time_to_stop:
            sleep(1)
        if not self.disabled:
            self.callback()


class OMS:
    def __init__(self,sim_real_clock):
        self.sim_real_clock = sim_real_clock
        self.five_sec_order_time_out_management=\
            TimeOut(sim_real_clock,
                sim_real_clock.getTime()+timedelta(0,5),
                    self.onTimeOut)
    def send_order(self):
        self.five_sec_order_time_out_management.disabled = False
        self.five_sec_order_time_out_management.start()
        print('send order')
    def receive_market_reponse(self):
        self.five_sec_order_time_out_management.disabled=True
    def onTimeOut(self):
        print('Order Timeout Please Take Action')

if __name__ == '__main__':
    print('case 1: real time')
    simulated_real_clock=SimulatedRealClock()
    oms=OMS(simulated_real_clock)
    oms.send_order()
    for i in range(10):
        print('do something else: %d' % (i))
        sleep(1)

    print('case 2: simulated time')
    simulated_real_clock=SimulatedRealClock(simulated=True)
    simulated_real_clock.\
        process_order({'id' : 1,\
                       'timestamp' : '2018-06-29 08:15:27.243860'})
    oms = OMS(simulated_real_clock)
    oms.send_order()
    simulated_real_clock. \
        process_order({'id': 1, \
                       'timestamp': '2018-06-29 08:21:27.243860'})
