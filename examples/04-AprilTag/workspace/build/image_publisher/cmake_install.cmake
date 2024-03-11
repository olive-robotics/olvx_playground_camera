# Install script for directory: /home/olive/ros2_ws/src/image_publisher

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/olive/ros2_ws/install/image_publisher")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/olive/ros2_ws/src/image_publisher/include/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/environment" TYPE FILE FILES "/opt/ros2/humble/build/ament_package/ament_package/template/environment_hook/library_path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/environment" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/library_path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libimage_publisher.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libimage_publisher.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libimage_publisher.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/olive/ros2_ws/build/image_publisher/libimage_publisher.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libimage_publisher.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libimage_publisher.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libimage_publisher.so"
         OLD_RPATH "/opt/ros2/humble/install/camera_info_manager/lib:/home/olive/ros2_ws/install/cv_bridge/lib:/home/olive/ros2_ws/install/image_transport/lib:/home/olive/ros2_ws/install/rclcpp_components/lib:/usr/local/lib:/opt/ros2/humble/install/camera_calibration_parsers/lib:/opt/ros2/humble/install/sensor_msgs/lib:/opt/ros2/humble/install/geometry_msgs/lib:/opt/ros2/humble/install/std_msgs/lib:/opt/ros2/humble/install/message_filters/lib:/home/olive/ros2_ws/install/rclcpp/lib:/opt/ros2/humble/install/libstatistics_collector/lib:/home/olive/ros2_ws/install/rcl/lib:/opt/ros2/humble/install/rmw_implementation/lib:/opt/ros2/humble/install/rcl_logging_spdlog/lib:/opt/ros2/humble/install/rcl_logging_interface/lib:/home/olive/ros2_ws/install/rcl_yaml_param_parser/lib:/opt/ros2/humble/install/libyaml_vendor/lib:/home/olive/ros2_ws/install/rosgraph_msgs/lib:/home/olive/ros2_ws/install/statistics_msgs/lib:/opt/ros2/humble/install/tracetools/lib:/opt/ros2/humble/install/ament_index_cpp/lib:/opt/ros2/humble/install/class_loader/lib:/opt/ros2/humble/install/console_bridge_vendor/lib:/home/olive/ros2_ws/install/composition_interfaces/lib:/home/olive/ros2_ws/install/rcl_interfaces/lib:/home/olive/ros2_ws/install/builtin_interfaces/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_c/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_cpp/lib:/opt/ros2/humble/install/fastcdr/lib:/opt/ros2/humble/install/rmw/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_c/lib:/opt/ros2/humble/install/rosidl_typesupport_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_c/lib:/opt/ros2/humble/install/rosidl_runtime_c/lib:/home/olive/ros2_ws/install/rcpputils/lib:/opt/ros2/humble/install/rcutils/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libimage_publisher.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/image_publisher/image_publisher_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/image_publisher/image_publisher_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/image_publisher/image_publisher_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/image_publisher" TYPE EXECUTABLE FILES "/home/olive/ros2_ws/build/image_publisher/image_publisher_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/image_publisher/image_publisher_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/image_publisher/image_publisher_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/image_publisher/image_publisher_node"
         OLD_RPATH "/home/olive/ros2_ws/build/image_publisher:/opt/ros2/humble/install/camera_info_manager/lib:/home/olive/ros2_ws/install/cv_bridge/lib:/home/olive/ros2_ws/install/image_transport/lib:/home/olive/ros2_ws/install/rclcpp_components/lib:/opt/ros2/humble/install/camera_calibration_parsers/lib:/opt/ros2/humble/install/sensor_msgs/lib:/opt/ros2/humble/install/geometry_msgs/lib:/opt/ros2/humble/install/std_msgs/lib:/opt/ros2/humble/install/message_filters/lib:/home/olive/ros2_ws/install/rclcpp/lib:/opt/ros2/humble/install/libstatistics_collector/lib:/home/olive/ros2_ws/install/rcl/lib:/opt/ros2/humble/install/rmw_implementation/lib:/opt/ros2/humble/install/rcl_logging_spdlog/lib:/opt/ros2/humble/install/rcl_logging_interface/lib:/home/olive/ros2_ws/install/rcl_yaml_param_parser/lib:/opt/ros2/humble/install/libyaml_vendor/lib:/home/olive/ros2_ws/install/rosgraph_msgs/lib:/home/olive/ros2_ws/install/statistics_msgs/lib:/opt/ros2/humble/install/tracetools/lib:/opt/ros2/humble/install/ament_index_cpp/lib:/opt/ros2/humble/install/class_loader/lib:/opt/ros2/humble/install/console_bridge_vendor/lib:/home/olive/ros2_ws/install/composition_interfaces/lib:/home/olive/ros2_ws/install/rcl_interfaces/lib:/home/olive/ros2_ws/install/builtin_interfaces/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_c/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_cpp/lib:/opt/ros2/humble/install/fastcdr/lib:/opt/ros2/humble/install/rmw/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_c/lib:/opt/ros2/humble/install/rosidl_typesupport_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_c/lib:/opt/ros2/humble/install/rosidl_runtime_c/lib:/home/olive/ros2_ws/install/rcpputils/lib:/opt/ros2/humble/install/rcutils/lib:/usr/local/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/image_publisher/image_publisher_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher" TYPE DIRECTORY FILES "/home/olive/ros2_ws/src/image_publisher/launch")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/package_run_dependencies" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/image_publisher")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/parent_prefix_path" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/image_publisher")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/environment" TYPE FILE FILES "/opt/ros2/humble/install/ament_cmake_core/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/environment" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/ament_prefix_path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/environment" TYPE FILE FILES "/opt/ros2/humble/install/ament_cmake_core/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/environment" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/local_setup.bash")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/local_setup.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/local_setup.zsh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/local_setup.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_environment_hooks/package.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_index/share/ament_index/resource_index/packages/image_publisher")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/rclcpp_components" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_index/share/ament_index/resource_index/rclcpp_components/image_publisher")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/cmake" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_export_dependencies/ament_cmake_export_dependencies-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/cmake" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_export_include_directories/ament_cmake_export_include_directories-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/cmake" TYPE FILE FILES "/home/olive/ros2_ws/build/image_publisher/ament_cmake_export_libraries/ament_cmake_export_libraries-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher/cmake" TYPE FILE FILES
    "/home/olive/ros2_ws/build/image_publisher/ament_cmake_core/image_publisherConfig.cmake"
    "/home/olive/ros2_ws/build/image_publisher/ament_cmake_core/image_publisherConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/image_publisher" TYPE FILE FILES "/home/olive/ros2_ws/src/image_publisher/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/olive/ros2_ws/build/image_publisher/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
