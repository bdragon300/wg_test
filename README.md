# Installation

```
pip3 -r requirements.txt
```

Then specify `wsgi.app` as application object in wsgi configuration

Next, create site configuration file (`config.py` for instance) and put its path
to the `CONFIG_FILE` environment variable. As long as it is not specified the
default configuration from `default_config.py` will be used.

# API

`/fibonachi?from=x&to=y` will return Fibonacci sequence in given range. Response format: JSON.

# Development server

Run `python3 wsgi.py` and development server will appear at 127.0.0.1:5000. Make sure you have started Memcached instance.

