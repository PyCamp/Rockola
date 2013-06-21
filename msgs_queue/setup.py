from distutils.core import setup

setup(name='queue_manager',
      version='0.1',
      description="Publish and consume messages from RabbitMQ",
      py_modules=['queue_manager',],
      provides=['queue_manager',],
      install_requires=['pika',],
     )
