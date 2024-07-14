import sys
from threading import *

import customtkinter
from PIL import Image

from testing import start_webcam_inference

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


# chuyen doi widget GUI -> doi tuong ghi du lieu stdout
class Console(customtkinter.CTkTextbox):
    def __init__(self, *args, **kwargs):
        customtkinter.CTkTextbox.__init__(self, *args, **kwargs)
        self.bind("<Destroy>", self.reset)
        self.old_stdout = sys.stdout
        sys.stdout = self

    # xoa noi dung cua Console
    def delete(self, *args, **kwargs):
        self.configure(state="normal")
        self.delete(*args, **kwargs)
        self.configure(state="disabled")

    # ghi noi dung vao Console
    def write(self, content):
        self.configure(state="normal")
        self.insert("end", content)
        self.configure(state="disabled")

    # reset stdout ve gia tri ban dau
    def reset(self, event):
        sys.stdout = self.old_stdout

    # compulsory
    def flush(self):
        pass


# de chay GUI console trong nen ma ko anh huong den GUI camera
def threading(func, args):
    t1 = Thread(target=func, args=args)
    t1.start()


def launch(gui, cam_gui):
    model_name = "traffic_sign_classifier.model"
    use_video = True if gui.prerecorded_switch_var.get() == "on" else False
    gui.main_label.configure(text="Live Camera")
    start_webcam_inference(model_name, use_video, cam_gui)


class Video_GUI(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Traffic Sign Recognition")
        self.resizable(width=False, height=False)
        self.geometry("800x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = customtkinter.CTkFrame(master=self, fg_color="#161b22", corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.main_label = customtkinter.CTkLabel(master=self.main_frame, text="Live Camera",
                                                 font=customtkinter.CTkFont(family="Roboto Mono", size=16))
        self.main_label.grid(row=0, column=0, sticky="w", padx=20, pady=(24, 0))
        self.main_inner_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="#30363d", corner_radius=10)
        self.main_inner_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.main_inner_frame.grid_columnconfigure(0, weight=1)
        self.main_inner_frame.grid_rowconfigure(0, weight=1)
        self.image_label = customtkinter.CTkLabel(master=self.main_inner_frame, text="", bg_color="transparent")
        self.image_label.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Traffic Sign Classifier")
        self.resizable(width=False, height=False)
        self.geometry("1280x720")

        self.grid_rowconfigure(0, weight=1)

        self.side_bar = customtkinter.CTkFrame(master=self, fg_color="#0d1117", corner_radius=0, width=320)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.side_bar.grid_columnconfigure(0, weight=1)
        self.side_bar.grid_rowconfigure(1, weight=1)
        self.side_bar.grid_propagate(False)

        self.logo_label = customtkinter.CTkLabel(master=self.side_bar, text="Traffic Sign\nClassifier",
                                                 font=customtkinter.CTkFont(family="Roboto Mono", size=22))
        self.logo_label.grid(row=0, column=0, padx=12, pady=(20, 0), sticky="nsew")

        self.launch_button = customtkinter.CTkButton(master=self.side_bar, height=32, text="Launch",
                                                     text_color="#000000",
                                                     font=customtkinter.CTkFont(family="Roboto Mono", size=16),
                                                     command=self.launch_button_event)
        self.launch_button.grid(row=2, column=0, padx=40, pady=8, sticky="nsew")

        self.model_label = customtkinter.CTkLabel(master=self.side_bar, text="e", text_color="#5e7373", anchor="w",
                                                  font=customtkinter.CTkFont(family="Roboto Mono", size=10))
        self.model_label.grid(row=3, column=0, padx=16, pady=0, sticky="sew")

        self.main_area = customtkinter.CTkFrame(master=self, fg_color="#161b22", corner_radius=0, width=960)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_propagate(False)

        self.main_upper_frame = customtkinter.CTkFrame(master=self.main_area, fg_color="#161b22", corner_radius=0)
        self.main_upper_frame.grid(row=0, column=0, sticky="nsew")
        self.main_upper_frame.grid_columnconfigure(1, weight=1)
        self.main_lower_frame = customtkinter.CTkFrame(master=self.main_area, fg_color="#30363d", corner_radius=10)
        self.main_lower_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        self.main_lower_frame.grid_columnconfigure(1, weight=1)
        self.new_main_lower_frame = customtkinter.CTkFrame(master=self.main_area, fg_color="#30363d", corner_radius=10)
        self.new_main_lower_frame.grid_columnconfigure(0, weight=1)
        self.new_main_lower_frame.grid_rowconfigure(0, weight=1)

        self.main_label = customtkinter.CTkLabel(master=self.main_upper_frame, text="Setup Params", anchor="w",
                                                 font=customtkinter.CTkFont(family="Roboto Mono", size=18))
        self.main_label.grid(row=0, column=0, padx=20, pady=(32, 0))

        self.cam_toplevel_window = None

        self.switch_label = customtkinter.CTkLabel(master=self.main_lower_frame, text="Choose to use",
                                                   font=customtkinter.CTkFont(family="Roboto Mono", size=16))
        self.switch_label.grid(row=1, column=0, padx=24, pady=(24, 6), sticky="w")
        self.prerecorded_switch_var = customtkinter.StringVar(value="off")
        self.inference_switch_var = customtkinter.StringVar(value="on")
        self.inference_switch = customtkinter.CTkSwitch(master=self.main_lower_frame, text="Use Camera",
                                                        font=customtkinter.CTkFont(family="Roboto Mono", size=14),
                                                        variable=self.inference_switch_var, onvalue="on",
                                                        offvalue="off",
                                                        command=self.inference_switch_event)
        self.inference_switch.grid(row=2, column=0, padx=32, pady=(12, 0), sticky="w")
        self.prerecorded_switch = customtkinter.CTkSwitch(master=self.main_lower_frame, text="Use Video",
                                                          font=customtkinter.CTkFont(family="Roboto Mono", size=14),
                                                          variable=self.prerecorded_switch_var, onvalue="on",
                                                          offvalue="off")
        self.prerecorded_switch.grid(row=2, column=1, padx=20, pady=(12, 0), sticky="w")

        self.inference_switch_event()
        self.line = customtkinter.CTkFrame(master=self.main_lower_frame, fg_color="#2b2d30", corner_radius=1, height=2)
        self.line.grid(row=3, column=0, padx=16, pady=(24, 16), sticky="ew", columnspan=2)

        self.console_var = customtkinter.StringVar()
        self.console_label = Console(master=self.new_main_lower_frame, fg_color="#30363d",
                                     font=customtkinter.CTkFont(family="Roboto Mono", size=12))
        self.console_label.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

    def launch_button_event(self):
        self.launch_button.configure(state="disabled", fg_color="#b54747", text_color_disabled="#000000")
        self.switch_frame()
        self.cam_toplevel_window = Video_GUI()
        self.cam_toplevel_window.grab_set()
        threading(launch, (self, self.cam_toplevel_window))

    def switch_frame(self):
        self.main_lower_frame.destroy()
        self.new_main_lower_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)

    def inference_switch_event(self):
        if self.inference_switch_var.get() == "on":
            self.prerecorded_switch_var.set(value="off")
            self.prerecorded_switch.configure(state="normal")
        else:
            self.prerecorded_switch.configure(state="disabled")


if __name__ == '__main__':
    window = GUI()
    window.mainloop()
