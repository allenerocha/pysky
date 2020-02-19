PySky

# Usage

    ./pysky.py [celestial body (string)] [pixel width (int)] [pixel height (int)] [resolution (float)] [brightness scale (string)]

## Celestial body

    Celestial body          Names comprised of two words must have %20
                            instead of the space character.

## Pixel width and Pixel height

    Pixel dimensions of the image to be produced.

## Resolution

    Size of the image in degrees.

## Brightness Scale

    Linear                  Tends to enhance bright features.
    
    Sqrt                    Intermediate between logarithmic and linear and
                            is close to the response of the eye.
                            
    HistEq                  Can sometimes show subtle features in the data.

### Examples

    ./pysky.py andromeda 1280 720 3.5 Linear
    ./pysky.py vega 1920 1080 3.0 HistEq
    ./pysky.py alula%20australis 1920 1080 3.0 Sqrt
    
# Supported Python Versions

    Python 3.x

# Dependencies

- [Beautiful Soup 4 (bs4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [requests](https://requests.readthedocs.io/en/master/)
- [Pillow](https://python-pillow.org/)
