"""
Base service for Falcon services.
"""

class BaseService:
    """Base class shared by application services."""

    def __init__(self, data_provider=None):
        self.data_provider = data_provider
