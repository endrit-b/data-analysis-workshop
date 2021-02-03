from dotenv import load_dotenv, find_dotenv


def load_env_vars(env='dev'):
    """
    A helper function used to load environment variables based on running env
    ie. if we're running in production, it should load prod variables
    :param env:
    :return:
    """
    if env == 'production':
        load_dotenv(find_dotenv('.env.prod'))
    elif env == 'test':
        load_dotenv(find_dotenv('.env.dev'))
    elif env == 'dev':
        load_dotenv(find_dotenv('.env.dev'))
