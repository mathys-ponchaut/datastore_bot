import os
from os import path
from warnings import warn
from typing import Union


class Setting:
    """Represents a configuration setting with a name and a value."""

    def __init__(self, name: str, value: str = 'undefined'):
        self.__name = name
        self.__value = value

    def __str__(self):
        # Defines how the object is displayed when printed
        return f"{Setting.__name__}({self.name}: {self.value})"

    def __repr__(self):
        # Defines how the object is represented in lists or in the interpreter
        return f"{Setting.__name__}({self.name}: {self.value})"

    def __eq__(self, other):
        # Equality comparison between two Setting objects
        return vars(self) == vars(other)

    def __ne__(self, other):
        # Inequality comparison between two Setting objects
        return vars(self) != vars(other)

    @property
    def name(self):
        # Read-only property for the setting's name
        return self.__name

    @name.setter
    def name(self):
        # Prevent modification of the setting name
        raise AttributeError("can't modify setting's name")

    @property
    def value(self):
        # Getter for the setting's value
        return self.__value

    @value.setter
    def value(self, value: str = 'undefined'):
        # Validation when changing the value
        if ': ' in value:
            raise ValueError("Value cannot contain ': '")


def get_path():
    """
    Returns the path to the settings file.
    Creates the local directory if it doesn't exist.
    """
    local_path = path.join(os.getenv('LOCALAPPDATA'), 'datastore_bot')
    if not path.exists(local_path):
        os.makedirs(local_path)

    setting_path = path.join(local_path, 'settings.txt')

    print(setting_path)
    return setting_path


def set_settings(settings: Union[list, Setting]):
    """
    Writes a list of Setting objects to the settings file.
    If a single Setting is given, it is converted into a list.
    """
    if not isinstance(settings, (list, Setting)):
        raise ValueError(f"Must be a list of {Setting.__name__}")

    if isinstance(settings, Setting):
        settings = [settings]

    # Build a human-readable text representation of settings
    content = ''
    for i, setting in enumerate(settings):
        content = f'{content}{setting.name}: {setting.value}'
        if not i + 1 == len(settings):
            content = f'{content}\n'

    # Write settings to file
    with open(get_path(), mode='w', encoding='utf-8') as file:
        file.write(content)

    print(settings)
    return settings


def settings(table: bool = False):
    """
    Reads the settings file and returns either:
    - A list of Setting objects (default)
    - A dictionary {name: value} if table=True
    """
    setting_path = get_path()

    try:
        with open(setting_path, mode='r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')

            values = any  # placeholder variable for output (dict or list)
            for line in lines:
                key, value = line.split(': ')

                # Return as dictionary
                if table is True:
                    if not isinstance(values, dict):
                        values = {key: value}
                    else:
                        values[key] = value
                # Return as list of Setting objects
                else:
                    if not isinstance(values, list):
                        values = [Setting(key, value)]
                    else:
                        values.append(Setting(key, value))
            return values

    except OSError:
        # If the file cannot be accessed, warn the user
        warn(f"Can't access '{setting_path}'!")

    # Return an empty structure depending on requested mode
    if table is True:
        return {}
    else:
        return []


def get_setting(name: str):
    """
    Returns the value of a setting by its name.
    If not found, returns None.
    """
    list_settings = settings()

    for setting in list_settings:
        if setting.name == name:
            return setting.value

    return None


def add_setting(setting: Union[list, Setting]):
    """
    Adds one or more settings to the file.
    Raises an error if a setting already exists or duplicates are found.
    """
    if not isinstance(setting, (list, Setting)):
        raise ValueError(f"Value must be a list or Setting, got: '{setting.__class__}'")

    if isinstance(setting, Setting):
        setting = [setting]

    list_setting = settings()      # List of existing Setting objects
    keys_setting = settings(True)  # Dictionary of existing settings
    added_setting = []             # Track added names to detect duplicates

    for s in setting:
        if not isinstance(s, Setting):
            raise ValueError(f"Must be a list of Setting, got: '{s.__class__}'")

        # Check for duplicates (in both added and existing settings)
        if s.name in added_setting or s.name in keys_setting.keys():
            raise ValueError(f"Duplicated setting: '{s.name}'")

        added_setting.append(s.name)
        list_setting.append(s)

    return set_settings(list_setting)


def remove_setting(setting: Union[list, str]):
    """
    Removes one or more settings from the file by name.
    If the name is not found, prints a warning.
    """
    if not isinstance(setting, (list, str)):
        raise ValueError(f"Must be a list or str, got: '{setting.__class__}'")

    if isinstance(setting, str):
        setting = [setting]

    for s in setting:
        if not isinstance(s, str):
            raise ValueError(f"Must be a list of str, got: '{s.__class__}'")

    old_settings = settings()
    new_settings = []

    # Keep only settings that are not in the removal list
    for s in old_settings:
        if s.name not in setting:
            new_settings.append(s)

    if old_settings == new_settings:
        print(f"{str(setting)} not found")
    else:
        print(new_settings)

    return set_settings(new_settings)


def edit_setting(setting: Setting):
    """
    Edits an existing setting by name.
    If the setting does not exist, prints a warning.
    """
    if not isinstance(setting, Setting):
        raise ValueError(f"Must be a {Setting.__name__}, got: '{setting.__class__}'")

    remove_setting(setting.name)
    return add_setting(setting)