# klayouttext
A simple script for creating text polygons in [KLayout](https://www.klayout.de/) mask layout software using Python based on the [fourteen segment display](https://en.wikipedia.org/wiki/Fourteen-segment_display). 

### Installation
The script file can be placed in the KLayout Python interpreter path. This path can be found by printing `sys.path` from the Python `sys` module. Once the script has been placed in this folder, the library can be imported into other KLayout Python macros using `import klayouttext`.

### Use
The script is able to create polygon representations of all 26 capital Latin alphabet characters, as well as digits 0-9. Multi-line text is supported by use of the newline character (`\n`). Each segment of each character is a separate polygon entity.

The main function (`create_text`) places the given text string at a specified location in a specified layer of the mask. The default size of each segment is 15 µm x 2 µm

`create_text` takes 5 arguments:
* `string`: text string to place in layout
* `loc`: location (x,y) of string in layout (in microns)
* `cell`: cell in which to place text
* `layer`: layer in which text is written
* `scale`: relative scale of font (default segment size is 10 µm by 1 µm, scale of 2 will increase this to 20 µm by 2 µm)

### Example
Below is an example macro that creates all valid Latin characters and digits 0-9 with line breaks, as well as a scaled down sample text.
```python
from klayouttext import create_text

layout = pya.Layout()
l1 = layout.layer(1, 0)
top_cell = layout.create_cell("TOP")

create_text("ABCDEFG\nHIJKLMN\nOPQRSTU\nVWXYZ\n0123456789", (0,0), top_cell, l1)
create_text("Example text", (0,-200000), top_cell, l1, scale=0.5)
```

![layout](/assets/font.jpg)
