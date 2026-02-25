# reVISit study – Color Scales and Population Density of India: A Basic Questionnaire Study.  

# Deployed Link: https://cdes404.github.io/grizzlybears/

## Purpose of the Study

This study examines how accurately users can estimate differences in population density between Indian states using different color scale legends. Participants are asked to compare two states at a time and estimate how much more densely populated one state is than the other by marking their answer as a percentage. The study consists of ten comparison trials.

In each trial, the color scale used on the map is randomized and may be one of three types: a red monochromatic/saturation scale, a full RGB color scale, or a grayscale. By comparing estimation accuracy across these conditions, the study aims to determine which color scale best supports users in interpreting relative population density. To reduce bias, participants are instructed not to rely on prior knowledge of Indian states or their real population densities, as the data used in this study has been intentionally modified.

## Experiment Design
Each participant completed randomized trials comparing two highlighted states on a map of India. For every trial:
- The visualization condition (R, G, or RGB) was randomly assigned.
- The state pair was randomly selected from the set of ten comparisons.
- Two states were visually highlighted for comparison.
- Participants estimated the percent difference in population density.

The order of trials was randomized to reduce order effects and learning bias.

Across all participants, the total number of trials per condition was:
- R (Saturation Scale): 56 trials
- G (Grayscale): 62 trials
- RGB (Full Color Scale): 53 trials

Each visualization condition exceeded the minimum number of trials required for stable error estimation.
## Study Notes

Map Creation: The maps were generated using three separate JavaScript files, each implementing a different color scale. These maps were rendered in index.html and then captured as screenshots. Afterward, the specific states being compared in each trial were manually highlighted and labeled. The geographic boundary data for Indian states was sourced from a publicly available GeoJSON file.

Representing the Population Densities: The population density values included several extreme outliers, with some states appearing disproportionately dense or sparse. To reduce the impact of these extremes and improve visual comparability, the data was square-root transformed. Additional adjustments were made to outlier values to ensure a more balanced and interpretable range across all states. A bias warning was given to participants in the study, mentioning that data adjustments had been made and they should not answer questions using prior knowledge of Indian states.

Error Metric and Statistical Analysis: Per Cleveland & McGill (1984), participant responses were evaluated using a log-scaled perceptual error metric.
Raw Error = ∣ Reported Percentage − True Percentage ∣
Log Scaled Error = { 0 if raw error = 0; log₂(Raw Error + 0.125) otherwise}
The log₂ transformation reflects the scaling principle described by Cleveland & McGill, where proportional differences are more meaningful than absolute differences.

For each visualization condition, we computed:
- Mean log₂(Error)
- Median log₂(Error)
- Mean raw error
- Bootstrapped 95% confidence intervals

These values were placed into Tableau and Excel to create visualizations depicting the performance of each condition. 

## Technical Achievements
We sourced and integrated two separate datasets: a GeoJSON file defining the boundaries of Indian states and a dataset representing population density values. Ensuring these datasets aligned correctly required additional research and data validation, as state names, boundaries, and formatting needed to match precisely for the map to render accurately. We also processed the population density data to address extreme outliers, applying transformations and adjustments so the values could be represented meaningfully within a visual scale. This preprocessing was essential for enabling fair comparisons and reliable user interpretation during the study. In addition, we exported raw participant responses from reVISit and merged responses with ground-truth comparison values before computing the error and bootstrapped 95% confidence intervals.

## Design Achievements
We designed and implemented a fully interactive choropleth map that visualizes population density using multiple color scales. Rather than relying on a simple chart or minimal visual encoding, we incorporated legends and distinct color schemes to support user interpretation and comparison. By experimenting with monochromatic, grayscale, and full RGB color scales, the design goes beyond basic requirements and directly supports the study’s research question. Care was taken to maintain visual simplicity in accordance with Cleveland & McGill’s principles. Modeled after their example, the CI graph contains no additional decorative elements or color cues in order to highlight the correct answer, ensuring that the perceptual task remained meaningful and unbiased.

# Example Visualizations
Below are example screenshots of each visualization condition as shown in the experiment:

Red Saturation Scale: 
<img width="1806" height="1121" alt="image" src="https://github.com/user-attachments/assets/7bc43afc-4a25-421b-85de-fb95cf809b8d" />

Grayscale:
<img width="1752" height="1142" alt="image" src="https://github.com/user-attachments/assets/bc7d5cc2-e4f7-4f68-9b9d-6be25c6c4b21" />

RGB Full Color Scale: 
<img width="1721" height="1108" alt="image" src="https://github.com/user-attachments/assets/d0ca0ffd-c460-4c59-ba3d-b0730dcf427f" />

## Study Results
Ranking of error under different conditions:
<img width="724" height="124" alt="image" src="https://github.com/user-attachments/assets/a6cad494-2f88-4872-bb04-02a38a88e20d" />
<img width="1484" height="1152" alt="image" src="https://github.com/user-attachments/assets/21b2020c-1b65-44b9-bd1d-08c9e941df12" />

The figure below shows the mean log₂(Error) per visualization condition with bootstrapped 95% confidence intervals.
<img width="1486" height="1158" alt="image" src="https://github.com/user-attachments/assets/0466899c-54b6-47a2-bde9-474e9448111d" />

Ranking of Conditions (Best → Worst)
- R (Saturation Scale) — Mean log₂(Error): 3.62
- G (Grayscale) — Mean log₂(Error): 3.69
- RGB (Full Color Scale) — Mean log₂(Error): 3.91

Although confidence intervals overlap, the saturation-based red scale consistently produced the lowest mean error across trials. The full RGB color scale resulted in the highest perceptual error.

Interpretation: The results suggest that simpler, monotonic color encodings (saturation and grayscale) slightly improve perceptual accuracy compared to a full RGB color scale. This finding aligns with the argument that simpler visuals reduce cognitive load and improve estimation. The full RGB scale introduces multiple perceptual dimensions, which may increase interpretation difficulty. Grayscale performed nearly as well as the red saturation scale.





