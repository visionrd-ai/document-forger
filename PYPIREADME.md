# Document Forger

Document Forger is a Python package that allows you to create a custom-defined number of documents using one document. This package generates as many forged or synthetic documents as the user needs.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install document forger.

```bash
pip install document-forger
```

Or go to our github page and clone this git repository and install the dependencies through the requirements text file provided

```bash
pip install -r requirements.txt
```

## How it Works

The package is built around using the copy-paste technique. The code utilizes OCR to detect and recognize words and their bounding boxes. The code then goes through the words and decides whether or not two characters are swappable. If they are, the code swaps the first character with the second character. This allows us to create minor forgeries that are unrecognizable to the naked eye but still obvious enough to detection software and AIs.

The purpose behind this package is to artificially expand and create a synthetic dataset that can be used to test Forgery Detection AI and to stress test it with different variations.

![Real vs Forged](https://github.com/visionrd-ai/document-forger/tree/main/docs/Results_1.png)
![Real vs Forged](https://github.com/visionrd-ai/document-forger/tree/main/docs/Results_2.png)
![Real vs Forged](https://github.com/visionrd-ai/document-forger/tree/main/docs/Results_3.png)
![Real vs Forged](https://github.com/visionrd-ai/document-forger/tree/main/docs/Results_4.png)

The above images shows real vs forged generated documents where the red boxes highlight the modifications made to the real document.

This shows the capabilities of our package to work with different sizes, styles and fonts.

## Usage

Through Scripts:

```python
from document_forger.document_processing import process_document

process_document(input_image, output_directory)
```

Or through the terminal

```bash
python -m document_forger --image_path input_img --ouptut_dir output_dir
```
To explore the other arguments just run ```--help``` at the end.

If you have tesseract installed and added to your local enviorments, than set the path to the exe using the following:
```python
from document_forger.utils import set_tesseract_cmd

set_tesseract_cmd(exe_path)
```

Or you can use the ```--tesseract_cmd``` argument in the terminal.

## Contributing

Pull requests are welcome. Go to our Github Page and for major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)