from setuptools import setup, find_packages


setup(
    name="ARPasswords",
    version="0.0.1",         # Версия
    author="Pavel Milosh",
    author_email="global@pavelmilosh.com",
    description="Multilanguage password manager with encryption for telegram",
    url="https://github.com/pavel-milosh/ARPassword",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiogram",
        "aiosqlite",
        "pyotp",
        "keyring",
        "cryptography"
    ],
    entry_points={
        "console_scripts": [
            "arpasswords=arpasswords.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)