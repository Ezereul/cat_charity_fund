from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков QRKot'
    app_description: str = 'Сбор пожертвований для проектов, помогающих котикам'
    # указано, что это имя нужно для корректного прохождения тестов
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
