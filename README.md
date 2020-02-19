PySky

<b>Usage</b>

    ./pysky.py [celestial body (string)] [pixel width (int)] [pixel height (int)] [resolution (float)] [brightness scale (string)]

<b>Celestial body</b>

    Celestial body          Names comprised of two words must have %20
                            instead of the space character.

<b>Pixel width and Pixel height</b>

    Pixel dimensions of the image to be produced.
    

<b>Resolution</b>

    Size of the image in degrees.

<b>Brightness Scale</b>

    Linear                  Tends to enhance bright features.
    
    Sqrt                    Intermediate between logarithmic and linear and
                            is close to the response of the eye.
                            
    HistEq                  Can sometimes show subtle features in the data.

<b>Examples</b>

    ./pysky.py andromeda 1280 720 3.5 Linear
    ./pysky.py vega 1920 1080 3.0 HistEq
    ./pysky.py alula%20australis 1920 1080 3.0 Sqrt
