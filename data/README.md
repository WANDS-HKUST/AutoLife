# Sensor File Details
After unzipping the sensor data into this folder, you will find multiple experiment folders (e.g., `j240322`), each representing a single experiment. Inside each experiment folder, sensor data is organized into **data collection sessions**.

A **data collection session** is a fixed time window during which all available sensors are sampled and recorded. Each session folder is named by its **collection start time** in the format `HH_MM_SS`.

## Setup

All data were collected using Android smartphones. In this dataset, each session is configured as follows:

- **Session duration:** 15 seconds  
- **Session interval:** A new session is triggered every 1 minute  

This setup strikes a balance between **sensing coverage** and **system overhead**, enabling continuous long-term monitoring while minimizing battery drain and resource usage.

> **Note:** Due to system constraints, some sensors may not record data if the device is idle or restricted by the OS. In such cases, the corresponding CSV files may be empty.

## Sensors

Each session directory contains **18 data files**, including:

- **11 physical sensor files** (e.g., accelerometer, location, WiFi)  
- **6 virtual sensor files** (derived from other sensors, e.g., rotation, step counter)  
- **1 meta file** describing session-level information


Here is a summary of the sensors:

| Category | Sensor File                                          | Short Description |
|----------|------------------------------------------------------|-----------------|
| **Physical Sensors** | [Accelerometer.csv](#accelerometercsv)               | Measures device acceleration along X, Y, Z axes |
|  | [Gyroscope.csv](#gyroscopecsv)                       | Measures device angular velocity along X, Y, Z axes |
|  | [Magnetometer.csv](#magnetometercsv)                 | Measures ambient magnetic field along X, Y, Z axes |
|  | [Proximity.csv](#proximitycsv)                       | Detects distance to nearby objects |
|  | [Light.csv](#lightcsv)                               | Measures ambient light intensity |
|  | [Pressure.csv](#pressurecsv)                         | Measures atmospheric pressure (barometer) |
| **Wireless Signals** | [Bluetooth.csv](#bluetoothcsv)                       | Scanned nearby Bluetooth devices |
|  | [WiFi.csv](#wificsv)                                 | Scanned nearby WiFi APs and connected network |
|  | [Cellular.csv](#cellularcsv)                         | Cellular network information and signal strength |
| **Location / GNSS** | [Location.csv](#locationcsv)                         | Device geographic coordinates and movement info |
|  | [Satellite.csv](#satellitecsv)                       | Individual GNSS satellite observations |
| **Virtual Sensors** | [Game_Rotation.csv](#game_rotationcsv)               | Device orientation vector without geomagnetic data |
|  | [Rotation.csv](#rotationcsv)                         | Device rotation vector including geomagnetic data |
|  | [Gravity.csv](#gravitycsv)                           | Gravity vector in device coordinates |
|  | [Linear_Accelerometer.csv](#linear_accelerometercsv) | Linear acceleration excluding gravity |
|  | [Step_Counter.csv](#step_countercsv)                 | Cumulative step count, only updated when steps change |
|  | [Activity.csv](#activitycsv)                         | Activity recognition output (empty in our experiments) |
| **Metadata** | [Label.csv](#labelcsv) | Marks start and end of each session |


For more information about Android sensors and their behavior, see the official documentation [here](https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview).

### Physical Sensors
#### Accelerometer.csv
Records tri-axis acceleration measurements from the smartphone accelerometer during each data collection session.

Each row represents one sensor sample with the following format:
```
timestamp, acc_x, acc_y, acc_z
```

**Fields:**

| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `acc_x` | Acceleration along the device X-axis | m/s² |
| `acc_y` | Acceleration along the device Y-axis | m/s² |
| `acc_z` | Acceleration along the device Z-axis (including gravity) | m/s² |

**Example:**
```
1736676871715,-0.2664032,-0.090927124,9.9756775
1736676871716,-0.2632141,-0.093322754,10.02832
1736676871728,-0.2592163,-0.09492493,10.00679
```

#### Gyroscope.csv
Records tri-axis angular velocity measurements from the smartphone gyroscope during each data collection session.

Each row represents one sensor sample with the following format:
```
timestamp, gyro_x, gyro_y, gyro_z
```

**Fields:**

| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `gyro_x` | Angular velocity around the device X-axis | rad/s |
| `gyro_y` | Angular velocity around the device Y-axis | rad/s |
| `gyro_z` | Angular velocity around the device Z-axis | rad/s |

**Example:**
```
1736676871716,0.0020751953,4.272461E-4,5.187988E-4
1736676871747,-0.0011749268,-0.0016021729,5.340576E-4
1736676871804,-0.0042266846,-0.007507324,-9.1552734E-5
```

#### Magnetometer.csv
Records tri-axis magnetic field measurements from the smartphone magnetometer during each data collection session. This sensor captures the ambient geomagnetic field and can be used for orientation estimation, indoor localization, and environmental context sensing.

Each row represents one sensor sample with the following format:
```
timestamp, mag_x, mag_y, mag_z
```

**Fields:**

| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `mag_x` | Magnetic field strength along the device X-axis | µT |
| `mag_y` | Magnetic field strength along the device Y-axis | µT |
| `mag_z` | Magnetic field strength along the device Z-axis | µT |

**Example:**
```
1736676871739,3.2714844,-36.827087,99.349976
1736676871789,5.1971436,-36.914062,100.87891
1736676871839,5.9646606,-39.250183,104.22974
```

#### Proximity.csv

Records distance measurements from the smartphone proximity sensor during each data collection session. The proximity sensor is typically used to detect whether an object is close to the device screen (e.g., during phone calls or when the device is in a pocket).

Each row represents one sensor sample with the following format:
```
timestamp, distance
```
**Fields:**

| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `distance` | Distance between the device sensor and the nearest detected object | cm (device-dependent) |

**Example:**
```
1736676871716,8.000183
```
**Notes:** 
- The maximum measurable distance is **device-dependent**. For example, some devices report a maximum value of approximately **5.0 cm**, while others may report larger values (e.g., ~8.0 cm)
- - **A new row is only recorded when the step count changes.**
#### Light.csv

Records ambient light intensity measurements from the smartphone light sensor during each data collection session. This sensor reflects the surrounding illumination conditions and can be useful for inferring indoor/outdoor context, environmental changes, and user activity patterns

Each row represents one sensor sample with the following format:
```
timestamp, illuminance
```
**Fields:**

| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `illuminance` | Ambient light intensity measured by the device sensor | lux |

**Example:**
```
1736676871716,326.0
1736676871739,327.0
```
#### Pressure.csv

Records atmospheric pressure measurements from the smartphone barometer during each data collection session. Pressure readings can be used to infer altitude changes, floor transitions in buildings, and fine-grained motion patterns.

Each row represents one sensor sample with the following format:
```
timestamp, pressure
```
**Fields:**

| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `pressure` | Ambient atmospheric pressure measured by the device sensor | hPa |

**Example:**
```
1736676871716,1015.3933
1736676871753,1015.37866
```

#### Bluetooth.csv
Records Bluetooth scan results detected by the smartphone during each data collection session. Each row corresponds to one discovered Bluetooth device at a given timestamp. This sensor captures nearby wireless context and can support proximity sensing, co-location detection, and environment modeling.

Each row represents one Bluetooth scan record with the following format:
```
timestamp, device_name, address, rssi, uuids_string, type, bond_state
```
**Fields:**

| Column | Description | Type |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the device was detected | int |
| `device_name` | Broadcast name of the Bluetooth device (may be empty or null) | string |
| `address` | MAC address of the Bluetooth device | string |
| `rssi` | Received Signal Strength Indicator (signal power) | dBm |
| `uuids_string` | Advertised service UUIDs (if available, otherwise empty) | string |
| `type` | Bluetooth device type (system-defined integer) | int |
| `bond_state` | Bonding state of the device (system-defined integer) | int |

**Example:**
```
1736680528064,Reyee-4594,94:45:DB:76:A4:C0,-83,,2,10
1736680528946,null,FE:6A:DB:50:72:16,-92,,0,10
1736680532130,null,63:87:A1:3E:F6:F1,-92,,0,10
```
**Notes:**
- Multiple Bluetooth records may appear at the same timestamp due to scanning multiple nearby devices.
- `device_name` may be empty or missing depending on device visibility and privacy settings.

#### Cellular.csv
Records cellular network information detected by the smartphone during each data collection session. Each row corresponds to one cellular cell observation at a given timestamp. This sensor reflects mobile network context and can support mobility analysis, coarse localization, and environment characterization.

Each row represents one cellular scan record with the following format:
```
timestamp, type, connected_signal_level, size, protocol, time, identity, RSCP, isRegistered
```
**Fields:**

| Column | Description | Type |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the cell was observed | int |
| `type` | Network type identifier (system-defined integer) | int |
| `connected_signal_level` | Signal level of the currently connected cell | int |
| `size` | Number of detected cells in the scan | int |
| `protocol` | Cellular protocol (e.g., GSM, LTE, NR) | string |
| `time` | System-provided cell timestamp or identifier | long |
| `identity` | Cell identity or base station identifier | long |
| `RSCP` | Received Signal Code Power (signal strength indicator) | dBm |
| `isRegistered` | Whether the device is currently registered to this cell | boolean |

**Example:**
```
1736680527977,1,5,2,GSM,3739959650133,4271,-83,true
1736680527977,1,5,2,GSM,3739959650133,4261,-107,false
1736680532993,1,5,2,GSM,3744997871381,4271,-81,true
1736680532993,1,5,2,GSM,3744997871381,4261,-107,false
```

#### Location.csv
Records geographic location estimates produced by the smartphone location framework during each data collection session. Each row corresponds to one location update and may originate from different providers (e.g., fused, network, GPS).

Each row represents one location record with the following format:
```
timestamp, category, signal_timestamp, provider, longitude, latitude, altitude, speed, accuracy, bearing
```
**Fields:**

| Column | Description | Unit / Type |
|--------|-------------|-------------|
| `timestamp` | Unix timestamp in milliseconds when the record was logged | ms |
| `category` | Location update category (system-defined integer) | int |
| `signal_timestamp` | Timestamp when the location signal was generated by the provider | ms |
| `provider` | Location provider (e.g., `fused`, `network`, `gps`) | string |
| `longitude` | Longitude coordinate | degrees |
| `latitude` | Latitude coordinate | degrees |
| `altitude` | Altitude above sea level | meters |
| `speed` | Estimated device speed | m/s |
| `accuracy` | Estimated horizontal accuracy radius | meters |
| `bearing` | Device movement direction | degrees |

**Example:**
```
1736680528043,2,1736679803048,fused,114.0568172,22.5364385,-32.91639878288953,0.0,86.832,0.0
1736680529462,1,1736680529260,network,114.055957,22.536472,0.0,0.0,69.9,0.0
1736680533049,2,1736679803048,fused,114.0568172,22.5364385,-32.91639878288953,0.0,86.832,0.0
```
**Notes:**
- Location updates may come from different providers with varying accuracy and latency.
- `accuracy` represents the estimated radius of uncertainty; smaller values indicate higher confidence.
- `altitude`, `speed`, and `bearing` may be zero or missing depending on provider availability.

#### Satellite.csv
Records individual satellite observations detected by the smartphone GNSS receiver during each data collection session. Multiple satellites can be observed at the same timestamp because a single GNSS scan detects multiple satellites simultaneously.

Each row represents one satellite observation record with the following format:
```
timestamp, count, prn, used_in_fix, snr, constellation_type, azimuth, elevation
```
**Fields:**

| Column | Description | Unit / Type |
|--------|-------------|-------------|
| `timestamp` | Unix timestamp in milliseconds when the observation was logged | ms |
| `count` | Total number of satellites observed in the current scan | int |
| `prn` | Satellite PRN (pseudo-random number) identifier | int |
| `used_in_fix` | Whether the satellite was used in the computed location fix | boolean |
| `snr` | Signal-to-noise ratio of the satellite signal | dB-Hz |
| `constellation_type` | Satellite constellation type (e.g., GPS, GLONASS, etc., encoded as integer) | int |
| `azimuth` | Satellite azimuth relative to the receiver | degrees |
| `elevation` | Satellite elevation relative to the horizon | degrees |

**Example:**
```
1736680528043,17,17,false,16.1,1,355.0,47.0
1736680528043,17,19,false,19.7,1,316.0,33.0
1736680528043,17,30,false,16.8,1,199.0,21.0
1736680528043,17,2,false,0.0,1,43.0,10.0
```
**Notes:**
- Multiple satellites may share the same `timestamp` since they are collected from the same GNSS scan.
- `used_in_fix = true` indicates that the satellite contributed to the device's current location fix.
- `snr`, `azimuth`, and `elevation` can help assess signal quality and satellite geometry.

#### WiFi.csv
Records WiFi scan results detected by the smartphone during each data collection session. Each row corresponds to one WiFi access point (AP) observed at a given timestamp.

Each row represents one WiFi record with the following format:
```
timestamp, count, signal_timestamp, ssid, bssid, frequency, rssi
```
**Fields:**

| Column | Description | Type / Unit |
|--------|-------------|-------------|
| `timestamp` | Unix timestamp in milliseconds when the WiFi record was logged | ms |
| `count` | Number of WiFi APs detected in the current scan (0 for connected AP row) | int |
| `signal_timestamp` | Timestamp of the WiFi scan signal (0 for connected AP row) | ms |
| `ssid` | WiFi network name (may be empty if hidden) | string |
| `bssid` | MAC address of the WiFi access point | string |
| `frequency` | Operating frequency of the AP | MHz |
| `rssi` | Received Signal Strength Indicator of the AP | dBm |

**Special case:**  
If both `count` and `signal_timestamp` are `0`, the row represents the AP the smartphone is currently connected to.


**Example:**
```
1736679627080,0,0,"powanphone",3e:ac:ab:87:c6:08,2437,-61
1736679627090,16,1736679640174,"小龙翻大江深圳店",c2:a4:76:8b:45:9b,5745,-45
1736679627090,16,1736679640174,,c2:a4:76:db:45:9b,5745,-46
```
**Notes:**
- Multiple WiFi records may share the same timestamp because multiple APs are detected in one scan.
- `ssid` may be empty if the network is hidden or not broadcasted. It is defined by the AP owner and can be in any language.
- Higher `rssi` (closer to 0) indicates stronger signal strength.
- `frequency` helps distinguish between 2.4 GHz and 5/6 GHz bands.

### Virtual Sensors
#### Game_Rotation.csv
Records the **game rotation vector** from the smartphone during each data collection session. This virtual sensor represents the device’s orientation in 3D space and is commonly used in games and AR/VR applications. Unlike the standard rotation vector, the game rotation vector does not include geomagnetic data, making it less affected by magnetic interference.

Each row represents one sample with the following format:
```
timestamp, x, y, z, w
```

**Fields:**

| Column | Description | Unit / Type |
|--------|-------------|-------------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `x` | X component of the rotation vector (unit quaternion) | float |
| `y` | Y component of the rotation vector (unit quaternion) | float |
| `z` | Z component of the rotation vector (unit quaternion) | float |
| `w` | W component of the rotation vector (unit quaternion, scalar) | float |

**Example:**
```
1736679625788,0.0,0.0,0.0,1.0
1736679625788,-0.1524888,-0.36830738,0.061863642,0.91502446
1736679625789,-0.1516964,-0.36727032,0.06197382,0.9155654
1736679625838,-0.1515326,-0.36649042,0.062232263,0.9158874
1736679625898,-0.15156883,-0.36605558,0.06233039,0.91604865
```

**Notes:** Represents device orientation as a **unit quaternion**; the vector `(x, y, z)` is the rotation axis and `w` is the scalar component.

#### Gravity.csv
Records the **gravity vector** from the smartphone during each data collection session. This virtual sensor represents the direction and magnitude of the gravitational acceleration acting on the device, separated from linear motion. It is commonly used for orientation, motion analysis, and inertial navigation.

Each row represents one sample with the following format:
```
timestamp, x, y, z
```

**Fields:**


| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `x` | Gravity acceleration along the device X-axis | m/s² |
| `y` | Gravity acceleration along the device Y-axis | m/s² |
| `z` | Gravity acceleration along the device Z-axis | m/s² |

**Example:**
```
1736679625788,6.4491296,-3.1983624,6.6595488
1736679625788,6.424861,-3.183549,6.6900353
1736679625788,6.4107795,-3.1704724,6.7097244
```

**Notes:** Gravity vector is extracted from the accelerometer using the device’s sensor fusion algorithm.

#### Gravity.csv
Records the **gravity vector** from the smartphone during each data collection session. This virtual sensor represents the direction and magnitude of the gravitational acceleration acting on the device, separated from linear motion. It is commonly used for orientation, motion analysis, and inertial navigation.

Each row represents one sample with the following format:
```
timestamp, x, y, z
```

**Fields:**


| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `x` | Gravity acceleration along the device X-axis | m/s² |
| `y` | Gravity acceleration along the device Y-axis | m/s² |
| `z` | Gravity acceleration along the device Z-axis | m/s² |

**Example:**
```
1736679625788,6.4491296,-3.1983624,6.6595488
1736679625788,6.424861,-3.183549,6.6900353
1736679625788,6.4107795,-3.1704724,6.7097244
```

**Notes:** Gravity vector is extracted from the accelerometer using the device’s sensor fusion algorithm.

#### Linear_Accelerometer.csv
Records the **linear acceleration** vector from the smartphone during each data collection session. This virtual sensor represents the acceleration caused by the device’s motion **excluding gravity**, making it useful for detecting gestures, steps, or other user movements.

Each row represents one sample with the following format:
```
timestamp, x, y, z
```

**Fields:**


| Column | Description | Unit |
|--------|-------------|------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `x` | Linear acceleration along the device X-axis | m/s² |
| `y` | Linear acceleration along the device Y-axis | m/s² |
| `z` | Linear acceleration along the device Z-axis | m/s² |

**Example:**
```
1736679625788,0.0,0.0,-0.0
1736679625788,-0.0030984879,0.006804228,0.009222984
1736679625788,0.0076527596,0.017472744,-0.010115147
```

**Notes:** Linear acceleration is derived by removing the gravity component from raw accelerometer readings.

#### Rotation.csv
Records the **rotation vector** from the smartphone during each data collection session. This virtual sensor represents the device’s orientation in 3D space, typically computed using sensor fusion of the accelerometer, gyroscope, and magnetometer. Unlike the Game Rotation Vector, this includes the geomagnetic field, providing absolute orientation relative to the Earth.

Each row represents one sample with the following format:
```
timestamp, x, y, z, w, accuracy
```

**Fields:**


| Column | Description | Unit / Type |
|--------|-------------|-------------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `x` | X component of the rotation vector (unit quaternion) | float |
| `y` | Y component of the rotation vector (unit quaternion) | float |
| `z` | Z component of the rotation vector (unit quaternion) | float |
| `w` | W component of the rotation vector (unit quaternion, scalar) | float |
| `accuracy` | Estimated accuracy of the rotation vector | float |

**Example:**
```
1736679625788,-0.15138854,-0.36876097,0.064595155,0.9148357,0.0
1736679625788,-0.15035835,-0.3678201,0.06530648,0.9153337,0.0
1736679625838,-0.1503432,-0.36697996,0.065202326,0.91568077,0.0
```

**Notes:**
- Represents device orientation as a **unit quaternion**.
- Includes geomagnetic data, providing absolute orientation relative to Earth.

#### Step_Counter.csv
Records the **cumulative step count** detected by the smartphone during each data collection session. This sensor counts the number of steps taken by the user since the device was last booted or reset.

Each row represents one sample with the following format:
```
timestamp, steps
```

**Fields:**


| Column | Description | Unit / Type |
|--------|-------------|-------------|
| `timestamp` | Unix timestamp in milliseconds when the sample was recorded | ms |
| `steps` | Cumulative number of steps detected | count |

**Example:**
```
1736679625788,234.0
```

**Notes:**
- Step count is cumulative; differences between consecutive readings represent the number of steps taken during that interval.
- **A new row is only recorded when the step count changes.**

#### Activity.csv

Records the **recognized user activity** using Google Activity Recognition API.  
Each row would normally include a timestamp and activity type, but in our experiments, this file **contains no recorded values**.

### Label.csv
Records the **start and end times of each data collection session**. This file contains only two rows per session: one marking the start and one marking the end.

Each row represents a label record with the following format:
```
timestamp, tag1, tag2, tag3
```

**Fields:**


| Column | Description | Notes |
|--------|-------------|-------|
| `timestamp` | Unix timestamp in milliseconds when the label was recorded | ms |
| `tag1` | Special tag to indicate start or end of the session | int |
| `tag2` | Reserved / placeholder | int |
| `tag3` | Reserved / placeholder | int |

**Example:**
```
1736679625787,0,0,0 # Start of session
1736679640788,-1,-1,-1 # End of session
```
## Notes
- Due to operating system constraints and device power management policies, some sessions may not be successfully activated. For example, sensor collection may be suspended when the system remains idle for a long time or when background execution is restricted. As a result, certain sessions may contain partially missing sensor data.
- If a specific sensor is unavailable or fails to collect data during a session, the corresponding file will exist but remain **empty**.