import serial
import serial.tools.list_ports
import time

print("------------------------------------------------")
print("   🔍 SYSTEM DIAGNOSTIC TOOL V1.0")
print("------------------------------------------------")

# 1. FIND THE PORT AUTOMATICALLY
ports = list(serial.tools.list_ports.comports())
target_port = None

print("Available Ports:")
for p in ports:
    print(f" > {p.device} ({p.description})")
    # Try to guess the ESP32
    if "CP210" in p.description or "CH340" in p.description or "USB" in p.description:
        target_port = p.device

if not target_port and len(ports) > 0:
    target_port = ports[0].device # Just pick the first one if we can't guess

if not target_port:
    print("\n❌ CRITICAL ERROR: No USB devices found.")
    print("   -> Check USB cable.")
    print("   -> Try a different USB port.")
    exit()

print(f"\n✅ CONNECTING TO: {target_port}")

# 2. ATTEMPT CONNECTION
try:
    ser = serial.Serial(target_port, 115200, timeout=1)
    print("   -> Connection Established.")
    print("   -> Listening for data... (Press Ctrl+C to stop)")
    print("------------------------------------------------")

    while True:
        if ser.in_waiting > 0:
            try:
                # Read the raw bytes
                line = ser.readline()
                
                # Decode to text
                decoded = line.decode('utf-8').strip()
                
                # Print it
                print(f"📨 RAW DATA: {decoded}")
                
            except UnicodeDecodeError:
                print(f"⚠️ GARBAGE DATA: {line} (Baud rate mismatch?)")
                
        else:
            time.sleep(0.1)

except serial.SerialException as e:
    print(f"\n❌ CONNECTION FAILED: {e}")
    print("   -> Is Arduino Serial Monitor open? CLOSE IT.")
    print("   -> Is another Python script running? STOP IT.")