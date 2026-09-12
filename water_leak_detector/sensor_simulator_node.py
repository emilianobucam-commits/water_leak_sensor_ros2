import random
import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class SensorSimulatorNode(Node):

    def __init__(self):
        super().__init__('water_sensor_simulator')

        self.declare_parameter('publish_period_sec', 1.0)
        self.declare_parameter('min_reading', 0)
        self.declare_parameter('max_reading', 1023)
        self.declare_parameter('leak_probability', 0.2)

        self._publisher = self.create_publisher(
            Int32, 'water_sensor/raw_value', 10)

        period = self.get_parameter('publish_period_sec').value
        self._timer = self.create_timer(period, self._timer_callback)

        self.get_logger().info(
            "Sensor simulador iniciado. Publicando en "
            "'water_sensor/raw_value' cada %.2f s." % period
        )

    def _timer_callback(self):
        min_reading = self.get_parameter('min_reading').value
        max_reading = self.get_parameter('max_reading').value
        leak_probability = self.get_parameter('leak_probability').value

        # Rango alto: agua presente; rango bajo: enclosure seco.
        high_range_start = int((min_reading + max_reading) * 0.7)

        if random.random() < leak_probability:
            reading = random.randint(high_range_start, max_reading)
        else:
            reading = random.randint(min_reading, high_range_start - 1)

        msg = Int32()
        msg.data = reading
        self._publisher.publish(msg)
        self.get_logger().debug('Lectura simulada publicada: %d' % reading)


def main(args=None):
    rclpy.init(args=args)
    node = SensorSimulatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()