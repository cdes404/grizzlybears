console.log("map.js is running");

const width = 1400;
const height = 1000;

const legendWidth = 20;
const legendHeight = 200;
const legendMargin = { top: 50, right: 40 };

// Select SVG and set size
const svg = d3.select("svg")
  .attr("width", width)
  .attr("height", height);

// Load both GeoJSON and CSV
Promise.all([
  d3.json("india-states.geojson"),
  d3.csv("population-density-data/india_states_density.csv")
]).then(([geoData, csvData]) => {

  console.log("GeoJSON loaded:", geoData);
  console.log("CSV loaded:", csvData);

  // ---- AUTO-FIT PROJECTION ----
  const projection = d3.geoMercator()
    .fitSize([width, height], geoData);

  const path = d3.geoPath().projection(projection);

  // ---- CLEAN & CONVERT DATA ----
  csvData.forEach(d => {
    d["Population Density (per km²)"] =
      +d["Population Density (per km²)"];
  });

  // ---- CREATE LOOKUP OBJECT ----
  const densityMap = {};
  csvData.forEach(d => {
    densityMap[d["State/UT"]] =
      d["Population Density (per km²)"];
  });

  console.log("Density map:", densityMap);

  // ---- COLOR SCALE (square-root) ----
  const densities = csvData.map(d => d["Population Density (per km²)"]);
  const minDensity = d3.min(densities);
  const maxDensity = d3.max(densities);

  const colorScale = d3.scaleSequential()
    .domain([Math.sqrt(minDensity), Math.sqrt(maxDensity)]) // square-root domain
    .interpolator(d3.interpolateRgbBasis(["#0000ff", "#00ffff", "#ffff00", "#ff0000"])) // heatmap RGB ramp (blue→cyan→yellow→red)
    .clamp(true);

  // ---- LEGEND ----
  const legendGroup = svg.append("g")
    .attr(
      "transform",
      `translate(${width - legendWidth - 150}, ${legendMargin.top})`
    );

  const defs = svg.append("defs");

  const legendGradient = defs.append("linearGradient")
    .attr("id", "legend-gradient")
    .attr("x1", "0%")
    .attr("y1", "100%")
    .attr("x2", "0%")
    .attr("y2", "0%");

  legendGradient.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", colorScale(Math.sqrt(minDensity)));

  legendGradient.append("stop")
    .attr("offset", "25%")
    .attr("stop-color", colorScale(Math.sqrt(minDensity + (maxDensity - minDensity) * 0.25)));

  legendGradient.append("stop")
    .attr("offset", "50%")
    .attr("stop-color", colorScale(Math.sqrt(minDensity + (maxDensity - minDensity) * 0.5)));

  legendGradient.append("stop")
    .attr("offset", "75%")
    .attr("stop-color", colorScale(Math.sqrt(minDensity + (maxDensity - minDensity) * 0.75)));

  legendGradient.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", colorScale(Math.sqrt(maxDensity)));

  legendGroup.append("rect")
    .attr("width", legendWidth)
    .attr("height", legendHeight)
    .style("fill", "url(#legend-gradient)");

  // For legend axis, keep it linear but display original values
  const legendScale = d3.scaleLinear()
    .domain([minDensity, maxDensity])
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale)
    .ticks(6);

  legendGroup.append("g")
    .attr("transform", `translate(${legendWidth}, 0)`)
    .call(legendAxis);

  legendGroup.append("text")
    .attr("x", -10)
    .attr("y", -10)
    .attr("text-anchor", "start")
    .style("font-size", "12px")
    .text("Population Density (per km²)");

  // ---- DRAW MAP ----
  svg.selectAll("path")
    .data(geoData.features)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("fill", d => {
      const stateName = d.properties.NAME_1;
      const density = densityMap[stateName];

      return density != null ? colorScale(Math.sqrt(density)) : "#ccc";
    })
    .attr("stroke", "#000")
    .attr("stroke-width", 0.8);

}).catch(error => {
  console.error("Error loading files:", error);
});
