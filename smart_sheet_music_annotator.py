import cv2
import numpy as np
from mido import Message, MidiFile, MidiTrack
import tkinter as tk
from tkinter import filedialog, simpledialog

# Step 1: Image preprocessing function
def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # Resize for consistent processing
    img = cv2.resize(img, (800, 1000))
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    # Adaptive thresholding to binary image
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2)
    return thresh

# Step 2: Basic template matching to detect quarter notes (example)
# Load a sample quarter note template (you need a small sample image for this)
template_path = 'quarter_note_template.png'
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
template_w, template_h = template.shape[::-1]

def detect_notes(binary_img):
    matches = cv2.matchTemplate(binary_img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(matches >= threshold)
    notes_positions = list(zip(*loc[::-1]))
    return notes_positions

# Step 3: Convert detected notes to MIDI
def notes_to_midi(positions):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    # Note mapping example (y-position to pitch), simplification
    base_pitch = 60  # Middle C (C4)
    
    for pos in positions:
        y = pos[1]
        # Rough pitch by y position (lower y -> higher pitch)
        pitch = base_pitch + int((1000 - y) / 10)  
        track.append(Message('note_on', note=pitch, velocity=64, time=100))
        track.append(Message('note_off', note=pitch, velocity=64, time=200))
    
    midi_output = 'output.mid'
    mid.save(midi_output)
    print(f"MIDI saved as {midi_output}")

# Step 4: Simple Tkinter GUI to annotate image
class AnnotatorApp:
    def __init__(self, master, img_path):
        self.master = master
        self.img_path = img_path
        self.img = cv2.imread(img_path)
        self.canvas = tk.Canvas(master, width=self.img.shape[1], height=self.img.shape)
        self.canvas.pack()
        self.tk_img = None
        self.load_image()
        self.rect_start = None
        self.rect = None
        self.annotations = []
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
    
    def load_image(self):
        # Convert OpenCV image (BGR) to PhotoImage via RGB
        cv_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        from PIL import Image, ImageTk
        pil_img = Image.fromarray(cv_img)
        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)

    def on_press(self, event):
        self.rect_start = (event.x, event.y)
        self.rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red')

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.rect_start[0], self.rect_start, event.x, event.y)

    def on_release(self, event):
        comment = simpledialog.askstring("Input", "Add annotation comment:")
        if comment:
            self.annotations.append((self.rect_start, self.rect_start, event.x, event.y, comment))
            print(f"Annotation saved: {comment}")
        else:
            self.canvas.delete(self.rect)
        self.rect = None

# Main program
if __name__ == "__main__":
    # Ask user to select an image file via GUI
    root = tk.Tk()
    root.withdraw()  # Hide main window
    img_file = filedialog.askopenfilename(title='Select Sheet Music Image')
    if not img_file:
        print("No image selected, exiting.")
        exit()

    # Preprocess image
    binary_img = preprocess_image(img_file)

    # Detect notes (requires you have quarter_note_template.png prepared)
    note_positions = detect_notes(binary_img)
    print(f"Detected {len(note_positions)} notes.")

    # Convert to MIDI
    notes_to_midi(note_positions)

    # Start GUI annotator
    annot_root = tk.Tk()
    annot_root.title("Sheet Music Annotator")
    app = AnnotatorApp(annot_root, img_file)
    annot_root.mainloop()
