import subprocess
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Declare codec_var globally
codec_var = None

def change_resolution(input_file, output_file, resolution):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f'scale={resolution}',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    subprocess.run(command)

def change_codec(input_file, output_file, codec):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-c:v', codec,
        output_file
    ]
    subprocess.run(command)

def compare_videos(input_file1, input_file2, output_file):
    command = [
        'ffmpeg',
        '-i', input_file1,
        '-i', input_file2,
        '-filter_complex', '[0:v]pad=iw*2:ih[bg];[bg][1:v]overlay=w',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    subprocess.run(command)

def process_video():
    input_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if input_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], title="Save Processed Video")
        if output_path:
            selected_codec = codec_var.get()
            change_codec(input_path, output_path, selected_codec)
            messagebox.showinfo("Success", "Video processing complete.")

def process_with_codec(codec):
    input_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if input_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], title="Save Processed Video")
        if output_path:
            change_codec(input_path, output_path, codec)
            messagebox.showinfo("Success", "Video processing complete.")

def main():
    # Default values
    input_file = 'bunny.mp4'
    output_folder = 'output_videos'

    resolutions = ['1280x720', '854x480', '640x360', '320x240']
    codecs = ['libvpx', 'libvpx-vp9', 'libx265', 'libaom-av1']

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Change resolution
    for resolution in resolutions:
        output_file = os.path.join(output_folder, f'output_resolution_{resolution}.mp4')
        change_resolution(input_file, output_file, resolution)

    # Change codec
    for codec in codecs:
        output_file = os.path.join(output_folder, f'output_codec_{codec}.mp4')
        change_codec(input_file, output_file, codec)

    input_file_vp8 = 'output_codec_libx265.mp4'
    input_file_vp9 = 'output_codec_libvpx-vp9.mp4'
    output_file = 'output_comparison.mp4'

    # Assuming both input videos have the same resolution
    compare_videos(input_file_vp8, input_file_vp9, output_file)

    # Create the main window
    global codec_var  # Declare codec_var as global
    root = tk.Tk()
    root.title("Video Codec Changer")
    root.geometry("800x600")  # Set initial window size

    # Background Image
    background_image = tk.PhotoImage(file='messi.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Style for the widgets
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="black", foreground="black", font=('Helvetica', 12))
    style.configure("TLabel", padding=6, font=('Helvetica', 12))
    style.configure("TFrame", background="#F8F9FA")

    # Create a frame with a lighter background color
    frame = ttk.Frame(root, style="TFrame")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Create a label
    label = ttk.Label(frame, text="Select a video file and choose a new codec:", style="TLabel")
    label.grid(row=0, column=0, pady=10)

    # Create a dropdown for selecting the codec
    codec_var = tk.StringVar(root)
    codec_var.set(codecs[0])  # Default codec

    codec_dropdown = ttk.Combobox(frame, textvariable=codec_var, values=codecs, style="TButton")
    codec_dropdown.grid(row=1, column=0, pady=10, padx=20, sticky="we")

    # Create buttons for each codec
    for i, codec in enumerate(codecs):
        button = ttk.Button(frame, text=f"Process with {codec}", command=lambda c=codec: process_with_codec(c), style="TButton")
        button.grid(row=i + 2, column=0, pady=10, ipadx=20, ipady=10, sticky="we")

    # Create a button to process the video
    process_button = ttk.Button(frame, text="Process Video", command=process_video, style="TButton")
    process_button.grid(row=len(codecs) + 2, column=0, pady=10, ipadx=20, ipady=10, sticky="we")

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
