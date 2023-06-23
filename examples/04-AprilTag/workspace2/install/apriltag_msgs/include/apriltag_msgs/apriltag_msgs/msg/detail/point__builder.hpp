// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from apriltag_msgs:msg/Point.idl
// generated code does not contain a copyright notice

#ifndef APRILTAG_MSGS__MSG__DETAIL__POINT__BUILDER_HPP_
#define APRILTAG_MSGS__MSG__DETAIL__POINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "apriltag_msgs/msg/detail/point__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace apriltag_msgs
{

namespace msg
{

namespace builder
{

class Init_Point_y
{
public:
  explicit Init_Point_y(::apriltag_msgs::msg::Point & msg)
  : msg_(msg)
  {}
  ::apriltag_msgs::msg::Point y(::apriltag_msgs::msg::Point::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::apriltag_msgs::msg::Point msg_;
};

class Init_Point_x
{
public:
  Init_Point_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Point_y x(::apriltag_msgs::msg::Point::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Point_y(msg_);
  }

private:
  ::apriltag_msgs::msg::Point msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::apriltag_msgs::msg::Point>()
{
  return apriltag_msgs::msg::builder::Init_Point_x();
}

}  // namespace apriltag_msgs

#endif  // APRILTAG_MSGS__MSG__DETAIL__POINT__BUILDER_HPP_
