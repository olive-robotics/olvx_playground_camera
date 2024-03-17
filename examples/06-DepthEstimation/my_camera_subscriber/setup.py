from setuptools import setup

package_name = 'my_camera_subscriber'
setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='malek',
    maintainer_email='malek.dhiab@tum.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_subscriber = my_camera_subscriber.camera_subscriber:main',
            'depth_map_comparison_node = my_camera_subscriber.depth_map_comparison_node:main',
            'stereo_depth_comparison_node = my_camera_subscriber.stereo_depth_comparison_node:main',
            'stereo_depth_estimation_node = my_camera_subscriber.stereo_depth_estimation_node:main',
            'stereo_depth_comparison_realtime_model_node = my_camera_subscriber.stereo_depth_comparison_realtime_model_node:main',
        ],
    },
)


