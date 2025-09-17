# Copilot Instructions for Microcontroladores

## Project Overview
This repository contains Arduino projects for microcontroller-based electronics and sensor integration. Each subfolder represents a distinct hardware-focused lesson or module.

### Major Components
- `Clase_1_Electronica/Clase_1_Electronica.ino`: Introductory electronics lesson, likely covers basic microcontroller setup and I/O.
- `Sensor_VL53L0X/Sensor_VL53L0X.ino`: Demonstrates usage of the VL53L0X time-of-flight distance sensor with a microcontroller.

## Developer Workflows
- **Development:** Edit `.ino` files using the Arduino IDE or compatible editor. Each folder is a self-contained sketch.
- **Build & Upload:** Use the Arduino IDE to select the correct board and port, then compile and upload each sketch individually.
- **Debugging:** Use serial output (e.g., `Serial.print`) for runtime diagnostics. Connect the microcontroller to a PC and open the Serial Monitor in the Arduino IDE.

## Project-Specific Conventions
- Each lesson or sensor integration is isolated in its own folder for clarity and modularity.
- Sketches are named after their folder for easy identification.
- Hardware-specific code (e.g., sensor libraries) should be included at the top of each `.ino` file.
- Comments in Spanish are common; preserve language and style when editing or adding documentation.

## Integration Points
- External libraries (e.g., VL53L0X sensor library) must be installed via the Arduino Library Manager before building relevant sketches.
- No cross-sketch communication; each `.ino` is independent.

## Examples
- To add a new sensor integration, create a new folder and place a single `.ino` file named after the folder.
- To debug hardware issues, add `Serial.print` statements and use the Serial Monitor.

## Key Files
- `Clase_1_Electronica/Clase_1_Electronica.ino`: Reference for basic microcontroller setup.
- `Sensor_VL53L0X/Sensor_VL53L0X.ino`: Reference for sensor integration patterns.

---
**For AI agents:**
- Always match the language and commenting style of existing code.
- When adding new modules, follow the folder/file naming convention.
- Document hardware requirements and library dependencies in comments at the top of new `.ino` files.
