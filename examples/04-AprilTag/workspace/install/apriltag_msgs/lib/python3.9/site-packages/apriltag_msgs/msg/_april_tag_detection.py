# generated from rosidl_generator_py/resource/_idl.py.em
# with input from apriltag_msgs:msg/AprilTagDetection.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

# Member 'homography'
import numpy  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_AprilTagDetection(type):
    """Metaclass of message 'AprilTagDetection'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('apriltag_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'apriltag_msgs.msg.AprilTagDetection')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__april_tag_detection
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__april_tag_detection
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__april_tag_detection
            cls._TYPE_SUPPORT = module.type_support_msg__msg__april_tag_detection
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__april_tag_detection

            from apriltag_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class AprilTagDetection(metaclass=Metaclass_AprilTagDetection):
    """Message class 'AprilTagDetection'."""

    __slots__ = [
        '_family',
        '_id',
        '_hamming',
        '_goodness',
        '_decision_margin',
        '_centre',
        '_corners',
        '_homography',
    ]

    _fields_and_field_types = {
        'family': 'string',
        'id': 'int32',
        'hamming': 'int32',
        'goodness': 'float',
        'decision_margin': 'float',
        'centre': 'apriltag_msgs/Point',
        'corners': 'apriltag_msgs/Point[4]',
        'homography': 'double[9]',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['apriltag_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.NamespacedType(['apriltag_msgs', 'msg'], 'Point'), 4),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 9),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.family = kwargs.get('family', str())
        self.id = kwargs.get('id', int())
        self.hamming = kwargs.get('hamming', int())
        self.goodness = kwargs.get('goodness', float())
        self.decision_margin = kwargs.get('decision_margin', float())
        from apriltag_msgs.msg import Point
        self.centre = kwargs.get('centre', Point())
        from apriltag_msgs.msg import Point
        self.corners = kwargs.get(
            'corners',
            [Point() for x in range(4)]
        )
        if 'homography' not in kwargs:
            self.homography = numpy.zeros(9, dtype=numpy.float64)
        else:
            self.homography = numpy.array(kwargs.get('homography'), dtype=numpy.float64)
            assert self.homography.shape == (9, )

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.family != other.family:
            return False
        if self.id != other.id:
            return False
        if self.hamming != other.hamming:
            return False
        if self.goodness != other.goodness:
            return False
        if self.decision_margin != other.decision_margin:
            return False
        if self.centre != other.centre:
            return False
        if self.corners != other.corners:
            return False
        if all(self.homography != other.homography):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def family(self):
        """Message field 'family'."""
        return self._family

    @family.setter
    def family(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'family' field must be of type 'str'"
        self._family = value

    @builtins.property  # noqa: A003
    def id(self):  # noqa: A003
        """Message field 'id'."""
        return self._id

    @id.setter  # noqa: A003
    def id(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'id' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'id' field must be an integer in [-2147483648, 2147483647]"
        self._id = value

    @builtins.property
    def hamming(self):
        """Message field 'hamming'."""
        return self._hamming

    @hamming.setter
    def hamming(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'hamming' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'hamming' field must be an integer in [-2147483648, 2147483647]"
        self._hamming = value

    @builtins.property
    def goodness(self):
        """Message field 'goodness'."""
        return self._goodness

    @goodness.setter
    def goodness(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'goodness' field must be of type 'float'"
            assert value >= -3.402823e+38 and value <= 3.402823e+38, \
                "The 'goodness' field must be a float in [-3.402823e+38, 3.402823e+38]"
        self._goodness = value

    @builtins.property
    def decision_margin(self):
        """Message field 'decision_margin'."""
        return self._decision_margin

    @decision_margin.setter
    def decision_margin(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'decision_margin' field must be of type 'float'"
            assert value >= -3.402823e+38 and value <= 3.402823e+38, \
                "The 'decision_margin' field must be a float in [-3.402823e+38, 3.402823e+38]"
        self._decision_margin = value

    @builtins.property
    def centre(self):
        """Message field 'centre'."""
        return self._centre

    @centre.setter
    def centre(self, value):
        if __debug__:
            from apriltag_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'centre' field must be a sub message of type 'Point'"
        self._centre = value

    @builtins.property
    def corners(self):
        """Message field 'corners'."""
        return self._corners

    @corners.setter
    def corners(self, value):
        if __debug__:
            from apriltag_msgs.msg import Point
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 4 and
                 all(isinstance(v, Point) for v in value) and
                 True), \
                "The 'corners' field must be a set or sequence with length 4 and each value of type 'Point'"
        self._corners = value

    @builtins.property
    def homography(self):
        """Message field 'homography'."""
        return self._homography

    @homography.setter
    def homography(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float64, \
                "The 'homography' numpy.ndarray() must have the dtype of 'numpy.float64'"
            assert value.size == 9, \
                "The 'homography' numpy.ndarray() must have a size of 9"
            self._homography = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 9 and
                 all(isinstance(v, float) for v in value) and
                 all(val >= -1.7976931348623157e+308 and val <= 1.7976931348623157e+308 for val in value)), \
                "The 'homography' field must be a set or sequence with length 9 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._homography = numpy.array(value, dtype=numpy.float64)
