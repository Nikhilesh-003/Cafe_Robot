from setuptools import find_packages, setup

package_name = 'goat_examples'

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
    maintainer='niki',
    maintainer_email='niki@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cafe_navigator = automation_examples.cafe_navigator:start_app',
            'butler_robot_server = automation_examples.butler_robot_server:main',
            'butler_robot_client = automation_examples.butler_robot_client:main',
            'food_delivery_server = automation_examples.food_delivery_server:main',
            'food_delivery_client = automation_examples.food_delivery_client:main',
            'moveto_server = automation_examples.moveto_server:main',
            'moveto_client = automation_examples.moveto_client:main',
            'multi_order_server = automation_examples.multi_order_server:main',
            'multi_order_client = automation_examples.multi_order_client:main',
        ],
    },
)
