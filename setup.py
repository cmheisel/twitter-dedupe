from setuptools import setup, find_packages, Command

version = "0.6"


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name="twitter-dedupe",
    version=version,
    author="Chris Heisel",
    author_email="chris@heisel.org",
    description=("Python library to retweet unique links from noisy Twitter accounts."),
    long_description=open("README.md").read(),
    url="https://github.com/cmheisel/twitter-dedupe",
    zip_safe=False,
    include_package_data=True,
    scripts=['bin/logonly.py', 'bin/retweet.py'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '.html'],
    },
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=[
        "redis",
        "requests",
        "tweepy",
    ],
    cmdclass = {'test': PyTest},
)
