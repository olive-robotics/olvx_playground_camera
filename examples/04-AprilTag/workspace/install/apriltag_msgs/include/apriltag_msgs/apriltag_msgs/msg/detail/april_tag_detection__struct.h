// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from apriltag_msgs:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_H_
#define APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'family'
#include "rosidl_runtime_c/string.h"
// Member 'centre'
// Member 'corners'
#include "apriltag_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/AprilTagDetection in the package apriltag_msgs.
typedef struct apriltag_msgs__msg__AprilTagDetection
{
  rosidl_runtime_c__String family;
  int32_t id;
  int32_t hamming;
  float goodness;
  float decision_margin;
  /// centre in (x,y) pixel coordinates
  apriltag_msgs__msg__Point centre;
  /// corners of tag ((x1,y1),(x2,y2),...)
  apriltag_msgs__msg__Point corners[4];
  /// 3x3 row-major homography matrix
  double homography[9];
} apriltag_msgs__msg__AprilTagDetection;

// Struct for a sequence of apriltag_msgs__msg__AprilTagDetection.
typedef struct apriltag_msgs__msg__AprilTagDetection__Sequence
{
  apriltag_msgs__msg__AprilTagDetection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} apriltag_msgs__msg__AprilTagDetection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_H_
