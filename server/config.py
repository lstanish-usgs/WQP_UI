import logging
import os
import re


DEBUG = 'DEBUG' in os.environ

# Verify SSL certs during web service calls by requests, can be a path to a cert bundle
VERIFY_CERT = 'NO_VERIFY_CERT' not in os.environ

# Do not use the same key as any of the deployment servers
SECRET_KEY = os.environ.get('SECRET_KEY')

PROJECT_HOME = os.path.dirname(__file__)

# Application defined config variables

# Site summary URL
SITE_SUMMARY_ENDPOINT = 'https://www.waterqualitydata.us/data/summary/monitoringlocation/search/'

# Points to the geoserver endpoint you want to use.
WQP_MAP_GEOSERVER_ENDPOINT = os.environ.get('WQP_MAP_GEOSERVER_ENDPOINT')

SITES_MAP_GEOSERVER_ENDPOINT = os.environ.get('SITES_MAP_GEOSERVER_ENDPOINT')

# Points to the sld endpoint you want to use.
# SLD_ENDPOINT = os.environ.get('SLD_ENDPOINT')
SLD_ENDPOINT = 'https://www.waterqualitydata.us/Codes/Summary?dataSource=A&geometry=S&timeFrame=A'


# Points to the codes endpoint
CODES_ENDPOINT = os.environ.get('CODES_ENDPOINT')

# Points to the query endpoint. Does not include the type of data or 'search' part of the endpoint
SEARCH_QUERY_ENDPOINT = os.environ.get('SEARCH_QUERY_ENDPOINT', 'https://www.waterqualitydata.us/')

# Points to the public srsnames endpoint you want to use.
PUBLIC_SRSNAMES_ENDPOINT = os.environ.get('PUBLIC_SRSNAMES_ENDPOINT')

HYDRO_LAYER_ENDPOINT = 'https://tiles.arcgis.com/tiles/P3ePLMYs2RVChkJx/arcgis/rest/services/Esri_Hydro_Reference_Overlay/MapServer'
NHDPLUS_FLOWLINE_ENDPOINT = 'https://labs.waterdata.usgs.gov/geoserver/wms'
NHDPLUS_FLOWLINE_LAYER_NAME = 'wmadata:nhdflowline_network'

# Points to the endpoint which returns flow lines and sites for a comid
NLDI_SERVICES_ENDPOINT = os.environ.get('NLDI_SERVICES_ENDPOINT')

NWIS_SITES_SERVICE_ENDPOINT = 'https://waterservices.usgs.gov/nwis/site/'
NWIS_SITES_INVENTORY_ENDPOINT = 'https://waterdata.usgs.gov/monitoring-location/'

GEO_SEARCH_API_ENDPOINT = 'https://txdata.usgs.gov/search_api/1.1/services.ashx/search'

WSGI_STR = os.environ.get('WSGI_STR', '')  # When using real urls this is the string that should be removed from url's to get the correct mapping

# In each dictionary,
#    The 'id' key should be given a string value - the name of a style present on GeoServer
#    The 'text' key should be given a string value - user-facing text that appears in the web ui's dropdown for selecting styles
SITE_SLDS = [
    {'id' : 'wqp_sources', 'text' : 'By source'},
    {'id' : 'site_type', 'text' : 'By site type'},
    {'id' : 'activity_visual', 'text' : 'By activity'}
]

GA_TRACKING_CODE = os.environ.get('GA_TRACKING_CODE', '')

# Set to false in instance/config.py if you want to turn off the NLDI feature,
# or set NLDI_DISABLED in the environment.
NLDI_ENABLED = 'NLDI_DISABLED' not in os.environ

SORTING_CHECKBOX_ENABLED = False  # Setting  to False as we want this to be off except during development

# For robots.txt
ROBOTS_WELCOME = 'ROBOTS_WELCOME' in os.environ

# Set the local base url, this deals with the weird way we do wsgi around here
LOCAL_BASE_URL = os.environ.get('LOCAL_BASE_URL', '')

# Allow for setting an announcement banner without having to release code
ANNOUNCEMENT_BANNER = os.environ.get('ANNOUNCEMENT_BANNER')

# Logging Configuration
LOGGING_ENABLED = 'LOGGING_DISABLED' not in os.environ
LOGGING_DIRECTORY = os.environ.get('LOGGING_DIRECTORY')
LOGGING_LEVEL = int(os.environ.get('LOGGING_LEVEL', logging.DEBUG))
LOG_RETENTION = int(os.environ.get('LOG_RETENTION', '30'))
# These aren't overridden anywhere, so maintain as hardcoded tuples
LOG_ROLLOVER_TIME = (0, 0)  # tuple of format (hour, minute)
LOG_DELETE_TIME = (1, 0)  # tuple of format (hour, minute)

# To use hashed assets, set this to the gulp-rev-all rev-manifest.json path
ASSET_MANIFEST_PATH = os.environ.get('ASSET_MANIFEST_PATH')

STATIC_ROOT = os.environ.get('STATIC_ROOT', '/static/')
