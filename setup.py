from setuptools import setup, find_packages

setup(
    name="weather_monitoring",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'sqlalchemy',
        'pandas',
        'matplotlib',
        'pytest',
        'pytest-asyncio',
        'python-dotenv'
    ],
)