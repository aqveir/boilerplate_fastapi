from fastapi import status, Response

class BaseResponse(Response):
    """
    Base class for all response models.
    """
    media_type: str = "application/json"
    message: str = "Success"
    success: bool = True
    error: bool = False
    data: dict = {}
    #status_code: int = status.HTTP_200_OK

    