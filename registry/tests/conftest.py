import config as thmr_config


def pytest_configure(config):
    if not thmr_config.DB_URL == thmr_config.DB_TEST_URL:
        thmr_config.OLD_DB_URL = thmr_config.DB_URL
        thmr_config.DB_URL = thmr_config.DB_TEST_URL


def pytest_unconfigure(config):
    if thmr_config.DB_URL == thmr_config.DB_TEST_URL:
        thmr_config.DB_URL = thmr_config.OLD_DB_URL
