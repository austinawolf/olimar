import json
import os
from typing import List, Any

from pydantic import BaseModel, ValidationError


class FileConfig(BaseModel):
    class Config:
        # Enable strict validation
        strict = False
        # Use any other Pydantic configurations you need
        validate_assignment = True  # Ensure validation on attribute assignment

    @classmethod
    def get_path(cls) -> str:
        """Return the default path for the configuration file."""
        return "config.json"

    @classmethod
    def load(cls, file_path: str = None):
        """
        Load the configuration from a JSON file.

        :param file_path: The path to the configuration file. Defaults to the result of get_path().
        :return: An instance of FileConfig populated with the data from the file.
        :raises ValidationError: If the file content does not conform to the model schema.
        :raises JSONDecodeError: If the file content is not valid JSON.
        :raises ValueError: If the file is empty.
        """
        file_path = file_path if file_path else cls.get_path()
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("File is empty")
                return cls.parse_raw(content)
        except ValidationError as e:
            # Handle validation errors
            errors = e.errors()
            print(f"{len(errors)} validation error(s) detected parsing config at: {file_path}")
            for err in errors:
                location = ".".join(err.get('loc', []))
                message = err.get('msg', '')
                print(f"\tField: {location} ({message})")
            quit()
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            raise e
        except ValueError as e:
            # Handle empty file errors
            raise e
        except FileNotFoundError as e:
            print("Config not found. Creating default.")
            self = cls()
            self.save()
            return self

    def save(self):
        """
        Save the configuration to a JSON file.

        :raises OSError: If an error occurs while creating the directory or writing the file.
        """
        path = self.get_path()
        dir_path = os.path.dirname(path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        with open(path, 'w') as f:
            json.dump(self.model_dump(), f, indent=4)

    @classmethod
    def get_fields(cls) -> List[str]:
        """Retrieve all fields of the model."""
        return list(cls.model_fields.keys())

    def set(self, field, value):
        try:
            setattr(self, field, value)
        except ValidationError as e:
            errors = e.errors()
            print(f"{len(errors)} validation error(s) detected setting field")
            for err in errors:
                location = ".".join(err.get('loc', []))
                message = err.get('msg', '')
                print(f"\tField: {location} ({message})")
                quit()

    def get(self, field) -> Any:
        return json.dumps(getattr(self, field))
