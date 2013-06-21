from distutils.core import setup

setup(name='rabbit_sse',
      version='0.1',
      author='Darren Worrall',
      description="Flask extension providing SSE support for RabbitMQ",
      py_modules=['rabbit_sse',],
      provides=['rabbit_sse',],
      install_requires=[l.strip() for l in open('requirements.txt').readlines()],
     )
