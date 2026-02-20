# reVISit study – Color Scales and Population Density of India: A Basic Questionnaire Study.  

# Deployed Link: https://cdes404.github.io/grizzlybears/

## Purpose of the Study

This study examines how accurately users can estimate differences in population density between Indian states using different color scale legends. Participants are asked to compare two states at a time and estimate how much more densely populated one state is than the other by marking their answer as a percentage. The study consists of ten comparison trials.

In each trial, the color scale used on the map is randomized and may be one of three types: a red monochromatic scale, a full RGB color scale, or a grayscale. By comparing estimation accuracy across these conditions, the study aims to determine which color scale best supports users in interpreting relative population density. To reduce bias, participants are instructed not to rely on prior knowledge of Indian states or their real population densities, as the data used in this study has been intentionally modified.


## Study Notes

Map Creation: The maps were generated using three separate JavaScript files, each implementing a different color scale. These maps were rendered in index.html and then captured as screenshots. Afterward, the specific states being compared in each trial were manually highlighted and labeled. The geographic boundary data for Indian states was sourced from a publicly available GeoJSON file.

Representing the Population Densities: The population density values included several extreme outliers, with some states appearing disproportionately dense or sparse. To reduce the impact of these extremes and improve visual comparability, the data was square-root transformed. Additional adjustments were made to outlier values to ensure a more balanced and interpretable range across all states.

## Technical Achievements
We sourced and integrated two separate datasets: a GeoJSON file defining the boundaries of Indian states and a dataset representing population density values. Ensuring these datasets aligned correctly required additional research and data validation, as state names, boundaries, and formatting needed to match precisely for the map to render accurately. We also processed the population density data to address extreme outliers, applying transformations and adjustments so the values could be represented meaningfully within a visual scale. This preprocessing was essential for enabling fair comparisons and reliable user interpretation during the study.

## Design Achievements
We designed and implemented a fully interactive choropleth map that visualizes population density using multiple color scales. Rather than relying on a simple chart or minimal visual encoding, we incorporated legends and distinct color schemes to support user interpretation and comparison. By experimenting with monochromatic, grayscale, and full RGB color scales, the design goes beyond basic requirements and directly supports the study’s research question.

