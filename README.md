# heic-2-jpg

## License
The code of heic-2-jpg is released under the MIT License.

## Pre-Requisite Installations
pip install --upgrade pip
pip install pyheif

Please refer to [this page]([https://www.google.com](https://pypi.org/project/pyheif/)) if you have problems with pyhreif

## Usage
1. Clone this repo
2. Run the command
...```python3 convert_heic_to_jpg.py -i /fullpath/to/source/directory -o /fullpath/to/destination/directory 
   ```
3. Append ```-r``` to the command if you intend to get the images resized to 1k (1024 x 768)
4. Append ```-s``` to the command if the images are contained with subdirectories
