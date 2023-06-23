// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from apriltag_msgs:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice
#include "apriltag_msgs/msg/detail/april_tag_detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `family`
#include "rosidl_runtime_c/string_functions.h"
// Member `centre`
// Member `corners`
#include "apriltag_msgs/msg/detail/point__functions.h"

bool
apriltag_msgs__msg__AprilTagDetection__init(apriltag_msgs__msg__AprilTagDetection * msg)
{
  if (!msg) {
    return false;
  }
  // family
  if (!rosidl_runtime_c__String__init(&msg->family)) {
    apriltag_msgs__msg__AprilTagDetection__fini(msg);
    return false;
  }
  // id
  // hamming
  // goodness
  // decision_margin
  // centre
  if (!apriltag_msgs__msg__Point__init(&msg->centre)) {
    apriltag_msgs__msg__AprilTagDetection__fini(msg);
    return false;
  }
  // corners
  for (size_t i = 0; i < 4; ++i) {
    if (!apriltag_msgs__msg__Point__init(&msg->corners[i])) {
      apriltag_msgs__msg__AprilTagDetection__fini(msg);
      return false;
    }
  }
  // homography
  return true;
}

void
apriltag_msgs__msg__AprilTagDetection__fini(apriltag_msgs__msg__AprilTagDetection * msg)
{
  if (!msg) {
    return;
  }
  // family
  rosidl_runtime_c__String__fini(&msg->family);
  // id
  // hamming
  // goodness
  // decision_margin
  // centre
  apriltag_msgs__msg__Point__fini(&msg->centre);
  // corners
  for (size_t i = 0; i < 4; ++i) {
    apriltag_msgs__msg__Point__fini(&msg->corners[i]);
  }
  // homography
}

bool
apriltag_msgs__msg__AprilTagDetection__are_equal(const apriltag_msgs__msg__AprilTagDetection * lhs, const apriltag_msgs__msg__AprilTagDetection * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // family
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->family), &(rhs->family)))
  {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // hamming
  if (lhs->hamming != rhs->hamming) {
    return false;
  }
  // goodness
  if (lhs->goodness != rhs->goodness) {
    return false;
  }
  // decision_margin
  if (lhs->decision_margin != rhs->decision_margin) {
    return false;
  }
  // centre
  if (!apriltag_msgs__msg__Point__are_equal(
      &(lhs->centre), &(rhs->centre)))
  {
    return false;
  }
  // corners
  for (size_t i = 0; i < 4; ++i) {
    if (!apriltag_msgs__msg__Point__are_equal(
        &(lhs->corners[i]), &(rhs->corners[i])))
    {
      return false;
    }
  }
  // homography
  for (size_t i = 0; i < 9; ++i) {
    if (lhs->homography[i] != rhs->homography[i]) {
      return false;
    }
  }
  return true;
}

bool
apriltag_msgs__msg__AprilTagDetection__copy(
  const apriltag_msgs__msg__AprilTagDetection * input,
  apriltag_msgs__msg__AprilTagDetection * output)
{
  if (!input || !output) {
    return false;
  }
  // family
  if (!rosidl_runtime_c__String__copy(
      &(input->family), &(output->family)))
  {
    return false;
  }
  // id
  output->id = input->id;
  // hamming
  output->hamming = input->hamming;
  // goodness
  output->goodness = input->goodness;
  // decision_margin
  output->decision_margin = input->decision_margin;
  // centre
  if (!apriltag_msgs__msg__Point__copy(
      &(input->centre), &(output->centre)))
  {
    return false;
  }
  // corners
  for (size_t i = 0; i < 4; ++i) {
    if (!apriltag_msgs__msg__Point__copy(
        &(input->corners[i]), &(output->corners[i])))
    {
      return false;
    }
  }
  // homography
  for (size_t i = 0; i < 9; ++i) {
    output->homography[i] = input->homography[i];
  }
  return true;
}

apriltag_msgs__msg__AprilTagDetection *
apriltag_msgs__msg__AprilTagDetection__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  apriltag_msgs__msg__AprilTagDetection * msg = (apriltag_msgs__msg__AprilTagDetection *)allocator.allocate(sizeof(apriltag_msgs__msg__AprilTagDetection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(apriltag_msgs__msg__AprilTagDetection));
  bool success = apriltag_msgs__msg__AprilTagDetection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
apriltag_msgs__msg__AprilTagDetection__destroy(apriltag_msgs__msg__AprilTagDetection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    apriltag_msgs__msg__AprilTagDetection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
apriltag_msgs__msg__AprilTagDetection__Sequence__init(apriltag_msgs__msg__AprilTagDetection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  apriltag_msgs__msg__AprilTagDetection * data = NULL;

  if (size) {
    data = (apriltag_msgs__msg__AprilTagDetection *)allocator.zero_allocate(size, sizeof(apriltag_msgs__msg__AprilTagDetection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = apriltag_msgs__msg__AprilTagDetection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        apriltag_msgs__msg__AprilTagDetection__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
apriltag_msgs__msg__AprilTagDetection__Sequence__fini(apriltag_msgs__msg__AprilTagDetection__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      apriltag_msgs__msg__AprilTagDetection__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

apriltag_msgs__msg__AprilTagDetection__Sequence *
apriltag_msgs__msg__AprilTagDetection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  apriltag_msgs__msg__AprilTagDetection__Sequence * array = (apriltag_msgs__msg__AprilTagDetection__Sequence *)allocator.allocate(sizeof(apriltag_msgs__msg__AprilTagDetection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = apriltag_msgs__msg__AprilTagDetection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
apriltag_msgs__msg__AprilTagDetection__Sequence__destroy(apriltag_msgs__msg__AprilTagDetection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    apriltag_msgs__msg__AprilTagDetection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
apriltag_msgs__msg__AprilTagDetection__Sequence__are_equal(const apriltag_msgs__msg__AprilTagDetection__Sequence * lhs, const apriltag_msgs__msg__AprilTagDetection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!apriltag_msgs__msg__AprilTagDetection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
apriltag_msgs__msg__AprilTagDetection__Sequence__copy(
  const apriltag_msgs__msg__AprilTagDetection__Sequence * input,
  apriltag_msgs__msg__AprilTagDetection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(apriltag_msgs__msg__AprilTagDetection);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    apriltag_msgs__msg__AprilTagDetection * data =
      (apriltag_msgs__msg__AprilTagDetection *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!apriltag_msgs__msg__AprilTagDetection__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          apriltag_msgs__msg__AprilTagDetection__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!apriltag_msgs__msg__AprilTagDetection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
