# models.py
from pydantic import BaseModel, validator

class Address(BaseModel):
    name: str
    latitude: float
    longitude: float

    @validator('latitude')
    def validate_latitude(cls, value):
        """
        Validate the latitude value to ensure it's within the valid range.

        Args:
            value (float): The latitude value to be validated.

        Raises:
            ValueError: If the latitude value is outside the valid range (-90 to 90 degrees).

        Returns:
            float: The validated latitude value.
        """
        try:
            if value < -90 or value > 90:
                raise ValueError('Latitude must be between -90 and 90 degrees')
        except ValueError as e:
            raise ValueError("Invalid latitude value: {}".format(e))
        return value

    @validator('longitude')
    def validate_longitude(cls, value):
        """
        Validate the longitude value to ensure it's within the valid range.

        Args:
            value (float): The longitude value to be validated.

        Raises:
            ValueError: If the longitude value is outside the valid range (-180 to 180 degrees).

        Returns:
            float: The validated longitude value.
        """
        try:
            if value < -180 or value > 180:
                raise ValueError('Longitude must be between -180 and 180 degrees')
        except ValueError as e:
            raise ValueError("Invalid longitude value: {}".format(e))
        return value
