from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u
from astroquery.vizier import Vizier
import numpy as np

# ---------------------------------------------------------
# 1. Load a small bright-star catalog (Hipparcos subset)
# ---------------------------------------------------------
# Limit: brightest 200 stars (so comparisons are fast)
Vizier.ROW_LIMIT = 200
hip = Vizier().get_catalogs("I/239/hip_main")[0]
print(hip.colnames)
star_coords = SkyCoord(ra=hip["RAICRS"], dec=hip["DEICRS"], unit=(u.deg, u.deg))

# ---------------------------------------------------------
# 2. Define Locations A and B
# ---------------------------------------------------------
# 39.954227,-87.193843
location_A = EarthLocation(lat=39.954227*u.deg, lon=-87.193843*u.deg, height=0*u.m)  # Example: NYC
location_B = EarthLocation(lat=37.986043*u.deg, lon=23.725149*u.deg, height=0*u.m) # Example: Los Angeles

# ---------------------------------------------------------
# 3. Define time at Location A
# ---------------------------------------------------------
time_A = Time("2024-9-2 00:00:00")  # example timestamp

# ---------------------------------------------------------
# 4. Compute sky at Location A
# ---------------------------------------------------------
altaz_A = star_coords.transform_to(
    AltAz(obstime=time_A, location=location_A)
)

# We only care about stars above the horizon
mask_A = altaz_A.alt > 10*u.deg
coords_A = np.vstack([altaz_A.az[mask_A].value, altaz_A.alt[mask_A].value]).T

# ---------------------------------------------------------
# 5. Scan candidate times for Location B
# ---------------------------------------------------------
search_hours = np.linspace(-6, 6, 121)  # search +/- 6 hours in 6-min increments
best_score = float("inf")
best_time = None

for h in range(1, 3000):
    time_B = time_A + h * u.day

    altaz_B = star_coords.transform_to(
        AltAz(obstime=time_B, location=location_B)
    )

    mask_B = altaz_B.alt > 10*u.deg
    coords_B = np.vstack([altaz_B.az[mask_B].value, altaz_B.alt[mask_B].value]).T

    # ---------------------------------------------------------
    # 6. Compute similarity score
    # ---------------------------------------------------------
    # For simplicity: compare average pairwise difference between all visible stars
    # More sophisticated: match by star ID, angular separation matrices, etc.
    size = min(len(coords_A), len(coords_B))
    if size == 0:
        continue

    diff = coords_A[:size] - coords_B[:size]
    score = np.mean(np.linalg.norm(diff, axis=1))

    # Track best match
    if score < best_score:
        best_score = score
        best_time = time_B

# ---------------------------------------------------------
# 7. Output result
# ---------------------------------------------------------
print("Best matching time at Location B:", best_time.iso)
print("Similarity score:", best_score)
