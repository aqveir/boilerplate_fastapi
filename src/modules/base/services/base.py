class BaseService:
    def __init__(self, repository=None, dynamodb_service=None):
        self.repository = repository
        self.dynamodb_service = dynamodb_service