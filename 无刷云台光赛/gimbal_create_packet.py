import struct
import serial
import time

# **初始化串口**，避免重复开销
ser = serial.Serial(port='COM6', baudrate=115200, timeout=0.001, write_timeout=0, dsrdtr=False, rtscts=False)


def calculate_crc16(data: bytes) -> int:
    crc = 0
    crc_ta = [
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
        0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
    ]
    for byte in data:
        da = (crc >> 12) & 0x0F
        crc = (crc << 4) & 0xFFFF
        crc ^= crc_ta[da ^ (byte >> 4)]
        da = (crc >> 12) & 0x0F
        crc = (crc << 4) & 0xFFFF
        crc ^= crc_ta[da ^ (byte & 0x0F)]
    return crc


def send_packet(packet: bytearray):
    """
    通过串口发送数据包，仅在延迟超过 1ms 时发出提醒
    """
    global ser
    try:
        start_time = time.perf_counter()
        ser.write(packet)  # 直接发送 bytearray
        end_time = time.perf_counter()

        elapsed_time = (end_time - start_time) * 1000  # 转换为 ms
        if elapsed_time > 1.0:  # **仅在超过 1ms 时提醒**
            print(f"⚠️ 警告：send_packet() 执行时间过长: {elapsed_time:.2f} ms")

    except serial.SerialException as e:
        print(f"串口通信错误: {e}")


trig_counter = 0


def create_packet(data=None):
    """
    创建数据包，并直接调用 `send_packet()`
    """
    global trig_counter
    trig_counter = (trig_counter + 1) % 8
    trig = trig_counter
    valu = 4
    cmd_byte = (trig & 0b111) | ((valu & 0b11111) << 3)

    sync = bytearray([0xA9, 0x5B])
    aux_byte = 0

    gbc_data = data.get('gbc_data', [
        {"go_zero": 1, "wk_mode": 1, "op_type": 0, "op_valu": 0},
        {"go_zero": 1, "wk_mode": 1, "op_type": 0, "op_valu": 0},
        {"go_zero": 1, "wk_mode": 1, "op_type": 0, "op_valu": 0}
    ])

    gbc_bytes = bytearray()
    for gbc in gbc_data:
        gbc_bytes.append(((gbc["go_zero"] & 0b1) << 4) | ((gbc["wk_mode"] & 0b11) << 2) | (gbc["op_type"] & 0b11))
        gbc_bytes.append(gbc["op_valu"] & 0xFF)
        gbc_bytes.append((gbc["op_valu"] >> 8) & 0xFF)

    uav_data = data.get('uav_data', {'valid': 0, 'angle': [0, 0, 0], 'accel': [0, 0, -980]})
    uav_bytes = bytearray([uav_data['valid'] & 0b1])
    for a in uav_data['angle']:
        uav_bytes.extend([a & 0xFF, (a >> 8) & 0xFF])
    for a in uav_data['accel']:
        uav_bytes.extend([a & 0xFF, (a >> 8) & 0xFF])

    cam_data = data.get('cam_data', {'vert_fov1x': 30, 'zoom_value': 1000, 'target_angle': [5.0, 10.0]})
    cam_bytes = bytearray([
        cam_data['vert_fov1x'] & 0b1111111,
        cam_data['zoom_value'] & 0xFF,
        (cam_data['zoom_value'] >> 8) & 0xFF,
        (cam_data['zoom_value'] >> 16) & 0xFF
    ])
    for angle in cam_data['target_angle']:
        cam_bytes.extend(struct.pack('<f', angle))

    packet = sync + bytearray([cmd_byte, aux_byte]) + gbc_bytes + uav_bytes + cam_bytes
    crc = calculate_crc16(packet)
    packet.extend([(crc >> 8) & 0xFF, crc & 0xFF])

    send_packet(packet)  # **直接调用，无需多线程**



def decode_received_data(data: bytes):
    """
    解析串口返回的云台数据包
    """
    if len(data) != 26:
        print("⚠️ 数据长度错误，无法解析")
        return

    unpacked = struct.unpack('<2B B B B B 3h 3h 3h 2B', data)

    sync = unpacked[:2]
    fw_ver = unpacked[2]
    hw_err = unpacked[3]
    inv_flag = unpacked[4] & 0b1
    gbc_stat = (unpacked[4] >> 1) & 0b111
    tca_flag = (unpacked[4] >> 4) & 0b1
    cmd_stat = unpacked[5] & 0b111
    cmd_valu = (unpacked[5] >> 3) & 0b11111
    cam_rate = unpacked[6:9]
    cam_angl = unpacked[9:12]
    mtr_angl = unpacked[12:15]
    crc = unpacked[15:]


    # print(f"  相机欧拉角 (0.01deg): {cam_angl}")
    # print(f"  电机欧拉角 (0.01deg): {mtr_angl}")
    return cam_angl  # 返回相机欧拉角数据

