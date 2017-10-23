
import threading


def do_this(func, *args, **kwargs):
    th = threading.Thread(target=func, args=args, kwargs=kwargs)
    th.start()
    th.join()
    return not th.isAlive()

