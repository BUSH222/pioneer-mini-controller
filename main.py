import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pioneer_sdk import Pioneer, Camera


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.pioneer = None
        self.camera = None

        self.min_v = 1300
        self.max_v = 1700
        self.channels = [1500, 1500, 1500, 1500, 2000]
        self.default_channels = [1500, 1500, 1500, 1500, 2000]

        self.pioneer_armed = False

        if True:  # Initialise tkinter
            # --- Sidebar Menu (left) ---
            self.title("Pioneer Mini Controller")
            sidebar = ttk.Frame(self, padding="5", borderwidth=2, relief="ridge")
            sidebar.grid(row=0, column=0, rowspan=3, sticky="ns", padx=5, pady=5)

            # Sidebar options
            ttk.Label(sidebar, text="Options", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

            # Control Mode
            ttk.Label(sidebar, text="Control Mode:").pack(anchor="w", pady=2)
            self.control_mode = ttk.Combobox(sidebar, values=["Manual", "Autonomous"])
            self.control_mode.set("Manual")  # Default value
            self.control_mode.pack(fill="x", pady=2)

            # Autopilot Mode
            ttk.Label(sidebar, text="Autopilot Mode:").pack(anchor="w", pady=2)
            self.autopilot_mode = ttk.Combobox(sidebar, values=["Off", "Waypoint", "Follow"])
            self.autopilot_mode.set("Off")  # Default value
            self.autopilot_mode.pack(fill="x", pady=2)

            # Apply Button
            apply_button = ttk.Button(sidebar, text="Apply Settings", command=self.apply_settings)
            apply_button.pack(fill="x", pady=10)

            # --- Status Bar (top) ---
            status_frame = ttk.Frame(self, padding="5")
            status_frame.grid(row=0, column=1, columnspan=3, sticky="ew")

            self.label_drone_connection = ttk.Label(status_frame, text="Drone: Disconnected")
            self.label_camera_connection = ttk.Label(status_frame, text="Camera: Off")
            self.label_battery = ttk.Label(status_frame, text="Battery: 100%")

            self.label_drone_connection.pack(side="left", padx=5)
            self.label_camera_connection.pack(side="left", padx=5)
            self.label_battery.pack(side="left", padx=5)

            # --- Camera View (placeholder) ---
            camera_image = Image.open("assets/camera_off.png")  # Load the default camera image
            camera_image = camera_image.resize((960, 540), Image.Resampling.LANCZOS)  # Resize to fit
            self.camera_photo = ImageTk.PhotoImage(camera_image)

            camera_view = ttk.Label(self, image=self.camera_photo, borderwidth=2, relief="ridge")
            camera_view.grid(row=1, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)

            # --- Speed Diagram (left) ---
            axis_image = Image.open("assets/axis.png")  # Load the axis image
            axis_image = axis_image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize to fit
            self.axis_photo = ImageTk.PhotoImage(axis_image)

            speed_diagram = ttk.Label(self, image=self.axis_photo, borderwidth=2, relief="ridge")
            speed_diagram.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

            # --- Navball (middle) ---
            navball_image = Image.open("assets/navball.png")  # Load the navball image
            navball_image = navball_image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize to fit
            self.navball_photo = ImageTk.PhotoImage(navball_image)

            navball = ttk.Label(self, image=self.navball_photo, borderwidth=2, relief="ridge")
            navball.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

            # --- Logs (right) ---
            logs_frame = ttk.Frame(self, borderwidth=2, relief="ridge")
            logs_frame.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")
            logs_label = ttk.Label(logs_frame, text="Telemetry")
            logs_label.pack(anchor="nw", padx=5, pady=2)
            self.logs_text = tk.Text(logs_frame, wrap="word", height=10)
            self.logs_text.insert("end", "Welcome!\n\n")
            self.logs_text.config(state="disabled")
            self.logs_text.pack(fill="both", expand=True, padx=5, pady=5)

            # Make the columns/rows expand proportionally
            self.columnconfigure(0, weight=0)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=1)
            self.columnconfigure(3, weight=1)
            self.rowconfigure(2, weight=1)

    def postinit(self):
        try:
            self.pioneer = Pioneer()
            self.camera = Camera()
            self.bind("<KeyPress>", self.on_key_press)
            self.bind("<KeyRelease>", self.on_key_release)
        except Exception as e:
            self.add_log(f"nError initializing Pioneer: {e}\n Trying again in 3 seconds...")
            self.after(3000, self.postinit())

    def add_log(self, message):
        self.logs_text.config(state="normal")
        self.logs_text.insert("end", '[LOG] ' + message + "\n")
        self.logs_text.config(state="disabled")
        self.logs_text.see("end")

    def on_key_press(self, event):
        """Handle key press events."""
        key = event.keysym.lower()
        print(key)
        if key == "w":
            self.add_log("Moving Forward")
        elif key == "s":
            self.add_log("Moving Backward")
        elif key == "a":
            self.add_log("Yawing Left")
        elif key == "d":
            self.add_log("Yawing Right")
        elif key == "e":
            self.add_log("Rolling Right")
        elif key == "q":
            self.add_log("Rolling Left")
        elif key == "shift_l":
            self.add_log("Moving Up")
            self.channels[0] += 200
        elif key == "control_l":
            self.add_log("Moving Down")
            self.channels[0] -= 200
        elif key == "space":
            if not self.pioneer_armed:
                self.add_log("Arming the engines")
                self.pioneer.arm()
            else:
                self.add_log("Disarming the engines")
                self.pioneer.disarm()
            self.pioneer_armed = not self.pioneer_armed
        elif key == "tab":
            if self.pioneer_armed:
                self.add_log("Taking off")
                self.pioneer.takeoff()
            else:
                self.add_log("Landing")
                self.pioneer.land()

        if self.pioneer_armed:
            self.pioneer.send_rc_channels(channel_1=self.channels[0],
                                          channel_2=self.channels[1],
                                          channel_3=self.channels[2],
                                          channel_4=self.channels[3],
                                          channel_5=self.channels[4])

    def on_key_release(self, event):
        """Handle key release events."""
        if self.pioneer_armed:
            self.pioneer.send_rc_channels(channel_1=self.default_channels[0],
                                          channel_2=self.default_channels[1],
                                          channel_3=self.default_channels[2],
                                          channel_4=self.default_channels[3],
                                          channel_5=self.default_channels[4])
        # key = event.keysym.lower()

    def apply_settings(self):
        control_mode = self.control_mode.get()
        autopilot_mode = self.autopilot_mode.get()
        self.add_log(f"Settings Applied: Control Mode={control_mode}, Autopilot Mode={autopilot_mode}")
        self.logs_text.see("end")


def main():
    app = App()
    app.after(500, app.add_log, "Pioneer Mini Controller starting...")
    app.after(1000, app.postinit)
    app.mainloop()


if __name__ == "__main__":
    main()
