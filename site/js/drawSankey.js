function getTaskParams(){
  var queryString = window.location.search;
  queryString = decodeURIComponent(queryString.substring(1, queryString.length));
  var params = queryString.split("&");
  
  var key, task;
  if(params.length){
      params.forEach(item => {
          if(item.includes("key")){
              task = item.replace(/key=/, '');
          }else if(item.includes("condition")){
              key = item.replace(/condition=/, '');
          }
      });
  }
  return [key, task];
}

function drawSankey(divId, data, card, pack){
    var units = "documents";
  
    // set the dimensions and margins of the graph
    var margin = {top: 0, right: 0, bottom: 0, left: 0},
        width = 450 - margin.left - margin.right,
        height = 450 - margin.top - margin.bottom;
  
    // format variables
    var formatNumber = d3.format(",.0f"),    // zero decimal places
        format = function(d) { return formatNumber(d) + " " + units; },
        color = d3.scaleOrdinal(d3.schemeCategory10);
  
    $("#" + divId).html();
    // append the svg object to the body of the page
    var svg = d3.select("#" + divId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");
  
    // Set the sankey diagram properties
    var sankey = d3.sankey()
        .nodeWidth(16)
        .nodePadding(20)
        .size([width, height]);
  
    var path = sankey.link();
    
      //set up graph in same style as original example but empty
    var graph = {"nodes" : [], "links" : []};
  
    data.forEach(function (d) {
      graph.nodes.push({ "name": d.source });
      graph.nodes.push({ "name": d.target });
      graph.links.push({ "source": d.source,
                        "target": d.target,
                        "value": +d.size,
                        "documents": d.documents });
    });
  
    // return only the distinct / unique nodes
    graph.nodes = d3.keys(d3.nest()
      .key(function (d) { return d.name; })
      .object(graph.nodes));
  
    // loop through each link replacing the text with its index from node
    graph.links.forEach(function (d, i) {
      graph.links[i].source = graph.nodes.indexOf(graph.links[i].source);
      graph.links[i].target = graph.nodes.indexOf(graph.links[i].target);
    });
  
    // now loop through each nodes to make nodes an array of objects
    // rather than an array of strings
    graph.nodes.forEach(function (d, i) {
      graph.nodes[i] = { "name": d };
    });
  
    sankey
        .nodes(graph.nodes)
        .links(graph.links)
        .layout(32);
  
    // add in the links
    var link = svg.append("g").selectAll(".link")
        .data(graph.links)
      .enter().append("path")
        .attr("class", "link")
        .attr("d", path)
        .style("stroke-width", function(d) { return Math.max(1, d.dy); })
        .sort(function(a, b) { return b.dy - a.dy; });
  
    // add the link titles
    link.append("title")
          .text(function(d) {
          return d.source.name + " → " + 
                  d.target.name + "\n" + format(d.value); });
  
    // add in the nodes
    var node = svg.append("g").selectAll(".node")
        .data(graph.nodes)
      .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { 
        return "translate(" + d.x + "," + d.y + ")"; })
        .call(d3.drag()
          .subject(function(d) {
            return d;
          })
          .on("start", function() {
            this.parentNode.appendChild(this);
          })
          .on("drag", dragmove));
  
    // add the rectangles for the nodes
    node.append("rect")
        .attr("height", function(d) { return d.dy; })
        .attr("width", sankey.nodeWidth())
        .style("fill", function(d) { 
        return d.color = color(d.name.replace(/ .*/, "")); })
        .style("stroke", function(d) { 
        return d3.rgb(d.color).darker(2); })
      .append("title")
        .text(function(d) { 
        return d.name + "\n" + format(d.value); });
  
    // add in the title for the nodes
    node.append("text")
        .attr("x", -6)
        .attr("y", function(d) { return d.dy / 2; })
        .attr("dy", ".35em")
        .attr("text-anchor", "end")
        .attr("transform", null)
        .text(function(d) { return d.name; })
      .filter(function(d) { return d.x < width / 2; })
        .attr("x", 6 + sankey.nodeWidth())
        .attr("text-anchor", "start");
  
    link.on("click", function(d) { 
      if(d.documents){
        //console.log(d);
        var html = '<h4>Top related sub-terms identified during document scanning </h4><br>'
        html += '<strong>Displaying documents representing relations between "' + d.source.name + '" and "' + d.target.name + '"</strong>';
        html += '<ul>';
        var params = getTaskParams();
        
        for (var link in d.documents) {
          var key = d.documents[link]['link'].replace('https://www.bbc.co.uk/news/', '');
          key = d.documents[link]['link'].replace('https://www.thepharmaletter.com/article/', '');
          var analysisLink = '/demo/lc.html?condition=all&key=' + key + '&card=' + card.replace('#', '') + '&pack=' + pack + '&task_condition=' + params[0] + '&task_key=' + params[1];
          html += '<li>'
            + '<strong>' + d.documents[link]['title'] + '</strong><br>'
            + '<p>' + d.documents[link]['description'] + '</p>'
            + '<p><a target="_blank" class="documentListModalLC" href="' + analysisLink + '">Local Context Analysis</a> |'
            + '<a class="documentListModalReference" target="_blank" href="' + d.documents[link]['link'] + '">Reference</a></p>'
            + '</li>';
        }    
        html += '</ul>';
        $('#sankeyList').html(html);
        window.dataLayer.push({
          'event': 'word_relation_display_in_modal',
          'word_relation_display_in_modal_card': card.replace('#', ''),
          'word_relation_display_in_modal_pack': pack
        });
      } else {
        $('#sankeyList').html('<p>Failed to identify scanned results.</p>');
      }
    });
    // the function for moving the nodes
    function dragmove(d) {
      d3.select(this)
        .attr("transform", 
              "translate(" 
                + d.x + "," 
                + (d.y = Math.max(
                    0, Math.min(height - d.dy, d3.event.y))
                  ) + ")");
      sankey.relayout();
      link.attr("d", path);
    }
  }