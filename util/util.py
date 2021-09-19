from time import sleep


def start_custom_thread(method, interval=0):
    while True:
        method()
        sleep(interval)
