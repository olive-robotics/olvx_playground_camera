# Install script for directory: /home/olive/workspace2/src/apriltag_detector

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/olive/workspace2/install/apriltag_detector")
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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/environment" TYPE FILE FILES "/opt/ros2/humble/build/ament_package/ament_package/template/environment_hook/library_path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/environment" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/library_path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector/apriltag_detector_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector/apriltag_detector_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector/apriltag_detector_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector" TYPE EXECUTABLE FILES "/home/olive/workspace2/build/apriltag_detector/apriltag_detector_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector/apriltag_detector_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector/apriltag_detector_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector/apriltag_detector_node"
         OLD_RPATH "/home/olive/workspace2/build/apriltag_detector:/opt/ros2/humble/install/rclcpp_components/lib:/opt/ros2/humble/install/class_loader/lib:/opt/ros2/humble/install/console_bridge_vendor/lib:/opt/ros2/humble/install/composition_interfaces/lib:/opt/ros2/humble/install/image_transport/lib:/opt/ros2/humble/install/message_filters/lib:/opt/ros2/humble/install/rclcpp/lib:/opt/ros2/humble/install/libstatistics_collector/lib:/opt/ros2/humble/install/rcl/lib:/opt/ros2/humble/install/rmw_implementation/lib:/opt/ros2/humble/install/ament_index_cpp/lib:/opt/ros2/humble/install/rcl_logging_spdlog/lib:/opt/ros2/humble/install/rcl_logging_interface/lib:/opt/ros2/humble/install/rcl_interfaces/lib:/opt/ros2/humble/install/rcl_yaml_param_parser/lib:/opt/ros2/humble/install/libyaml_vendor/lib:/opt/ros2/humble/install/rosgraph_msgs/lib:/opt/ros2/humble/install/statistics_msgs/lib:/opt/ros2/humble/install/tracetools/lib:/home/olive/workspace2/install/cv_bridge/lib:/home/olive/opencv_install/opencv-4.x/build/lib:/opt/ros2/humble/install/sensor_msgs/lib:/opt/ros2/humble/install/geometry_msgs/lib:/home/olive/workspace2/install/apriltag_msgs/lib:/opt/ros2/humble/install/std_msgs/lib:/opt/ros2/humble/install/builtin_interfaces/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_c/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_c/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_cpp/lib:/opt/ros2/humble/install/fastcdr/lib:/opt/ros2/humble/install/rmw/lib:/opt/ros2/humble/install/rosidl_typesupport_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_c/lib:/opt/ros2/humble/install/rcpputils/lib:/opt/ros2/humble/install/rosidl_runtime_c/lib:/opt/ros2/humble/install/rcutils/lib:/usr/local/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/apriltag_detector/apriltag_detector_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdetector_wrapper.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdetector_wrapper.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdetector_wrapper.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/olive/workspace2/build/apriltag_detector/libdetector_wrapper.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdetector_wrapper.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdetector_wrapper.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdetector_wrapper.so"
         OLD_RPATH "/opt/ros2/humble/install/rclcpp_components/lib:/opt/ros2/humble/install/image_transport/lib:/home/olive/workspace2/install/cv_bridge/lib:/opt/ros2/humble/install/sensor_msgs/lib:/home/olive/workspace2/install/apriltag_msgs/lib:/usr/local/lib:/opt/ros2/humble/install/class_loader/lib:/opt/ros2/humble/install/console_bridge_vendor/lib:/opt/ros2/humble/install/composition_interfaces/lib:/opt/ros2/humble/install/message_filters/lib:/opt/ros2/humble/install/rclcpp/lib:/opt/ros2/humble/install/libstatistics_collector/lib:/opt/ros2/humble/install/rcl/lib:/opt/ros2/humble/install/rmw_implementation/lib:/opt/ros2/humble/install/ament_index_cpp/lib:/opt/ros2/humble/install/rcl_logging_spdlog/lib:/opt/ros2/humble/install/rcl_logging_interface/lib:/opt/ros2/humble/install/rcl_interfaces/lib:/opt/ros2/humble/install/rcl_yaml_param_parser/lib:/opt/ros2/humble/install/libyaml_vendor/lib:/opt/ros2/humble/install/rosgraph_msgs/lib:/opt/ros2/humble/install/statistics_msgs/lib:/opt/ros2/humble/install/tracetools/lib:/opt/ros2/humble/install/geometry_msgs/lib:/home/olive/opencv_install/opencv-4.x/build/lib:/opt/ros2/humble/install/std_msgs/lib:/opt/ros2/humble/install/builtin_interfaces/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_c/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_c/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_cpp/lib:/opt/ros2/humble/install/fastcdr/lib:/opt/ros2/humble/install/rmw/lib:/opt/ros2/humble/install/rosidl_typesupport_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_c/lib:/opt/ros2/humble/install/rcpputils/lib:/opt/ros2/humble/install/rosidl_runtime_c/lib:/opt/ros2/humble/install/rcutils/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdetector_wrapper.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libapriltag_detector.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libapriltag_detector.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libapriltag_detector.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/olive/workspace2/build/apriltag_detector/libapriltag_detector.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libapriltag_detector.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libapriltag_detector.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libapriltag_detector.so"
         OLD_RPATH "/home/olive/workspace2/build/apriltag_detector:/opt/ros2/humble/install/rclcpp_components/lib:/opt/ros2/humble/install/class_loader/lib:/opt/ros2/humble/install/console_bridge_vendor/lib:/opt/ros2/humble/install/composition_interfaces/lib:/opt/ros2/humble/install/image_transport/lib:/opt/ros2/humble/install/message_filters/lib:/opt/ros2/humble/install/rclcpp/lib:/opt/ros2/humble/install/libstatistics_collector/lib:/opt/ros2/humble/install/rcl/lib:/opt/ros2/humble/install/rmw_implementation/lib:/opt/ros2/humble/install/ament_index_cpp/lib:/opt/ros2/humble/install/rcl_logging_spdlog/lib:/opt/ros2/humble/install/rcl_logging_interface/lib:/opt/ros2/humble/install/rcl_interfaces/lib:/opt/ros2/humble/install/rcl_yaml_param_parser/lib:/opt/ros2/humble/install/libyaml_vendor/lib:/opt/ros2/humble/install/rosgraph_msgs/lib:/opt/ros2/humble/install/statistics_msgs/lib:/opt/ros2/humble/install/tracetools/lib:/home/olive/workspace2/install/cv_bridge/lib:/home/olive/opencv_install/opencv-4.x/build/lib:/opt/ros2/humble/install/sensor_msgs/lib:/opt/ros2/humble/install/geometry_msgs/lib:/home/olive/workspace2/install/apriltag_msgs/lib:/opt/ros2/humble/install/std_msgs/lib:/opt/ros2/humble/install/builtin_interfaces/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_c/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_introspection_c/lib:/opt/ros2/humble/install/rosidl_typesupport_fastrtps_cpp/lib:/opt/ros2/humble/install/fastcdr/lib:/opt/ros2/humble/install/rmw/lib:/opt/ros2/humble/install/rosidl_typesupport_cpp/lib:/opt/ros2/humble/install/rosidl_typesupport_c/lib:/opt/ros2/humble/install/rcpputils/lib:/opt/ros2/humble/install/rosidl_runtime_c/lib:/opt/ros2/humble/install/rcutils/lib:/usr/local/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libapriltag_detector.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/olive/workspace2/src/apriltag_detector/include/" FILES_MATCHING REGEX "/detector\\_wrapper[^/]*\\.hpp$" REGEX "/detector\\_wrapper\\_ros1\\.hpp$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/" TYPE DIRECTORY FILES "/home/olive/workspace2/src/apriltag_detector/launch" FILES_MATCHING REGEX "/[^/]*\\.py$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/package_run_dependencies" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/apriltag_detector")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/parent_prefix_path" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/apriltag_detector")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/environment" TYPE FILE FILES "/opt/ros2/humble/install/ament_cmake_core/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/environment" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/ament_prefix_path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/environment" TYPE FILE FILES "/opt/ros2/humble/install/ament_cmake_core/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/environment" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/local_setup.bash")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/local_setup.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/local_setup.zsh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/local_setup.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_environment_hooks/package.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_index/share/ament_index/resource_index/packages/apriltag_detector")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake/apriltag_detector_exportExport.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake/apriltag_detector_exportExport.cmake"
         "/home/olive/workspace2/build/apriltag_detector/CMakeFiles/Export/share/apriltag_detector/cmake/apriltag_detector_exportExport.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake/apriltag_detector_exportExport-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake/apriltag_detector_exportExport.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/CMakeFiles/Export/share/apriltag_detector/cmake/apriltag_detector_exportExport.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/CMakeFiles/Export/share/apriltag_detector/cmake/apriltag_detector_exportExport-noconfig.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/rclcpp_components" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_index/share/ament_index/resource_index/rclcpp_components/apriltag_detector")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_export_targets/ament_cmake_export_targets-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake" TYPE FILE FILES "/home/olive/workspace2/build/apriltag_detector/ament_cmake_export_dependencies/ament_cmake_export_dependencies-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector/cmake" TYPE FILE FILES
    "/home/olive/workspace2/build/apriltag_detector/ament_cmake_core/apriltag_detectorConfig.cmake"
    "/home/olive/workspace2/build/apriltag_detector/ament_cmake_core/apriltag_detectorConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apriltag_detector" TYPE FILE FILES "/home/olive/workspace2/src/apriltag_detector/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/olive/workspace2/build/apriltag_detector/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
