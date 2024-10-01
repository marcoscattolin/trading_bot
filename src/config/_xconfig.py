#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

from abc import ABC
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, get_args

from pydantic_settings import BaseSettings

__all__ = ["XConfig", "BaseConfigProvider"]

ConfigurationClass = TypeVar("ConfigurationClass", bound="XConfig")


class XConfig(BaseSettings, ABC):
    """
    Base class for configuration settings.
    Users of the config module should inherit their configuration class from `XConfig`.

    >>> class CustomConfig(XConfig):
    ...     v1: str = "v1"
    ...     v2: int = 3

    To provide nested configuration, sub-class the `BaseModel` class from Pydantic.
    >>> from pydantic import BaseModel
    ...
    >>> class SubConfig(BaseModel):
    ...    v3: float = 0.4
    ...
    >>> class CustomConfig(XConfig):
    ...    sub: SubConfig
    ...
    >>> import os
    ... os.environ['SUB__V3'] = '0.9'
    ... assert CustomConfig().sub.v3 == 0.9
    """

    class Config:
        env_file = ".env"
        env_nested_delimiter: str = "__"
        # case_sensitive: bool = True


class BaseConfigProvider(Generic[ConfigurationClass], ABC):
    """
    Class for providing a config-singleton.
    Should not be instantiated directly but instead subclassed with an
    appropriate subclass of ConfigurationBase substituting the generic type.
    Usage example:
    >>> class CustomConfig(XConfig):
        ...     v1: str = "v1"
        ...     v2: int = 3
        ...
        >>> class __MyConfigProvider(BaseConfigProvider[CustomConfig]):
        ...     pass
        ...
        >>> _config_provider = __MyConfigProvider()
        ...
        >>> def get_config(reload=False, *args, **kwargs) -> CustomConfig:
        ...     return _config_provider.get_config(reload, *args, **kwargs)
    """

    def __init__(self):
        self.__config_instance = None
        self._config_args: Optional[List[Any]] = None
        self._config_kwargs: Optional[Dict[Any, Any]] = None
        # retrieving the generic type at runtime, see
        # https://stackoverflow.com/questions/48572831/how-to-access-the-type-arguments-of-typing-generic
        self._config_cls: Type[ConfigurationClass] = get_args(
            self.__class__.__orig_bases__[0]
        )[0]

    def _should_update_config_instance(self, reload: bool, args, kwargs):
        return (
            self.__config_instance is None
            or reload
            or self._config_args != args
            or self._config_kwargs != kwargs
        )

    def get_config(
        self,
        reload=False,
        env_file: Optional[str] = None,
        env_prefix: str = "",
        *args,
        **kwargs,
    ) -> ConfigurationClass:
        """
        Retrieves the configuration object (as singleton).

        :param reload: if True, the config will be reloaded from disk even if
            it is a configuration object already exists.
            This is mainly useful in interactive environments like notebooks
        :param env_file: Path to a .env file to read values from.
        :param env_prefix: Optional value to prefix environment variables.
            E.g. you can use 'DEV_' as the `env_prefix` and then all your config
            values are expected to start with 'DEV_', for example 'DEV_POSTGRES_DB'.
            If you want to exclude certain variables from the
            prefixing you can use field(..., env='fixed_name')
            to set the value in the config class for this value.
        :param args: passed to init of the configuration class
        :param kwargs: passed to init of the configuration class constructor
        :return:
        """
        if self._should_update_config_instance(reload, args, kwargs):
            self._config_args = args
            self._config_kwargs = kwargs
            self.__config_instance = self._wrap_with_env_prefix(
                env_file, env_prefix, *args, **kwargs
            )
        return self.__config_instance

    def _wrap_with_env_prefix(
        self,
        environment_file: Optional[str] = None,
        environment_prefix: str = "",
        *args,
        **kwargs,
    ):
        class ConfigWithEnvPrefix(self._config_cls):
            class Config(XConfig.Config):
                env_prefix: str = environment_prefix

        if environment_file is not None:
            return ConfigWithEnvPrefix(_env_file=environment_file, *args, **kwargs)
        else:
            return ConfigWithEnvPrefix(*args, **kwargs)
