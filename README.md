# alvarium-sdk-python
Python implementation of the Project Alvarium SDK

# SDK Interface

The SDK provides a minimal API -- DefaultSdk(), Create(), Mutate(), Transit(), Publish() and Close().

### NewSdk()

```python
def DefaultSdk(self, annotators: List[Annotator], config: SdkInfo, logger: Logger) -> DefaultSdk
```

Used to instantiate a new SDK instance with the specified list of annotators.

Takes a list of annotators, a populated configuration and a logger instance. Returns an SDK instance.

### Create()

```python
def create(self, data: bytes, properties: PropertyBag = None) -> None
```

Used to register creation of new data with the SDK. Passes data through the SDK instance's list of annotators.

SDK instance method. Parameters include:


- data -- The data being created represented as bytes

- properties -- Provide a property bag that may be used by individual annotators
### Mutate()

```python
def mutate(self, old_data: bytes, new_data: bytes, properties: PropertyBag = None) -> None
```

Used to register mutation of existing data with the SDK. Passes data through the SDK instance's list of annotators.

SDK instance method. Parameters include:

- old_data -- The source data item that is being modified, represented as bytes

- new_data -- The new data item resulting from the change, represented as bytes

- properties -- Provide a property bag that may be used by individual annotators

Calling this method will link the old data to the new in a lineage. Specific annotations will be applied to the `new` data element.

### Transit()

```python
def transit(self, data: bytes, properties: PropertyBag = None) -> None
```

Used to annotate data that is neither originated or modified but simply handed from one application to another.

SDK instance method. Parameters include:

- data -- The data being handled represented as bytes

- properties -- Provide a property bag that may be used by individual annotators

### Publish()

```python
def publish(self, data: bytes, properties: PropertyBag = None) -> None
```

Used to annotate data that is neither originated or modified but **before** being handed to another application.

SDK instance method. Parameters include:

- data -- The data being handled represented as bytes

- properties -- Provide a property bag that may be used by individual annotators

### Close()

```python
def close(self) -> None
```

SDK instance method. Ensures clean shutdown of the SDK and associated resources.
