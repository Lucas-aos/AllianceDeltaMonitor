# Alliance Delta Monitor

OCR-based pressure monitoring tool for Alliance HPLC instruments from Waters.

This tool reads the pressure value displayed in the instrument software using OCR
and calculates pressure deltas over 30 and 60 seconds in PSI.

The program runs as a lightweight transparent overlay window that can be positioned
over the instrument software interface.

---

## Features

- Real-time OCR pressure reading
- Delta calculation over **30 seconds** and **60 seconds**
- Transparent overlay window
- Resettable runtime timer
- Lightweight GUI built with Tkinter
- Standalone Windows executable

---

## Security Notice

This application captures **only a small region of the screen** to perform OCR
on the pressure value displayed by the instrument software.

No screenshots are saved, and no data is stored, logged, or transmitted externally.

The program operates entirely locally.

---

## Screenshot

Example interface:

![Interface](docs/interface.png)

---

## Running the Python version

Install dependencies:
pip install -r requirements.txt
Run:
python delta_pressure.py

---

## Standalone executable

A compiled Windows executable is available in the **Releases** section.

Download:
AllianceDeltaMonitor.exe

No Python installation is required.

---

## Build executable

To build the executable manually:

pyinstaller --noconfirm --windowed \
--name AllianceDeltaMonitor \
--icon=delta.ico \
--version-file build_tools/version.txt \
--add-data "tesseract;tesseract" \
--add-data "delta.ico;." \
delta_pressure.py

---

## Author

Lucas Albuquerque

---

## License

This project is licensed under the MIT License.




