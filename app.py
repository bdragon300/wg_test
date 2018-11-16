import flask
import os
from flask_pymemcache import FlaskPyMemcache

app = flask.Flask('test_wg')

# You can override config file via CONFIG_FILE environment var
config_fn = os.environ.get('CONFIG_FILE') or 'config/default_config.py'
app.config.from_pyfile(config_fn)

memcache = FlaskPyMemcache()
memcache.init_app(app)
