from alive_progress import alive_bar; import time

with alive_bar(1000) as bar:
    for i in range(1000):
        time.sleep(0.002)
        bar()
