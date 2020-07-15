import up

class ClientConfig(object):
        """
        Config for PyUpdater client
        """
        APP_NAME = 'upDemo'
        COMPANY_NAME = 'Laboratory'
        APP_VERSION = up.__version__
        MAX_DOWNLOAD_RETRIES = 1
        PUBLIC_KEY = None
        UPDATE_URLS = ['http://127.0.0.2:5000']