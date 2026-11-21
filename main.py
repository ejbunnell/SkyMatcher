from datetime import datetime
from zoneinfo import ZoneInfo

from starplot import Star, Observer, _

tz = ZoneInfo("America/Indianapolis")
dt = datetime(2024, 9, 2, 0, 0, tzinfo=tz)

observer = Observer(
    dt=dt,
    lat=39.954182,
    lon=-87.193711,
)

# p = ZenithPlot(
#     observer=observer,
#     resolution=4000,
# )
# p.constellations()  # Plot the constellation lines first
# p.stars(where=[_.magnitude < 6], where_labels=[_.magnitude < 1])
# p.horizon()
# p.constellation_labels()  # Plot the constellation labels last to avoid collisions

# p.export("test.svg")


test = Star.find(where=[_.magnitude < 6]);