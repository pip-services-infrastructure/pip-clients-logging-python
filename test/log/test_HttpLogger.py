# -*- coding: utf-8 -*-
"""
    tests.logic.test_LoggingHttpClientV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import pytest

from pip_services_commons.refer import References, Descriptor
from pip_services_commons.log import LogLevel
from pip_services_commons.data import FilterParams
from pip_services_commons.errors import ErrorDescriptionFactory
from pip_services_commons.config import ConfigParams
from pip_services_logging.persistence.LoggingMemoryPersistence import LoggingMemoryPersistence
from pip_services_logging.logic.LoggingController import LoggingController
from pip_services_logging.services.version1.LoggingHttpServiceV1 import LoggingHttpServiceV1

from pip_clients_logging.version1.LogMessageV1 import LogMessageV1
from pip_clients_logging.log.HttpLogger import HttpLogger
from .LoggerFixture import LoggerFixture

http_config = ConfigParams.from_tuples(
    'connection.host', 'localhost',
    'connection.port', 3002
)

class TestHttpLogger:
    persistence = None
    controller = None
    service = None
    logger = None
    fixture = None

    @staticmethod
    def setup_class(cls):
        cls.persistence = LoggingMemoryPersistence()
        cls.controller = LoggingController()

        cls.service = LoggingHttpServiceV1()
        cls.service.configure(http_config)
    
        references = References.from_tuples(
            Descriptor('pip-services-logging', 'persistence', 'memory', 'default', '1.0'), cls.persistence,
            Descriptor('pip-services-logging', 'controller', 'default', 'default', '1.0'), cls.controller,
            Descriptor('pip-services-logging', 'service', 'http', 'default', '1.0'), cls.service
        )
        cls.controller.set_references(references)
        cls.service.set_references(references)

        cls.logger = HttpLogger()
        cls.logger.configure(http_config)

        cls.fixture = LoggerFixture(cls.logger, cls.persistence)

    def setup_method(self, method):
        self.persistence.clear(None)
        self.service.open(None)
        self.logger.open(None)

    def teardown_method(self, method):
        self.persistence.clear(None)
        self.logger.close(None)
        self.service.close(None)

    # def test_log_level(self):
    #     self.fixture.test_log_level()

    def test_text_output(self):
        self.fixture.test_text_output()

