# setup.py
from setuptools import setup, find_packages

setup(
    name="shacnify",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click",
        "rich",
        "inquirerpy",
    ],
    entry_points={
        "console_scripts": [
            "shacnify=shacnify.cli:main_cli"
        ]
    },
    author="Hoang Hong Huy",
    author_email="huy.hoanghong.work@gmail.com",
    description="Một tool CLI để tự động hóa cài đặt Shadcn/UI và Tailwind CSS cho dự án React.",
)