#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "apriltag_detector::detector_wrapper" for configuration ""
set_property(TARGET apriltag_detector::detector_wrapper APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(apriltag_detector::detector_wrapper PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libdetector_wrapper.so"
  IMPORTED_SONAME_NOCONFIG "libdetector_wrapper.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS apriltag_detector::detector_wrapper )
list(APPEND _IMPORT_CHECK_FILES_FOR_apriltag_detector::detector_wrapper "${_IMPORT_PREFIX}/lib/libdetector_wrapper.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
