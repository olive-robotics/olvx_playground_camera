// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from apriltag_msgs:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "apriltag_msgs/msg/detail/april_tag_detection__rosidl_typesupport_introspection_c.h"
#include "apriltag_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "apriltag_msgs/msg/detail/april_tag_detection__functions.h"
#include "apriltag_msgs/msg/detail/april_tag_detection__struct.h"


// Include directives for member types
// Member `family`
#include "rosidl_runtime_c/string_functions.h"
// Member `centre`
// Member `corners`
#include "apriltag_msgs/msg/point.h"
// Member `centre`
// Member `corners`
#include "apriltag_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  apriltag_msgs__msg__AprilTagDetection__init(message_memory);
}

void apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_fini_function(void * message_memory)
{
  apriltag_msgs__msg__AprilTagDetection__fini(message_memory);
}

size_t apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__size_function__AprilTagDetection__corners(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__corners(
  const void * untyped_member, size_t index)
{
  const apriltag_msgs__msg__Point * member =
    (const apriltag_msgs__msg__Point *)(untyped_member);
  return &member[index];
}

void * apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__corners(
  void * untyped_member, size_t index)
{
  apriltag_msgs__msg__Point * member =
    (apriltag_msgs__msg__Point *)(untyped_member);
  return &member[index];
}

void apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__fetch_function__AprilTagDetection__corners(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const apriltag_msgs__msg__Point * item =
    ((const apriltag_msgs__msg__Point *)
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__corners(untyped_member, index));
  apriltag_msgs__msg__Point * value =
    (apriltag_msgs__msg__Point *)(untyped_value);
  *value = *item;
}

void apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__assign_function__AprilTagDetection__corners(
  void * untyped_member, size_t index, const void * untyped_value)
{
  apriltag_msgs__msg__Point * item =
    ((apriltag_msgs__msg__Point *)
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__corners(untyped_member, index));
  const apriltag_msgs__msg__Point * value =
    (const apriltag_msgs__msg__Point *)(untyped_value);
  *item = *value;
}

size_t apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__size_function__AprilTagDetection__homography(
  const void * untyped_member)
{
  (void)untyped_member;
  return 9;
}

const void * apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__homography(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__homography(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__fetch_function__AprilTagDetection__homography(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__homography(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__assign_function__AprilTagDetection__homography(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__homography(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array[8] = {
  {
    "family",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, family),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "hamming",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, hamming),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "goodness",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, goodness),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "decision_margin",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, decision_margin),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "centre",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, centre),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "corners",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, corners),  // bytes offset in struct
    NULL,  // default value
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__size_function__AprilTagDetection__corners,  // size() function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__corners,  // get_const(index) function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__corners,  // get(index) function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__fetch_function__AprilTagDetection__corners,  // fetch(index, &value) function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__assign_function__AprilTagDetection__corners,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "homography",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    9,  // array size
    false,  // is upper bound
    offsetof(apriltag_msgs__msg__AprilTagDetection, homography),  // bytes offset in struct
    NULL,  // default value
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__size_function__AprilTagDetection__homography,  // size() function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__homography,  // get_const(index) function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__homography,  // get(index) function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__fetch_function__AprilTagDetection__homography,  // fetch(index, &value) function pointer
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__assign_function__AprilTagDetection__homography,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_members = {
  "apriltag_msgs__msg",  // message namespace
  "AprilTagDetection",  // message name
  8,  // number of fields
  sizeof(apriltag_msgs__msg__AprilTagDetection),
  apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array,  // message members
  apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_init_function,  // function to initialize message memory (memory has to be allocated)
  apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle = {
  0,
  &apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_apriltag_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, apriltag_msgs, msg, AprilTagDetection)() {
  apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, apriltag_msgs, msg, Point)();
  apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array[6].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, apriltag_msgs, msg, Point)();
  if (!apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle.typesupport_identifier) {
    apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &apriltag_msgs__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
