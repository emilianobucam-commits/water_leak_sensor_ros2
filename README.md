# water_leak_sensor_ros2
Simulacion de sensor de ague en un water enclosure

## Qué incluye

| Nodo | Rol | Topic que usa | Tipo de mensaje |
|---|---|---|---|
| `sensor_simulator_node` | Simula el sensor de filtración (publisher) | publica en `/water_sensor/raw_value` | `std_msgs/Int32` |
| `leak_detector_node` | Nodo central (`water_leak_detector`): se suscribe, interpreta la lectura y publica el resultado | se suscribe a `/water_sensor/raw_value` y publica en `/water_leak/status` | `std_msgs/Bool` |

Flujo de datos:sensor_simulator_node --(Int32, /water_sensor/raw_value)--> leak_detector_node (water_leak_detector) --(Bool, /water_leak/status)--> cualquier suscriptor

- `sensor_simulator_node` genera un entero aleatorio cada cierto periodo,
  simulando la lectura cruda de un sensor (por ejemplo, un ADC de 10 bits,
  0-1023). El parámetro `leak_probability` fuerza de vez en cuando lecturas
  altas para poder probar el sistema sin esperar al azar.
- `leak_detector_node` (nombre de nodo en ROS: **`water_leak_detector`**) se
  suscribe a esas lecturas y aplica un criterio numérico
  (`lectura >= leak_threshold`) para decidir si hay agua. Publica
  `True`/`False` en `/water_leak/status` cada vez que recibe una lectura, y
  deja un log (`warn`/`info`) cada vez que el estado cambia.

## Nodos y topics

| Nodo | Función | Topic | Tipo |
|---|---|---|---|
| `sensor_simulator_node` | Simula el sensor (publisher) | `/water_sensor/raw_value` | `std_msgs/Int32` |
| `leak_detector_node` (`water_leak_detector`) | Recibe la lectura, decide si hay fuga y publica el resultado | `/water_leak/status` | `std_msgs/Bool` |

Si la lectura es `>= leak_threshold` (default `700`), se publica `true`.

## Instalación

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select water_leak_detector
source install/setup.bash
```

## Ejecución

Terminal 1:
```bash
ros2 run water_leak_detector leak_detector_node
```

Terminal 2:
```bash
ros2 run water_leak_detector sensor_simulator_node
```

## Probar manualmente

```bash
ros2 topic pub --once /water_sensor/raw_value std_msgs/msg/Int32 "{data: 900}"
ros2 topic echo /water_leak/status
```

## Parámetros

- `leak_threshold` (default `700`) — umbral de detección.
- `publish_period_sec` (default `1.0`) — frecuencia del sensor simulado.
