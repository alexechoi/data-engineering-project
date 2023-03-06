import sys
import itertools
import time

# Spinner function
def spinner_thread():
    while True:
        for char in itertools.cycle('|/-\\'):
            sys.stdout.write(f'\rProcess working... {char}')
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\r')