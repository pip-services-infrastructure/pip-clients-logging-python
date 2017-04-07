# Client API (version 1) <br/> Logging Microservices Client SDK for Python

Python client API for Logging microservice is a thin layer on the top of
communication protocols. It hides details related to specific protocol implementation
and provides high-level API to access the microservice for simple and productive development.

* [Installation](#install)
* [Getting started](#get_started)
* [LogMessageV1 class](#class1)
* [ILoggingClientV1 interface](#interface)
    - [read\_messages()](#operation1)
    - [read\_errors()](#operation2)
    - [write\_message()](#operation3)
    - [write\_messages()](#operation4)
    - [clear()](#operation5)
* [LoggingHttpClientV1 class](#client_http)
* [LoggingDirectClientV1 class](#client_direct)
* [LoggingNullClientV1 class](#client_null)

## <a name="install"></a> Installation

To work with the client SDK add dependency into **requirements.txt** file of your project
```text
pip_clients_logging_node>=1.0
```

Then download the dependency using **pip**:

```javascript
# Installing dependencies
pip install -r requirements.txt
```

## <a name="get_started"></a> Getting started

This is a simple example on how to work with the microservice using HTTP client:

```python
import datetime
from pip_services_commons.log import LogLevel
from pip_services_commons.config import ConfigParams
from pip_services_commons.data import FilterParams, PagingParams
from pip_clients_logging_node.version1 import LoggingHttpClientV1, LoggingMessageV1

# Client configuration
config = ConfigParams.from_tuples(
    "connection.protocol", "http",
    "connection.host", "localhost", 
    "connection.port", 8003
)

# Create the client instance
client = LoggingHttpClientV1(config)

# Connect to the microservice
try:
    client.open(None)

    # Log a message
    message = client.write_message(
        None,
        LogMessageV1(LogLevel.Info, None, None, None, "Restarted server")
    )

    print('Logger message is')
    print(message)

    # Remember: all dates shall be in utc
    now = datetime.datetime.utcnow()

    # Get the list system activities
    page = client.read_messages(
        None,
        FilterParams.from_tuples(
            "from_time", datetime.datetime.utcnow() - datetime.timediff(days=1),
            "to_time": datetime.datetime.utcnow(),
            "search": "server"
        ),
        PagingParams(0, 10, True),
    )

    print('Messages containing "server" were')
    print(page.data)

    # Close connection
    client.close(None)
except Exception as ex:
    print('Connection to the microservice failed')
    print(ex)
```

### <a name="class1"></a> LogMessageV1 class

Represents a record of a system activity performed in the past

**Properties:**
- correlation_id: string - unique id of transaction that caused the event
- time: Date - date and time in UTC when the event took place (default: current time)
- source: string - server name where event took place (default: current host)
- level: number - log level: 1 - fatal, 2 - error, 3 - warning, 4 - info, 5 - debug, 6 - trace.
- error: Object - error object
- message: string - descriptive message

## <a name="interface"></a> ILoggingClientV1 interface

If you are using Typescript, you can use ILoggingClientV1 as a common interface across all client implementations. 
If you are using plain Javascript, you shall not worry about ILoggingClientV1 interface. You can just expect that
all methods defined in this interface are implemented by all client classes.

```python
class ILoggingClientV1:
    def read_messages(correlation_id, filter, paging)
    def write_message(correlation_id, message)
    def write_messages(correlation_id, messages)
    def clear(correlation_id)
```

### <a name="operation1"></a> read\_messages(correlation_id, filter, paging, callback)

Retrieves logged messages by specified criteria

**Arguments:** 
- correlation_id: string - id that uniquely identifies transaction
- filter: object - filter parameters
  - search: string - (optional) search substring to find in source, type or message
  - level: number - (optional) log level
  - max_level: number - (optional) maximum log level
  - from_time: Date - (optional) start of the time range
  - to_time: Date - (optional) end of the time range
- paging: object - paging parameters
  - skip: int - (optional) start of page (default: 0)
  - take: int - (optional) page length (default: 100)
  - total: boolean - (optional) include total counter into paged result (default: false)

**Result**
  - DataPage<LogMessageV1> - retrieved LogMessageV1 objects in paged format

### <a name="operation2"></a> read\_errors(correlation_id, filter, paging, callback)

Retrieves logged errors by specified criteria

**Arguments:** 
- correlation_id: string - id that uniquely identifies transaction
- filter: object - filter parameters
  - search: string - (optional) search substring to find in source, type or message
  - level: number - (optional) log level
  - max_level: number - (optional) maximum log level
  - from_time: Date - (optional) start of the time range
  - to_time: Date - (optional) end of the time range
- paging: object - paging parameters
  - skip: int - (optional) start of page (default: 0)
  - take: int - (optional) page length (default: 100)
  - total: boolean - (optional) include total counter into paged result (default: false)

**Result**
  - DataPage<LogMessageV1> - retrieved LogMessageV1 objects in paged format

### <a name="operation3"></a> write\_message(correlation_id, message, callback)

Log message

**Activities:** 
- correlation_id: string - id that uniquely identifies transaction
- message: LogMessageV1 - message to be logged

**Result**
  - LogMessageV1 - logged system event
 
### <a name="operation4"></a> write\_messages(correlation_id, messages, callback)

Log multiple messages

**Activities:** 
- correlation_id: string - id that uniquely identifies transaction
- messages: LogMessageV1[] - array of messages to be logged

**Result**
- None

### <a name="operation5"></a> clear(correlation_id, callback)

Clears all logged messages and errors

**Activities:** 
- correlation_id: string - id that uniquely identifies transaction

**Result**
- None

## <a name="client_http"></a> LoggingHttpClientV1 class

LoggingHttpClientV1 is a client that implements HTTP protocol

```python
class LoggingHttpClientV1(CommandableHttpClient, ILoggingClientV1):
    def __init__(config?: any)
    def set_references(references)
    def open(correlation_id)
    def close(correlation_id)
    def read_messages(correlation_id, filter, paging)
    def write_message(correlation_id, message)
    def write_messages(correlation_id, messages)
    def clear(correlation_id)
```

**Constructor config properties:** 
- connection: object - HTTP transport configuration options
  - type: string - HTTP protocol - 'http' or 'https' (default is 'http')
  - host: string - IP address/hostname binding (default is '0.0.0.0')
  - port: number - HTTP port number

## <a name="client_direct"></a> LoggingDirectClientV1 class

LoggingDirectClientV1 is a client that calls controller directly from the same container.
It can be used in monolythic deployments when multiple microservices run in the same process.

```python
class LoggingDirectClientV1(DirectClient, ILoggingClientV1):
    def __init__(config?: any)
    def set_references(references)
    def open(correlation_id)
    def close(correlation_id)
    def read_messages(correlation_id, filter, paging)
    def write_message(correlation_id, message)
    def write_messages(correlation_id, messages)
    def clear(correlation_id)
```

## <a name="client_null"></a> LoggingNullClientV1 class

LoggingNullClientV1 is a dummy client that mimics the real client but doesn't call a microservice. 
It can be useful in testing scenarios to cut dependencies on external microservices.

```python
class LoggingNullClientV1(ILoggingClientV1):
    def read_messages(correlation_id, filter, paging)
    def write_message(correlation_id, message)
    def write_messages(correlation_id, messages)
    def clear(correlation_id)
```
