# -*- coding: utf-8 -*-
"""
    tests.logic.test_LoggingDirectClientV1
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
from pip_clients_logging.version1.LoggingHttpClientV1 import LoggingHttpClientV1
from .LoggingClientFixtureV1 import LoggingClientFixtureV1

http_config = ConfigParams.from_tuples(
    'connection.host', 'localhost',
    'connection.port', 3000
)

class TestLoggingHttpClientV1:
    persistence = None
    controller = None
    service = None
    client = None
    fixture = None

    @staticmethod
    def setup_class(cls):
        cls.persistence = LoggingMemoryPersistence()
        cls.controller = LoggingController()

        cls.service = LoggingHttpServiceV1()
        cls.service.configure(http_config)

        cls.client = LoggingHttpClientV1()
        cls.client.configure(http_config)
    
        references = References.from_tuples(
            Descriptor('pip-services-logging', 'persistence', 'memory', 'default', '1.0'), cls.persistence,
            Descriptor('pip-services-logging', 'controller', 'default', 'default', '1.0'), cls.controller,
            Descriptor('pip-services-logging', 'service', 'http', 'default', '1.0'), cls.service
        )
        cls.controller.set_references(references)
        cls.service.set_references(references)

        cls.fixture = LoggingClientFixtureV1(cls.client)

    def setup_method(self, method):
        self.persistence.clear(None)
        self.service.open(None)
        self.client.open(None)

    def teardown_method(self, method):
        self.client.close(None)
        self.service.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()