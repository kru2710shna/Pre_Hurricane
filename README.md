# Pre-Hurricane Alarm

## Project Description
Developed a machine learning model to predict topological disorder from Northern Atlantic waves, which is essential in detecting and forecasting hurricane activities. Utilizing data from the Google Earth API, the model analyzes key parameters such as wind speed, pressure, and proximity to land. This model is integrated into a real-time alert system, enhancing disaster preparedness for regions at risk of hurricanes. The project showcases advanced pattern recognition and predictive modeling, aiming to improve environmental safety through early detection and alerts.

## Background on Hurricanes
Hurricanes are some of the most devastating natural disasters, causing massive damage to coastal areas around the globe. These powerful storms form over warm ocean waters and are defined by violent winds, heavy rain, and storm surges. The Northern Atlantic region regularly experiences hurricane activity, often leading to the loss of life, damage to property, and disruption of ecosystems.

The increasing frequency and intensity of hurricanes, largely driven by climate change, make them a major global concern. Rising sea temperatures provide more energy for storm formation, resulting in stronger storms. As coastal areas become more vulnerable, millions of people are at risk. Predictive systems and early warning tools are critical in reducing hurricane impact by giving governments and individuals time to prepare and respond effectively.

## Datasets

### 1. [Google Earth Engine - International Best Track Archive for Climate Stewardship (IBTrACS)](https://www.ncei.noaa.gov/products/international-best-track-archive)
IBTrACS provides historical data on the location and intensity of global tropical cyclones, dating back to the 1840s. This dataset includes key information such as wind speed, minimum central pressure, and proximity to land. It is available in 3-hour intervals and is critical for understanding hurricane patterns.

### 2. [NOAA Hurricane Data](https://coast.noaa.gov/hurricanes/)
NOAA's extensive historical hurricane data spans over 150 years, providing a comprehensive look at hurricane tracks, wind speeds, and storm intensities. This dataset is essential for modeling storm behavior and predicting future activities.

### 3. [Kaggle - Hurricanes and Typhoons, 1851-2014](https://www.kaggle.com/datasets/noaa/hurricanes-and-typhoons)
The National Hurricane Center (NHC) conducts post-storm analysis of tropical cyclones in the Atlantic and Pacific Oceans. This dataset includes retrospective storm analysis to improve prediction models, with detailed storm information dating from 1851.

## Real-Life Impact

### Hurricane Katrina (2005)
- Affected Louisiana, Mississippi, and Alabama, causing catastrophic flooding, primarily in New Orleans.
- Resulted in over 1,800 deaths and $125 billion in damages.
  
### Hurricane Maria (2017)
- Devastated Puerto Rico with winds up to 175 mph, leading to the destruction of the power grid and over 3,000 deaths.
  
### Hurricane Harvey (2017)
- Brought unprecedented rainfall and flooding to Texas, with damages exceeding $125 billion.

### Hurricane Sandy (2012)
- Affected the northeastern U.S., causing $70 billion in damages and extensive flooding in New York City.

### Hurricane Dorian (2019)
- Struck the Bahamas as a Category 5 storm, with winds reaching 185 mph, causing widespread destruction and highlighting the vulnerability of small island nations.

## Conclusion
The Pre-Hurricane Alarm system provides a crucial tool for early detection and disaster preparedness. By leveraging advanced machine learning techniques and rich hurricane datasets, this project aims to minimize the catastrophic impact of hurricanes, safeguarding lives and infrastructure.


STEPS: 

=> Open your terminal and clone the repository using:
```bash
git clone <repository_url>
cd <project_directory>
```

=> Create the virtual environment:
```bash
python -m venv venv
```

=> Activate the virtual environment:

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

=> Run the following to install all the required packages:

```bash
pip install -r requirements.txt
```

=> Create a .env file in the project root:

```bash
touch .env
```
=> .env file variables
```bash
GEMINI_API_KEY = {GEMINI API KEY}
OPENWEATHER_API_KEY = {OPENWEATHER API KEY}
GOOGLE_MAPS_API_KEY = {GOOGLE MAPS API KEY}
DB_HOST = {GCP CLOUD PUBLIC IP}
DB_USER = {GCP CLOUD DB USER}
DB_PASSWORD = {GCP CLOUD DATABASE PASSWORD}
DB_NAME = {GCP CLOUD DATABASE NAME}
CLOUD_SQL_CONNECTION_NAME = {GCP CLOUD CONNECTION NAME}
```

=> Run python file

```bash
python app.py
```

Thank you so much! 

