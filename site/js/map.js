function drawMapBlocksPerDateGraph(divId, data, className, width, height){
    // set the dimensions and margins of the graph
    var margin = {top: 30, right: 30, bottom: 100, left: 60},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;
  
    // set the ranges
    var x = d3.scaleBand()
          .range([0, width])
          .padding(0.1);
    var y = d3.scaleLinear()
          .range([height, 0]);
        
    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#" + divId).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("class", className)
    .append("g")
      .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");
  
    // format the data
    // data.forEach(function(d) {
    //   d.value = +d.value;
    // });
  
    // Scale the range of the data in the domains
    var maxY = d3.max(data, function(d) { return d.value; });
    x.domain(data.map(function(d) { return d.date; }));
    y.domain([0, maxY]);
  
    // append the rectangles for the bar chart
    svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.date); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value); });
  
    // add the x Axis
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).tickValues(x.domain().filter(function(d,i){ return !(i%1)})).tickFormat(d3.timeFormat("%Y-%m-%d")))
      .selectAll("text")	
          .style("text-anchor", "end")
          .attr("dx", "-.8em")
          .attr("dy", ".15em")
          .attr("transform", "rotate(-65)");
  
    // add the y Axis
    svg.append("g")
      .call(d3.axisLeft(y).ticks(maxY).tickFormat(d3.format(".0f")));
  
      svg.append("text")
      .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
      .attr("transform", "translate("+ (-30) +","+(height/2)+")rotate(-90)")  // text is drawn off the screen top left, move down and out and rotate
      .text("Documents count");
  
    svg.append("text")
      .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
      .attr("transform", "translate("+ (width/2) +","+(height + 80)+")")  // centre below axis
      .text("Date");
  
    return svg;
  }
  
  function mapReady(error, data, items) {
    // Set map tooltips
    var mapTooltip = d3.tip()
      .attr('class', 'd3-map-tip')
      .offset([-10, 0])
      .html(function(d) {
        var url = '/rc.html?key=' + d.key;
        var html = "<strong>Country: </strong><span class='details'><a href=\"" + url + "\">" 
          + d.properties.name + "</a><br></span>"
          + "<strong>Blocks count in range: </strong><span class='details'>" 
          + d.total_block_count +"</span>";
        if (d.count_per_day) {
          var divId = 'map' + d.id;
          html += "<div id=\"" + divId+ "\" class=\"tooptipMap\"></div>";
        }
        return html;
      });
  
    var margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
  
    var color = d3.scaleThreshold()
      .domain([1,2,6,11,16,21,51,101,501,1001,1500000001])
      .range(["rgb(242, 242, 242)", "rgb(230, 247, 255)", "rgb(204, 239, 255)", 
      "rgb(128, 215, 255)", "rgb(26, 182, 255)", "rgb(0, 139, 204)", "rgb(0, 87, 128)",
      "rgb(0, 52, 77)", "rgb(0, 35, 51)","rgb(0, 17, 26)","rgb(0, 0, 0)"]);
      //.range(["rgb(247,251,255)", "rgb(222,235,247)", "rgb(198,219,239)", "rgb(158,202,225)", "rgb(107,174,214)", "rgb(66,146,198)","rgb(33,113,181)","rgb(8,81,156)","rgb(8,48,107)","rgb(3,19,43)"]);
  
    var svg = d3.select("#worldMap")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append('g')
      .attr('class', 'map');
  
    var projection = d3.geoMercator()
      .scale(130)
      .translate( [width / 2, height / 1.5]);
  
    var path = d3.geoPath().projection(projection);
    svg.call(mapTooltip);
  
    var itemsById = {};
  
    items.forEach(function(d) {
      itemsById[d.id] = d;
    });
    data.features.forEach(function(d) { 
      d.total_block_count = itemsById[d.id] ? itemsById[d.id].total_block_count: 0;
      d.key = itemsById[d.id] ? itemsById[d.id].key: null;
  
      d.count_per_day = [];
      if (itemsById[d.id] && itemsById[d.id]["count_per_day"]) {
        for (var key in itemsById[d.id]["count_per_day"]) {
          d.count_per_day.push({
            date : d3.timeParse("%Y-%m-%d")(key), 
            value : itemsById[d.id]["count_per_day"][key]
          });
        };
        d.count_per_day = d.count_per_day.sort(function(a,b) {
          return a.date - b.date;
        });
      }
    });
  
    svg.append("g")
        .attr("class", "countries")
      .selectAll("path")
        .data(data.features)
      .enter().append("path")
        .attr("d", path)
        .style("fill", function(d) { return color(d.total_block_count); })
        .style('stroke', 'white')
        .style('stroke-width', 1.5)
        .style("opacity",0.8)
        // tooltips
          .style("stroke","white")
          .style('stroke-width', 0.3)
          .on('mouseover',function(d){
            var divId = 'map' + d.id;
            mapTooltip.hide(d);
            mapTooltip.show(d);
            console.log(d);
            if(d.count_per_day && d.count_per_day.length){
              console.log('drawing');
              drawMapBlocksPerDateGraph(divId, d.count_per_day, "mapTooltipGraph", 300, 300);
            }
            d3.select(this)
              .style("opacity", 1)
              .style("stroke","white")
              .style("stroke-width",3);
          })
          .on('mouseout', function(d){
            d3.select(this)
              .style("opacity", 0.8)
              .style("stroke","white")
              .style("stroke-width",0.3);
          })
          .on("click", function(d){ 
            mapTooltip.hide(d);
            if (!d.key) return;
            var url = '/rc.html?key=' + d.key;
            window.open(url, '_blank');
          });
  
    svg.append("path")
      .datum(topojson.mesh(data.features, function(a, b) { return a.id !== b.id; }))
      .attr("class", "mapNames")
      .attr("d", path);
  }