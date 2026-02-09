const width = 900;
const height = 1000;

const svg = d3.select("svg");

// Projection tuned for India
const projection = d3.geoMercator()
  .center([82, 22])
  .scale(1100)
  .translate([width / 2, height / 2]);

const path = d3.geoPath().projection(projection);

// Load GeoJSON (no topojson needed)
d3.json("india-states.geojson").then(data => {

  svg.selectAll("path")
    .data(data.features)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("fill", "#f5f5f5")
    .attr("stroke", "#000")
    .attr("stroke-width", 0.8);
});
