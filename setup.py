from setuptools import setup, find_packages

setup(
    name="chatdollkit_aituber",
    version="0.2.2",
    url="https://github.com/uezo/chatdollkit-aituber",
    author="uezo",
    author_email="uezo@uezo.net",
    maintainer="uezo",
    maintainer_email="uezo@uezo.net",
    description="A RESTful API server to control ChatdollKit-based AITuber 💬",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["examples*", "tests*"]),
    install_requires=["fastapi", "uvicorn", "pytchat"],
    license="Apache v2",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
