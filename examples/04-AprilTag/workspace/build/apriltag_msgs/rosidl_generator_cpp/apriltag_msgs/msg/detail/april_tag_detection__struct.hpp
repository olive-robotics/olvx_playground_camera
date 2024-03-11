// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from apriltag_msgs:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_HPP_
#define APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'centre'
// Member 'corners'
#include "apriltag_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__apriltag_msgs__msg__AprilTagDetection __attribute__((deprecated))
#else
# define DEPRECATED__apriltag_msgs__msg__AprilTagDetection __declspec(deprecated)
#endif

namespace apriltag_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AprilTagDetection_
{
  using Type = AprilTagDetection_<ContainerAllocator>;

  explicit AprilTagDetection_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : centre(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->family = "";
      this->id = 0l;
      this->hamming = 0l;
      this->goodness = 0.0f;
      this->decision_margin = 0.0f;
      this->corners.fill(apriltag_msgs::msg::Point_<ContainerAllocator>{_init});
      std::fill<typename std::array<double, 9>::iterator, double>(this->homography.begin(), this->homography.end(), 0.0);
    }
  }

  explicit AprilTagDetection_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : family(_alloc),
    centre(_alloc, _init),
    corners(_alloc),
    homography(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->family = "";
      this->id = 0l;
      this->hamming = 0l;
      this->goodness = 0.0f;
      this->decision_margin = 0.0f;
      this->corners.fill(apriltag_msgs::msg::Point_<ContainerAllocator>{_alloc, _init});
      std::fill<typename std::array<double, 9>::iterator, double>(this->homography.begin(), this->homography.end(), 0.0);
    }
  }

  // field types and members
  using _family_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _family_type family;
  using _id_type =
    int32_t;
  _id_type id;
  using _hamming_type =
    int32_t;
  _hamming_type hamming;
  using _goodness_type =
    float;
  _goodness_type goodness;
  using _decision_margin_type =
    float;
  _decision_margin_type decision_margin;
  using _centre_type =
    apriltag_msgs::msg::Point_<ContainerAllocator>;
  _centre_type centre;
  using _corners_type =
    std::array<apriltag_msgs::msg::Point_<ContainerAllocator>, 4>;
  _corners_type corners;
  using _homography_type =
    std::array<double, 9>;
  _homography_type homography;

  // setters for named parameter idiom
  Type & set__family(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->family = _arg;
    return *this;
  }
  Type & set__id(
    const int32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__hamming(
    const int32_t & _arg)
  {
    this->hamming = _arg;
    return *this;
  }
  Type & set__goodness(
    const float & _arg)
  {
    this->goodness = _arg;
    return *this;
  }
  Type & set__decision_margin(
    const float & _arg)
  {
    this->decision_margin = _arg;
    return *this;
  }
  Type & set__centre(
    const apriltag_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->centre = _arg;
    return *this;
  }
  Type & set__corners(
    const std::array<apriltag_msgs::msg::Point_<ContainerAllocator>, 4> & _arg)
  {
    this->corners = _arg;
    return *this;
  }
  Type & set__homography(
    const std::array<double, 9> & _arg)
  {
    this->homography = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator> *;
  using ConstRawPtr =
    const apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__apriltag_msgs__msg__AprilTagDetection
    std::shared_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__apriltag_msgs__msg__AprilTagDetection
    std::shared_ptr<apriltag_msgs::msg::AprilTagDetection_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AprilTagDetection_ & other) const
  {
    if (this->family != other.family) {
      return false;
    }
    if (this->id != other.id) {
      return false;
    }
    if (this->hamming != other.hamming) {
      return false;
    }
    if (this->goodness != other.goodness) {
      return false;
    }
    if (this->decision_margin != other.decision_margin) {
      return false;
    }
    if (this->centre != other.centre) {
      return false;
    }
    if (this->corners != other.corners) {
      return false;
    }
    if (this->homography != other.homography) {
      return false;
    }
    return true;
  }
  bool operator!=(const AprilTagDetection_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AprilTagDetection_

// alias to use template instance with default allocator
using AprilTagDetection =
  apriltag_msgs::msg::AprilTagDetection_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace apriltag_msgs

#endif  // APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_HPP_
