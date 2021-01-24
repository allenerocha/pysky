import json
from pathlib import Path
from .const import Const


def phase_calculation():
    moon_data = json.loads(
        open(Path(Const.SLIDESHOW_DIR, "PySkySlideshow", f"Moon-{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY}-{Const.START_TIME.replace(':', '')}-{Const.END_YEAR}-{Const.END_MONTH}-{Const.END_DAY}-{Const.END_TIME.replace(':', '')}-data.json"), "r").read()
    )
    moon_data.pop("Coordinates")
    moon_data.pop("Constellation")
    moon_data.pop("Brightness")
    moon_data.pop("Distance")
    
    starting_illumination = moon_data[list(moon_data.keys())[0]]['Illumination']
    ending_illumination = moon_data[list(moon_data.keys())[-1]]['Illumination']
    
    if 0 <= starting_illumination < 1:
        Const.MOON_PHASE = "New Moon"
    elif 1 <= starting_illumination < 49:
        if starting_illumination < ending_illumination:
            Const.MOON_PHASE = "Waxing Crescent"
        else:
            Const.MOON_PHASE = "Waning Crescent"
    elif 49 <= starting_illumination < 51:
        if starting_illumination < ending_illumination:
            Const.MOON_PHASE = "First Quarter"
        else:
            Const.MOON_PHASE = "Last Quarter"
    elif 51 <= starting_illumination < 99:
        if starting_illumination < ending_illumination:
            Const.MOON_PHASE = "Waxing Gibbous"
        else:
            Const.MOON_PHASE = "Waning Gibbous"
    elif 99 <= starting_illumination <= 100:
        Const.MOON_PHASE = "Full Moon"
