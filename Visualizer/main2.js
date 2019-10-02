d3.json("items_ehh.json", function(error, data) {
  console.log(data);
  var nodes = data.nodes
  var links = data.links




function getNodeColor(node) {
  return node.level === 1 ? 'red' : 'red'
}
var width = window.innerWidth
var height = window.innerHeight

var svg = d3.select('svg')
svg.attr('width', width).attr('height', height)
// simulation setup with all forces

var linkForce = d3
  .forceLink()
  .id(function (link) { return link.id })
  .strength(function (link) { return link.strength })

var simulation = d3
  .forceSimulation()
  .force('link', linkForce)
  .force('charge', d3.forceManyBody().strength(-120))
  .force('center', d3.forceCenter(width / 2, height / 2))

var linkElements = svg.append("g")
  .attr("class", "links")
  .selectAll("line")
  .data(links)
  .enter().append("line")
    .attr("stroke-width", 1)
    .attr("stroke", "rgba(50, 50, 50, 0.2)")

var nodeElements = svg.append("g")
  .attr("class", "nodes")
  .selectAll("circle")
  .data(nodes)
  .enter().append("circle")
    .attr("r", 5 )
    .attr("fill", getNodeColor)



var textElements = svg.append("g")
  .attr("class", "text")
  .selectAll("text")
  .data(nodes)
  .enter().append("text")
    .text(function (node) { return  node.title })
    .attr("font-size", 2)
    .attr("dx", 5)
    .attr("dy", 1)

simulation.nodes(nodes).on('tick', () => {
  nodeElements
    .attr('cx', function (node) { return node.x })
    .attr('cy', function (node) { return node.y })
  textElements
    .attr('x', function (node) { return node.x })
    .attr('y', function (node) { return node.y })
  linkElements
    .attr('x1', function (link) { return link.source.x })
    .attr('y1', function (link) { return link.source.y })
    .attr('x2', function (link) { return link.target.x })
    .attr('y2', function (link) { return link.target.y })
})

simulation.force("link").links(links)

});