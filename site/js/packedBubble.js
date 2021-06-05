function displayPackedBubbles(divId, boxWidth, boxHeight, cardColor, data, displayOnlyChildrenLabel){
    var margin = {top: 20, right: 20, bottom: 30, left: 100},
    width = boxWidth - margin.left - margin.right,
    height = boxHeight - margin.top - margin.bottom,
    zoomMargin = 20;

    var tooltip = d3.select(divId).append("div").attr("class", "toolTipTermBoard");

    var svg = d3.select(divId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    var diameter = +svg.attr("width");
    var g = svg.append("g")
        .attr("transform", 
                "translate(" + diameter / 2 + "," + diameter / 2 + ")");

    var color = d3.scaleLinear()
        .domain([-1, 5])
        .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
        .interpolate(d3.interpolateHcl);

    var pack = d3.pack()
        .size([diameter - zoomMargin, diameter - zoomMargin])
        .padding(2);

    var root = d3.hierarchy(data)
        .sum(function(d) { return d.size; })
        .sort(function(a, b) { return b.value - a.value; });

    var focus = root,
        nodes = pack(root).descendants(),
        view;

    var circle = g.selectAll("circle")
        .data(nodes)
        .enter().append("circle")
            .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
            .style("fill", function(d) { 
                if (d.data.name == 'old_to_new') return '#858E8E';
                if (d.data.name == 'new_to_old') return '#D8E5E5';
                return d.children ? color(d.depth) : null; 
            });

    g.selectAll("circle").on("click", function(d) { 
        d3.select("#sankey").remove();
        $('#sankey').remove();
        $('#sankeyModal').modal();
        var listHtml = '<div id="sankeyList">'
        listHtml += '<h4>Top related sub-terms identified during document scanning </h4><br>';
        listHtml += 'Please <strong>click on a sub-terms link</strong> to see related documents representing sub-terms.';
        listHtml += '</div>';
        $('#sankeyModal').html('<a href="#" rel="modal:close" class="close">X</a><div><div id="sankey"></div>' + listHtml + '</div>')
        if(d.children.length){
            var relations = [];
            var combinedRelations = {};
            d.data.children.forEach(element => {
                if(element.relations){
                    element.relations.forEach(childElement => {
                        let relationIndex = relations.length;
                        var key = childElement["source"] + '_' + childElement["target"];
                        if(Object.keys(combinedRelations).includes(key)){
                            relationIndex = combinedRelations[key];
                            relations[relationIndex]['size'] += childElement['size'];
                            var allDocumentTitles = relations[relationIndex]['documents'].map(item => item.title);
                            childElement['documents'].forEach((document) => {
                                if(!allDocumentTitles.includes(document.title)){
                                    allDocumentTitles.append(document.title);
                                    relations[relationIndex]['documents'].append(document);
                                }
                            });
                        } else {
                            relations[relationIndex] = childElement;
                            combinedRelations[key] = relationIndex;
                        }
                    });
                }
            });
            // console.log(d.data.relations)
            if(relations){
                drawSankey('sankey', relations);
            }
        }
        //if (focus !== d) zoom(d), d3.event.stopPropagation(); 
    });
    

    g.selectAll("circle").on("mousemove", function(d){
        if (!d.data.children || !d.data.children.length) return;

        var heading = 'Consistent terms: ';
        var description = 'Terms that are used constiently in historical documents and lastest documents.';
        if (d.data.name == 'old_to_new') {
            var heading = 'Historical terms: ';
            var description = 'Terms that are used in historical documents mostly.';
        }
        if (d.data.name == 'new_to_old') {
            var heading = 'Latest terms: ';
            var description = 'Terms that are used in latest documents mostly.';
        }
        var html = "<strong>" + heading + "</strong><br><p>" + description + "</p><ul>";
        d.data.children.forEach(element => {
            html += '<li>' + element.name + ' (' + element.size + ') '+ '</li>';
        });
        html += '</ul>'
        
        tooltip
          .style("left", d3.event.pageX + 50 + "px")
          .style("top", d3.event.pageY - 70 + "px")
          .style("display", "inline-block")
          .html(html);
      })
      .on("mouseout", function(d){ tooltip.style("display", "none");});


    var text = g.selectAll("text")
        .data(nodes)
        .enter().append("text")
        .attr("class", "label")
        .style("fill-opacity", function(d) {
            return (d.children && d.children.length) ? 0 : 1;
        })
        .style("display", function(d) { 
            return (d.children && d.children.length) ? "none" : "inline";
        })
        .style("float", "center")
        .html(function(d) { 
            var name = d.data.name;
            if(name.length > 10){
                name = name.substring(0, 7) + '...';
            }
            return '<a href="#" rel="modal:open">' + name + '</a>'; 
        });

    var node = g.selectAll("circle,text");

    svg.style("background", cardColor);
    
    svg.on("click", function() { zoom(root); });
    

    zoomTo([root.x, root.y, root.r * 2 + zoomMargin]);

    function zoom(d) {
        var focus0 = focus; focus = d;
    
        var transition = d3.transition()
            .duration(d3.event.altKey ? 7500 : 750)
            .tween("zoom", function(d) {
              var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + zoomMargin]);
              return function(t) { zoomTo(i(t)); };
            });
    
        // transition.selectAll("text")
        //   .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
        //     .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
        //     .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
        //     .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
    }
    
    function zoomTo(v) {
        var k = diameter / v[2]; view = v;
        node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
        circle.attr("r", function(d) { return d.r * k; });
    }
}

