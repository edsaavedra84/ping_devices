# Ping Thermostats

A simple Python utility to monitor network connectivity of smart thermostats on a local network by pinging their IP addresses and logging the results.

## Purpose

This script was created to monitor the connectivity of multiple thermostats on my home network (upstairs, living room, playroom, etc.). It periodically checks if each thermostat is reachable and logs the results for troubleshooting connectivity issues.

**Note**: This script is tailored for my specific network configuration but can be easily adapted for anyone's network monitoring needs by modifying the `config.json` file.

## Features

- Cross-platform support (Windows and Linux)
- Configurable execution interval via JSON configuration
- Runs continuously as a monitoring service
- Automatic log rotation (daily) with 10-day retention
- Detailed logging with timestamps and platform information
- Simple, lightweight script with minimal dependencies

## Installation

### Option 1: Docker (Recommended)

1. Clone or download this repository
2. Create your configuration file:
   ```bash
   cp config.example.json config/config.json
   # Edit config/config.json with your IP addresses
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. View logs:
   ```bash
   docker-compose logs -f
   ```

### Option 2: Local Python Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create your configuration file:
   ```bash
   cp config.example.json config/config.json
   # Edit config/config.json with your IP addresses
   ```

## Configuration

The script reads its configuration from `config.json`. To configure your own devices:

1. Copy `config.example.json` to `config.json` (if not already done during installation)
2. Edit `config.json` in the project directory
3. Modify the configuration parameters:

```json
{
  "interval_seconds": 30,
  "ip_addresses": [
    {
      "ip": "192.168.1.120",
      "name": "Upstairs Thermostat"
    },
    {
      "ip": "192.168.1.235",
      "name": "Living Room Thermostat"
    }
  ]
}
```

**Configuration Parameters:**
- `interval_seconds`: How often to ping all devices (in seconds). Default: 30 seconds
- `ip_addresses`: Array of devices to monitor
  - `ip`: The IP address to ping (required)
  - `name`: Descriptive name for documentation purposes (optional)

## Usage

### Using Docker (Recommended)

Start the container in the background:
```bash
docker-compose up -d
```

View real-time logs:
```bash
docker-compose logs -f
```

Stop the container:
```bash
docker-compose down
```

Restart the container (e.g., after config changes):
```bash
docker-compose restart
```

**Notes:**
- Logs are written to both console (viewable with `docker-compose logs`) and `./logs/pinging.log`
- Configuration is read from `./config/config.json` on the host machine
- The container uses `network_mode: host` to access devices on your local network

### Using Python Directly

The script runs continuously as a monitoring service. Start it with:

```bash
python ping_thermostats.py
```

The script will:
1. Immediately ping all devices on startup
2. Continue to ping all devices at the interval specified in `config.json`
3. Log all results to console and `pinging.log` (or `logs/pinging.log` if directory exists)
4. Run indefinitely until stopped with `Ctrl+C`

### Running as a Background Service (Non-Docker)

**Linux (systemd)**:
Create a systemd service for automatic startup:
```bash
sudo nano /etc/systemd/system/ping-thermostats.service
```

Add the following content:
```ini
[Unit]
Description=Thermostat Ping Monitor
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/ping_thermostats
ExecStart=/path/to/ping_thermostats/venv/bin/python ping_thermostats.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable ping-thermostats
sudo systemctl start ping-thermostats
```

**Windows**:
Use Task Scheduler to run the script on system boot, or run the Docker container as a Windows service using tools like NSSM.

## Logs

Logs are written to **both console (stdout) and file**:

- **Console**: INFO level and above, displayed in real-time
- **File**: DEBUG level and above, written to:
  - `logs/pinging.log` (if logs directory exists, e.g., Docker setup)
  - `pinging.log` (in script directory, for non-Docker setup)

**Log Format:**
```
YYYY-MM-DD at HH:mm:ss | LEVEL | message
```

**Log Settings:**
- **Rotation**: Daily
- **Retention**: 10 days
- **Levels**: DEBUG (file), INFO (console)

## Dependencies

- `loguru` - Advanced logging library
- `schedule` - Job scheduling library for periodic task execution
- `colorama` - Cross-platform colored terminal output
- `win32_setctime` - Windows timestamp support for loguru

## Adapting for Your Use

To use this script for your own devices:

1. Edit `config.json` and add your device IP addresses with descriptive names
2. Adjust `interval_seconds` in `config.json` to set your desired ping frequency
3. Optionally modify the log format, rotation, or retention settings in `ping_thermostats.py` (lines 11-13)
4. Run the script and let it monitor continuously

## License

Free to use and modify for personal or commercial purposes.
