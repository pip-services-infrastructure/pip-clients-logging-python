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

from pip_clients_logging.version1.LogMessageV1 import LogMessageV1
from pip_clients_logging.version1.LoggingDirectClientV1 import LoggingDirectClientV1
from .LoggingClientFixtureV1 import LoggingClientFixtureV1

class TestLoggingDirectClientV1:
    persistence = None
    controller = None
    client = None
    fixture = None

    @staticmethod
    def setup_class(cls):
        cls.persistence = LoggingMemoryPersistence()
        cls.controller = LoggingController()
        cls.client = LoggingDirectClientV1()
    
        references = References.from_tuples(
            Descriptor('pip-services-logging', 'persistence', 'memory', 'default', '1.0'), cls.persistence,
            Descriptor('pip-services-logging', 'controller', 'default', 'default', '1.0'), cls.controller,
            Descriptor('pip-services-logging', 'client', 'direct', 'default', '1.0'), cls.client
        )
        cls.controller.set_references(references)
        cls.client.set_references(references)

        cls.fixture = LoggingClientFixtureV1(cls.client)

    def setup_method(self, method):
        self.persistence.clear(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()