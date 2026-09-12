from setuptools import find_packages, setup

package_name = 'water_leak_detector'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Emiliano',
    maintainer_email='emiliano.bucam@gmail.com',
    description='TODO: Package description',
    license='Nodo ROS 2 que detecta fugas de agua',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'leak_detector_node = water_leak_detector.leak_detector_node:main',
        'sensor_simulator_node = water_leak_detector.sensor_simulator_node:main',
        ],
    },
)
