// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from apriltag_msgs:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__BUILDER_HPP_
#define APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "apriltag_msgs/msg/detail/april_tag_detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace apriltag_msgs
{

namespace msg
{

namespace builder
{

class Init_AprilTagDetection_homography
{
public:
  explicit Init_AprilTagDetection_homography(::apriltag_msgs::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  ::apriltag_msgs::msg::AprilTagDetection homography(::apriltag_msgs::msg::AprilTagDetection::_homography_type arg)
  {
    msg_.homography = std::move(arg);
    return std::move(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_corners
{
public:
  explicit Init_AprilTagDetection_corners(::apriltag_msgs::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_homography corners(::apriltag_msgs::msg::AprilTagDetection::_corners_type arg)
  {
    msg_.corners = std::move(arg);
    return Init_AprilTagDetection_homography(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_centre
{
public:
  explicit Init_AprilTagDetection_centre(::apriltag_msgs::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_corners centre(::apriltag_msgs::msg::AprilTagDetection::_centre_type arg)
  {
    msg_.centre = std::move(arg);
    return Init_AprilTagDetection_corners(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_decision_margin
{
public:
  explicit Init_AprilTagDetection_decision_margin(::apriltag_msgs::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_centre decision_margin(::apriltag_msgs::msg::AprilTagDetection::_decision_margin_type arg)
  {
    msg_.decision_margin = std::move(arg);
    return Init_AprilTagDetection_centre(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_goodness
{
public:
  explicit Init_AprilTagDetection_goodness(::apriltag_msgs::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_decision_margin goodness(::apriltag_msgs::msg::AprilTagDetection::_goodness_type arg)
  {
    msg_.goodness = std::move(arg);
    return Init_AprilTagDetection_decision_margin(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_hamming
{
public:
  explicit Init_AprilTagDetection_hamming(::apriltag_msgs::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_goodness hamming(::apriltag_msgs::msg::AprilTagDetection::_hamming_type arg)
  {
    msg_.hamming = std::move(arg);
    return Init_AprilTagDetection_goodness(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_id
{
public:
  explicit Init_AprilTagDetection_id(::apriltag_msgs::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_hamming id(::apriltag_msgs::msg::AprilTagDetection::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_AprilTagDetection_hamming(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_family
{
public:
  Init_AprilTagDetection_family()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AprilTagDetection_id family(::apriltag_msgs::msg::AprilTagDetection::_family_type arg)
  {
    msg_.family = std::move(arg);
    return Init_AprilTagDetection_id(msg_);
  }

private:
  ::apriltag_msgs::msg::AprilTagDetection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::apriltag_msgs::msg::AprilTagDetection>()
{
  return apriltag_msgs::msg::builder::Init_AprilTagDetection_family();
}

}  // namespace apriltag_msgs

#endif  // APRILTAG_MSGS__MSG__DETAIL__APRIL_TAG_DETECTION__BUILDER_HPP_
