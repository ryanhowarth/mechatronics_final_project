How to use the pigpio encoder library:

start the pigpio daemon in seperate shell
```
sudo pigpiod
```

run the rotary_encoder.py script as root. Encoder output should displayed in the shell. Pin numbers are defined using there broadcom number according to the chart at the bottom of this page: http://abyz.co.uk/rpi/pigpio/index.html
```
sudo ./rotary_encoders.py
```

Ideally to incorporate this into final navigation we need to spin this off as a thread and use the queue class to pass data between the threads. 

Queue: https://docs.python.org/2/library/queue.html
Threading: https://docs.python.org/2/library/threading.html

would look something like this:
```
def main():
    ...
    threading.Thread(target=my_rotary_encoder_class).start()
    ...

```


