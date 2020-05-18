from time import time
import gc

start_time = time()
i = 0
print(gc.get_count())
print("Threshold: ", gc.get_threshold())
while True:
    end_time = time()
    i += 1
    time_taken = end_time - start_time  # time_taken is in seconds
    hours, rest = divmod(time_taken, 3600)
    minutes, seconds = divmod(rest, 60)
    print(i, "Total time: ", hours, minutes, int(seconds))
    if i % 1000 == 0:
        print("current i: ", i)

