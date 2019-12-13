from datetime import datetime

class SimulatedRealClock:
    def __init__(self,simulated=False):
        self.simulated = simulated
        self.simulated_time = None
    def process_order(self,order):
        self.simulated_time= \
            datetime.strptime(order['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
    def getTime(self):
        if not self.simulated:
            return datetime.now()
        else:
            return self.simulated_time

realtime=SimulatedRealClock()
print(realtime.getTime())
simulatedtime=SimulatedRealClock(simulated=True)
simulatedtime.process_order({'id' : 1, 'timestamp' : '2018-06-29 08:15:27.243860'})
print(simulatedtime.getTime())
