class BaseConfig:
    """Base configuration"""
    TESTING = False


class Development(BaseConfig):
    """Development configuration"""
    pass


class Testing(BaseConfig):
    """Testing configuration"""
    TESTING = True


class Production(BaseConfig):
    """Production configuration"""
    pass