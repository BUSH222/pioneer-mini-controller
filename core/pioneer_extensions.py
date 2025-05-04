def send_manual_control(self, x, y, z, r, buttons):
    """
    Sends a MANUAL_CONTROL MAVLink command to the drone.

    :param x: Pitch input (-1000 to 1000)
    :param y: Roll input (-1000 to 1000)
    :param z: Throttle input (0 to 1000)
    :param r: Yaw input (-1000 to 1000)
    :param buttons: Bitfield for joystick buttons (0 if no buttons are pressed)
    """
    if not self.connected():
        raise ConnectionError("Not connected to the drone")

    self.mavlink_socket.mav.manual_control_send(
        self.mavlink_socket.target_system,
        x, y, z, r, buttons
    )
    self.log(msg_type='MANUAL_CONTROL', msg=f'Sent MANUAL_CONTROL: x={x}, y={y}, z={z}, r={r}, buttons={buttons}')
