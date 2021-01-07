# mini-tracker4antenna
Educational satellite tracking antenna device based on Raspberry Pi and SG92R servos

## Elevation calculation
For low elevation passes, the trajectory approaches a parabolic curve. At elevations closer to the zenith, the approximation to a gaussian bell is better.
In this first iteration, the **calculation is based on a quadratic equation of a parabolic curve**.

