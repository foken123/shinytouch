import time

module_time_start = time.clock()

n = 0
for x in range(0,10000000):
  n += x

module_time_stop = time.clock()

print '\nTotal module time: \n', (module_time_stop - module_time_start) * 1000

