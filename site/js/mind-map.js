function displayMindMap(userCode, type, divId) {
    var mindMapColor = {
        "card": "#D68314",
        "document": "#ADD614",
        "task": "#D62414",
        "timeline": '#D6CE14'
      };


    var svg = d3.select("#" + divId + " svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");
    svg.selectAll("*").remove();

    // svg.call(d3.zoom().on("zoom", function () {
    //     svg.attr("transform", d3.event.transform)
    //  }))
  
    //var color = d3.scaleOrdinal(d3.schemeCategory20);
  
    var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().distance(function(d) {return 200;}).id(function(d) { return d.id; }))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));
  
    d3.json("/data/mind_map/analytics_graph.json", function(error, sourceGraph) {
        if (error) throw error;

        var graph = sourceGraph[userCode][type];
        
        var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(graph.nodes)
            .enter().append("g")
  
        var circles = node.append("circle")
            .attr("r", function(d) { return d.size; })
            .attr("fill", function(d) { return mindMapColor[d.group]; });
  
        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("stroke-width", function(d) { return Math.sqrt(d.value); });
  
        // Create a drag handler and append it to the node object instead
        var drag_handler = d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
  
        drag_handler(node);
        
        var lables = node.append("text")
            .text(function(d) {
            return d.id;
            })
            .attr('x', 6)
            .attr('y', 3);
    
        node.append("title")
            .text(function(d) { return d.id; });

    
        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);
    
        simulation.force("link")
            .links(graph.links);
  
        function ticked() {
            node
                .attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });

            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
        }
    });
  
    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
  
    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }
  
    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
  
}