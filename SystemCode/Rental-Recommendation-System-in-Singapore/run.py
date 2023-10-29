# find . -name "__pycache__" -exec rm -r {} + 当前目录及其所有子目录中查找并删除所有的 __pycache__ 目录

import os
from flask_migrate import Migrate
from flask_minify  import Minify
from sys import exit

from app.config import config_dict
from app import create_app, db

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
    
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )
    app.logger.info('GEOCODING_APIKEY      = ' + app_config.GEOCODING_APIKEY )


if __name__ == "__main__":
    app.run()
    
    