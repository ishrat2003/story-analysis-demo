
function displayGcTopics(data){
    data = data.reverse();
    var divId = "#dailyTopic";
  
    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 30, left: 100},
    width = 960 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom;
  
    // set the ranges
    var y = d3.scaleBand()
          .range([height, 0])
          .padding(0.1);
  
    var x = d3.scaleLinear()
          .range([0, width]);
  
    var tooltip = d3.select(divId).append("div").attr("class", "toolTip");
        
    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select(divId).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");
  
    // Scale the range of the data in the domains
    x.domain([0, d3.max(data, function(d){ return d.total_block_count; })])
    y.domain(data.map(function(d) { return d.display; }));
  
    // append the rectangles for the bar chart
    svg.selectAll(".topicBar")
      .data(data)
    .enter().append("rect")
      .attr("class", "topicBar")
      .attr("width", function(d) {return x(d.total_block_count); } )
      .attr("y", function(d) { return y(d.display); })
      .attr("height", y.bandwidth())
      .on("mousemove", function(d){
        var html = "<strong>Topic: </strong><span class='topicTooltipDetails'>" 
          + d.display + "<br></span>" 
          // + "<strong>Blocks count: </strong><span class='details'>" 
          // + d.total_block_count +"<br></span>"
          + "<strong>Blocks count in range: </strong><span class='details'>" 
          + d.total_block_count +"</span>";
        var divIdForGraph = 'topicItem' + d.key;
        if (d.linegraph) {
          html += "<div id=\"" + divIdForGraph+ "\" class=\"tooptipTopic\"></div>";
        }
        
        var countPerDay = [];
        if (d.linegraph) {
          d.linegraph.forEach(function(item){
            countPerDay.push({
              date : d3.timeParse("%Y-%m-%d")(item["date"]), 
              value : item["value"]
            });
          });
        }
        countPerDay = countPerDay.sort(function(a,b) {
            return a.date - b.date;
        });
        
        tooltip
          .style("left", d3.event.pageX + 50 + "px")
          .style("top", d3.event.pageY - 70 + "px")
          .style("display", "inline-block")
          .html(html);
          if(d.linegraph && d.linegraph.length){
            drawMapBlocksPerDateGraph(divIdForGraph, countPerDay, "topicTooltipGraph", 300, 300);
          }
      })
      .on("mouseout", function(d){ tooltip.style("display", "none");})
      .on("click", function(d){ 
        var url = '/demo/termsboard.html?key=' + d.key;
        window.open(url, '_blank');
      });
  
    // add the x Axis
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));
  
    // add the y Axis
    svg.append("g")
      .call(d3.axisLeft(y));
  }
  
  