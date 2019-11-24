# Light & Motion savings analysis
This repo features an example code on how to analyze the timer setting for the lights to be turned off based on the detected motion. This repo *provides an example data set* for both light and PIR readings in the `data` directory.

Read more info at https://www.zvonarov.com/post/improve-energy-conservation-for-buildings

## How does this work
To run the analysis you will need two datetime data series:
- light sensor readings (installed under direct light from the lighting system)
- Motion sensor readings (installed to cover most of the area where the light is active)

Motion sensors connected with the lights usually provide the shutoff timer with a default value set to 30 minutes. You can safely decrease the timer and improved energy efficiency.

In `main.py` configure the `IMPROVED_TIMER` value to correspond to the desired light shutdown timer (in seconds).

## Run the code
Prepare the environment to run the code. For example, using `virtualenv` run:
```
virtualenv -p /path/to/python3 light_analysis
# activate the environment
source light_analysis/bin/activate
# install required libraries
pip install -r requirements.txt
```
After your data is collected, put it in CSV format where the first column is datetime and the second one is value. Name the files `light.csv` and `pir.csv` respectively.

Run `python main.py`. After the data is analyzed you will see the output:
- total time lights were on
- possible time on
- improvement in `%`

The graph will also be shown if supported, if not - will be saved to `picture.png` in the main directory of the repo. You can find an example of a graph in `misc/example.png`

## Logging

For more detailed logs change the log level in `main.py` file, default is `INFO`. For example:

`log.basicConfig(level=log.DEBUG)`