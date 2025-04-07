class RepositoryProtocol:

    def get_or_create_many(self, filter_set) -> list:
        """Get if exists, create if not exists for many recipients"""
        pass

    def create(self, dto_creator) -> object:
        """Create a new object"""

    def get(self, filter_set) -> object:
        """Get single object"""

    def get_many(self, filter_set) -> list[object]:
        """Get many objects by filter set"""
