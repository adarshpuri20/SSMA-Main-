# Smart Sheet Music Annotator
A tool that uses computer vision and basic AI to help musicians interact with sheet music digitally.
we need a small image file of a quarter note as quarter_note_template.png to do template matching properly.

This example uses basic image processing and is a rudimentary prototype; real OCR/OMR requires more sophisticated models.

Install needed Python libraries: opencv-python, mido, python-rtmidi (for MIDI), Pillow (for displaying images in Tkinter), and optionally tkinter if your Python doesn't have it by default.

The MIDI generation is a simple mapping from note vertical position to MIDI pitch and simplistic timing.

The GUI supports drawing rectangular annotations and adding text comments, which are printed and stored in a list.
