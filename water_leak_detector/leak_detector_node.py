import rclpy
import sys
from rclpy.node import Node
from std_msgs.msg import Bool, Int32


class LeakDetectorNode(Node):

    def __init__(self):
        # Nombre del nodo
        super().__init__('water_leak_detector')

        # A partir de este valor se considera que hay agua.
        self.declare_parameter('leak_threshold', 700)

        # Subscriber: escucha las lecturas del sensor.
        self._subscription = self.create_subscription(
            Int32,
            'water_sensor/raw_value',
            self._sensor_callback,
            10,
        )

        # Publica el resultado (True/False).
        self._publisher = self.create_publisher(
            Bool, 'water_leak/status', 10)

        self._last_state = None  # para solo loguear cuando cambia el estado

        threshold = self.get_parameter('leak_threshold').value
        self.get_logger().info(
            "water_leak_detector iniciado. Umbral de fuga = %d" % threshold
        )

    def _sensor_callback(self, msg: Int32) -> None:
        threshold = self.get_parameter('leak_threshold').value

        # Si la lectura es >= umbral, hay agua.
        leak_present = msg.data >= threshold

        result = Bool()
        result.data = leak_present
        self._publisher.publish(result)

        if leak_present != self._last_state:
            if leak_present:
                self.get_logger().warn(
                    'FUGA DETECTADA. Lectura=%d >= umbral=%d'
                    % (msg.data, threshold)
                )
            else:
                self.get_logger().info(
                    'Enclosure seco. Lectura=%d < umbral=%d'
                    % (msg.data, threshold)
                )
            self._last_state = leak_present


def main(args=None):
    rclpy.init(args=args)
    node = LeakDetectorNode()
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