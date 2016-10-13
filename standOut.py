import sys
from time import sleep
i = 0

while i < 20000:
	i += 1
	sys.stdout.flush()
	sys.stdout.write('\rdog%d' % i)
	sleep(0.1)
	
