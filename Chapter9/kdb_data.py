from pyq import q
from datetime import date

#googdata:([]dt:();high:();low:();open:();close:();volume:(),adj_close:())

q.insert('googdata', (date(2014,01,2), 555.263550, 550.549194, 554.125916, 552.963501, 3666400.0, 552.963501))
q.insert('googdata', (date(2014,01,3), 554.856201, 548.894958, 553.897461, 548.929749, 3355000.0, 548.929749))

q.googdata.show()
                  High         Low        Open       Close     Volume   Adj Close
Date
2014-01-02  555.263550  550.549194  554.125916  552.963501  3666400.0  552.963501
2014-01-03  554.856201  548.894958  553.897461  548.929749  3355000.0  548.929749

# f:{[s]select from googdata where date=d}

x=q.f('2014-01-02')
print(x.show())

2014-01-02  555.263550  550.549194  554.125916  552.963501  3666400.0  552.963501
