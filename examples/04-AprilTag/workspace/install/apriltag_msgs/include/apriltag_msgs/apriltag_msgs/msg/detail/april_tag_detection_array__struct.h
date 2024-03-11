// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from apriltag_msgs:msg/AprilTagDetectionArray.idl
// generated code does not contain a copyright notice

#ifndef APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_H_
#define APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'detections'
#include "apriltag_msgs/msg/detail/april_tag_detection__struct.h"

/// Struct defined in msg/AprilTagDetectionArray in the package apriltag_msgs.
typedef struct apriltag_msgs__msg__AprilTagDetectionArray
{
  std_msgs__msg__Header header;
  apriltag_msgs__msg__AprilTagDetection__Sequence detections;
} apriltag_msgs__msg__AprilTagDetectionArray;

// Struct for a sequence of apriltag_msgs__msg__AprilTagDetectionArray.
typedef struct apriltag_msgs__msg__AprilTagDetectionArray__Sequence
{
  apriltag_msgs__msg__AprilTagDetectionArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} apriltag_msgs__msg__AprilTagDetectionArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_H_
