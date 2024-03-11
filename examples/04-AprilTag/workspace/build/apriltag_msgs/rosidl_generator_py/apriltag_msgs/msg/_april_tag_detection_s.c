// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from apriltag_msgs:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "apriltag_msgs/msg/detail/april_tag_detection__struct.h"
#include "apriltag_msgs/msg/detail/april_tag_detection__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes
#include "apriltag_msgs/msg/detail/point__functions.h"
// end nested array functions include
bool apriltag_msgs__msg__point__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * apriltag_msgs__msg__point__convert_to_py(void * raw_ros_message);
bool apriltag_msgs__msg__point__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * apriltag_msgs__msg__point__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool apriltag_msgs__msg__april_tag_detection__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[57];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("apriltag_msgs.msg._april_tag_detection.AprilTagDetection", full_classname_dest, 56) == 0);
  }
  apriltag_msgs__msg__AprilTagDetection * ros_message = _ros_message;
  {  // family
    PyObject * field = PyObject_GetAttrString(_pymsg, "family");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->family, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // id
    PyObject * field = PyObject_GetAttrString(_pymsg, "id");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->id = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // hamming
    PyObject * field = PyObject_GetAttrString(_pymsg, "hamming");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->hamming = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // goodness
    PyObject * field = PyObject_GetAttrString(_pymsg, "goodness");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->goodness = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // decision_margin
    PyObject * field = PyObject_GetAttrString(_pymsg, "decision_margin");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->decision_margin = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // centre
    PyObject * field = PyObject_GetAttrString(_pymsg, "centre");
    if (!field) {
      return false;
    }
    if (!apriltag_msgs__msg__point__convert_from_py(field, &ros_message->centre)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // corners
    PyObject * field = PyObject_GetAttrString(_pymsg, "corners");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'corners'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = 4;
    apriltag_msgs__msg__Point * dest = ros_message->corners;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!apriltag_msgs__msg__point__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // homography
    PyObject * field = PyObject_GetAttrString(_pymsg, "homography");
    if (!field) {
      return false;
    }
    {
      // TODO(dirk-thomas) use a better way to check the type before casting
      assert(field->ob_type != NULL);
      assert(field->ob_type->tp_name != NULL);
      assert(strcmp(field->ob_type->tp_name, "numpy.ndarray") == 0);
      PyArrayObject * seq_field = (PyArrayObject *)field;
      Py_INCREF(seq_field);
      assert(PyArray_NDIM(seq_field) == 1);
      assert(PyArray_TYPE(seq_field) == NPY_FLOAT64);
      Py_ssize_t size = 9;
      double * dest = ros_message->homography;
      for (Py_ssize_t i = 0; i < size; ++i) {
        double tmp = *(npy_float64 *)PyArray_GETPTR1(seq_field, i);
        memcpy(&dest[i], &tmp, sizeof(double));
      }
      Py_DECREF(seq_field);
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * apriltag_msgs__msg__april_tag_detection__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of AprilTagDetection */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("apriltag_msgs.msg._april_tag_detection");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "AprilTagDetection");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  apriltag_msgs__msg__AprilTagDetection * ros_message = (apriltag_msgs__msg__AprilTagDetection *)raw_ros_message;
  {  // family
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->family.data,
      strlen(ros_message->family.data),
      "strict");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "family", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // id
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->id);
    {
      int rc = PyObject_SetAttrString(_pymessage, "id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // hamming
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->hamming);
    {
      int rc = PyObject_SetAttrString(_pymessage, "hamming", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // goodness
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->goodness);
    {
      int rc = PyObject_SetAttrString(_pymessage, "goodness", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // decision_margin
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->decision_margin);
    {
      int rc = PyObject_SetAttrString(_pymessage, "decision_margin", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // centre
    PyObject * field = NULL;
    field = apriltag_msgs__msg__point__convert_to_py(&ros_message->centre);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "centre", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // corners
    PyObject * field = NULL;
    size_t size = 4;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    apriltag_msgs__msg__Point * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->corners[i]);
      PyObject * pyitem = apriltag_msgs__msg__point__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "corners", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // homography
    PyObject * field = NULL;
    field = PyObject_GetAttrString(_pymessage, "homography");
    if (!field) {
      return NULL;
    }
    assert(field->ob_type != NULL);
    assert(field->ob_type->tp_name != NULL);
    assert(strcmp(field->ob_type->tp_name, "numpy.ndarray") == 0);
    PyArrayObject * seq_field = (PyArrayObject *)field;
    assert(PyArray_NDIM(seq_field) == 1);
    assert(PyArray_TYPE(seq_field) == NPY_FLOAT64);
    assert(sizeof(npy_float64) == sizeof(double));
    npy_float64 * dst = (npy_float64 *)PyArray_GETPTR1(seq_field, 0);
    double * src = &(ros_message->homography[0]);
    memcpy(dst, src, 9 * sizeof(double));
    Py_DECREF(field);
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
