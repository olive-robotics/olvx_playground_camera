// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from apriltag_msgs:msg/AprilTagDetectionArray.idl
// generated code does not contain a copyright notice
#include "apriltag_msgs/msg/detail/april_tag_detection_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `detections`
#include "apriltag_msgs/msg/detail/april_tag_detection__functions.h"

bool
apriltag_msgs__msg__AprilTagDetectionArray__init(apriltag_msgs__msg__AprilTagDetectionArray * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    apriltag_msgs__msg__AprilTagDetectionArray__fini(msg);
    return false;
  }
  // detections
  if (!apriltag_msgs__msg__AprilTagDetection__Sequence__init(&msg->detections, 0)) {
    apriltag_msgs__msg__AprilTagDetectionArray__fini(msg);
    return false;
  }
  return true;
}

void
apriltag_msgs__msg__AprilTagDetectionArray__fini(apriltag_msgs__msg__AprilTagDetectionArray * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // detections
  apriltag_msgs__msg__AprilTagDetection__Sequence__fini(&msg->detections);
}

bool
apriltag_msgs__msg__AprilTagDetectionArray__are_equal(const apriltag_msgs__msg__AprilTagDetectionArray * lhs, const apriltag_msgs__msg__AprilTagDetectionArray * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // detections
  if (!apriltag_msgs__msg__AprilTagDetection__Sequence__are_equal(
      &(lhs->detections), &(rhs->detections)))
  {
    return false;
  }
  return true;
}

bool
apriltag_msgs__msg__AprilTagDetectionArray__copy(
  const apriltag_msgs__msg__AprilTagDetectionArray * input,
  apriltag_msgs__msg__AprilTagDetectionArray * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // detections
  if (!apriltag_msgs__msg__AprilTagDetection__Sequence__copy(
      &(input->detections), &(output->detections)))
  {
    return false;
  }
  return true;
}

apriltag_msgs__msg__AprilTagDetectionArray *
apriltag_msgs__msg__AprilTagDetectionArray__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  apriltag_msgs__msg__AprilTagDetectionArray * msg = (apriltag_msgs__msg__AprilTagDetectionArray *)allocator.allocate(sizeof(apriltag_msgs__msg__AprilTagDetectionArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(apriltag_msgs__msg__AprilTagDetectionArray));
  bool success = apriltag_msgs__msg__AprilTagDetectionArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
apriltag_msgs__msg__AprilTagDetectionArray__destroy(apriltag_msgs__msg__AprilTagDetectionArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    apriltag_msgs__msg__AprilTagDetectionArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
apriltag_msgs__msg__AprilTagDetectionArray__Sequence__init(apriltag_msgs__msg__AprilTagDetectionArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  apriltag_msgs__msg__AprilTagDetectionArray * data = NULL;

  if (size) {
    data = (apriltag_msgs__msg__AprilTagDetectionArray *)allocator.zero_allocate(size, sizeof(apriltag_msgs__msg__AprilTagDetectionArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = apriltag_msgs__msg__AprilTagDetectionArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        apriltag_msgs__msg__AprilTagDetectionArray__fini(&data[i - 1]);
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
apriltag_msgs__msg__AprilTagDetectionArray__Sequence__fini(apriltag_msgs__msg__AprilTagDetectionArray__Sequence * array)
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
      apriltag_msgs__msg__AprilTagDetectionArray__fini(&array->data[i]);
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

apriltag_msgs__msg__AprilTagDetectionArray__Sequence *
apriltag_msgs__msg__AprilTagDetectionArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  apriltag_msgs__msg__AprilTagDetectionArray__Sequence * array = (apriltag_msgs__msg__AprilTagDetectionArray__Sequence *)allocator.allocate(sizeof(apriltag_msgs__msg__AprilTagDetectionArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = apriltag_msgs__msg__AprilTagDetectionArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
apriltag_msgs__msg__AprilTagDetectionArray__Sequence__destroy(apriltag_msgs__msg__AprilTagDetectionArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    apriltag_msgs__msg__AprilTagDetectionArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
apriltag_msgs__msg__AprilTagDetectionArray__Sequence__are_equal(const apriltag_msgs__msg__AprilTagDetectionArray__Sequence * lhs, const apriltag_msgs__msg__AprilTagDetectionArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!apriltag_msgs__msg__AprilTagDetectionArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
apriltag_msgs__msg__AprilTagDetectionArray__Sequence__copy(
  const apriltag_msgs__msg__AprilTagDetectionArray__Sequence * input,
  apriltag_msgs__msg__AprilTagDetectionArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(apriltag_msgs__msg__AprilTagDetectionArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    apriltag_msgs__msg__AprilTagDetectionArray * data =
      (apriltag_msgs__msg__AprilTagDetectionArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!apriltag_msgs__msg__AprilTagDetectionArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          apriltag_msgs__msg__AprilTagDetectionArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!apriltag_msgs__msg__AprilTagDetectionArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
