from setuptools import setup, find_packages


setup(
    name="ARPasswords",
    version="1.2.1",
    author="Pavel Milosh",
    author_email="code@pavelmilosh.com",
    description="Multilanguage password manager with encryption for telegram",
    url="https://github.com/pavel-milosh/ARPassword",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "arpasswords": ["locales/*"],
    },
    install_requires=[
        "aiogram",
        "aiosqlite",
        "pyotp",
        "keyring",
        "keyrings.alt",
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
    python_requires=">=3.11"
)