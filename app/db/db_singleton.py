from abc import ABCMeta, abstractmethod
from sqlalchemy import (MetaData, create_engine)
from databases import Database
import threading


# This is a metaclass for creating singleton classes.
class SingletonMeta(type):
    _instances = {}  # Dictionary to hold the instance reference for each class
    _lock = threading.Lock()  # A lock to ensure thread-safe singleton instantiation

    def __call__(cls, *args, **kwargs):
        # Acquire the lock to make sure that only one thread can enter this block at a time
        with cls._lock:
            # Check if the instance already exists for the class
            if cls not in cls._instances:
                # if not, create the instance and store it in the _instances dictionary
                cls._instances[cls] = super().__call__(*args, **kwargs)
        # Return the instance
        return cls._instances[cls]


# This metaclass combines the features of singletonmeta and ABCmeta
class SingletonABCMeta(ABCMeta, SingletonMeta):
    def __new__(cls, name, bases, namespace):
        # Create a new class using the combined metaclasses
        return super().__new__(cls, name, bases, namespace)


# BaseDatabaseClient is an abstract class with the SingletonABCMeta metaclass
class BaseDatabaseClient(metaclass=SingletonABCMeta):
    # These methods are abstract, meaning subclasses must implement these methods
    @abstractmethod
    def startup(cls):
        pass

    @abstractmethod
    def shutdown(cls):
        pass

    @abstractmethod
    def execute(cls, query):
        pass


# DatabaseClient is a concrete implementation of BaseDatabaseClient
class DatabaseClient(BaseDatabaseClient):
    user: str
    password: str
    table: str

    def __init__(self, user, password, table):
        self.user = user
        self.password = password
        self.table = table

        self.connection_url = f"postgresql://{user}:{password}@localhost/{table}"
        self.database = Database(self.connection_url)
        self.engine = create_engine(self.connection_url)
        self.metadata = MetaData()

    async def startup(self):
        await self.database.connect()

    async def shutdown(self):
        await self.database.disconnect()

    async def execute(self, query):
        return await self.database.execute(query)
