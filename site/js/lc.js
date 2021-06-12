const feedbackUrl = "http://127.0.0.1:3500";
const analysisUrl = "http://127.0.0.1:3500";

var lcColor = {
    "proper_noun": "#2d7b30",
    "noun": "#259328bf",
    "adjective": "#f58207",
    "adverb": "#616361",
    "verb": "#181b1d",
    "positive": "#ffd700",
    "negative": "#f71f07",
    "person": "#1b2bde",
    "location": "#784698",
    "organization": "#43a9a7",
    "others": "#5e615e",
    "time": "#FFA533"
};

var kgColor = {
    "organization": "#43a9a7",
    "time": "#FFA533",
    "person": "#1b2bde",
    "location": "#784698",
    "others": "#5e615e",
    "default": "#259328bf"
  };

function getUrlParams(key){
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(key);       
}
  
function displayLc(data, statFiedName){
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = 600 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom,
    innerRadius = 150,
    outerRadius = Math.min(width, height) / 4;   // the outerRadius goes from the middle of the SVG area to the border

    d3.select("#lcVizualization").select("div").remove();

    // append the svg object
    var svg = d3.select("#lcVizualization")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + (width / 2 + margin.left) + "," + (height / 2 + margin.top) + ")");

    var tooltip = d3.select("#lcVizualization").append("div")	
        .attr("class", "tooltip")				
        .style("opacity", 1);

    // X scale: common for 2 data series
    var x = d3.scaleBand()
        .range([0, 2 * Math.PI])    // X axis goes from 0 to 2pi = all around the circle. If I stop at 1Pi, it will be around a half circle
        .align(0)                  // This does nothing
        .domain(data.map(function(d) { return d.pure_word  + '-' + d.count; })); // The domain of the X axis is the list of states.

    // Y scale outer variable
    var y = d3.scaleRadial()
        .range([innerRadius, outerRadius])   // Domain will be define later.
        .domain([0, 100]); // Domain of Y is from 0 to the max seen in the data

    // Second barplot Scales
    var ybis = d3.scaleRadial()
        .range([innerRadius, 1])   // Domain will be defined later.
        .domain([0, 100]);

    //Add the labels
    svg.append("g")
        .selectAll("g")
        .data(data)
        .enter()
        .append("g")
        .style("fill", function(d){return lcColor[d.color_group];})
        .attr("text-anchor", function(d) { return (x(d.pure_word + '-' + d.count) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
        .attr("transform", function(d) { return "rotate(" + ((x(d.pure_word + '-' + d.count) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d[statFiedName])+10) + ",0)"; })
        .append("text")
        .text(function(d){return(d.pure_word + '-' + d.count)})
        .attr("transform", function(d) { return (x(d.pure_word + '-' + d.count) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
        .style("font-size", "15px")
        .attr("alignment-baseline", "middle");

    //Add the second series
    svg.append("g")
        .selectAll("path")
        .data(data)
        .enter()
        .append("path")
        .attr("fill", function(d) { return lcColor[d.color_group]; })
        .attr("d", d3.arc()     // imagine your doing a part of a donut plot
        .innerRadius( function(d) { return ybis(0) })
        .outerRadius( function(d) { return ybis(d[statFiedName]); })
        .startAngle(function(d) { return x(d.pure_word + '-' + d.count); })
        .endAngle(function(d) { return x(d.pure_word + '-' + d.count) + x.bandwidth(); })
        .padAngle(0.01)
        .padRadius(innerRadius));

        svg.selectAll('text')
        .on("mouseover", function(d) {
            var html = '<h3 style="color:green;" class="center">' + d.pure_word + '</h3>'
                + '<b>Category: </b>' + ( d.category || d.type || '') + '<br>'
                + '<b>Sentiment: </b>' + ( d.sentiment || '') + '<br>'
                + '<b>Occurrence: </b>' + d.count + '<br>'
                + '<b>Forward position weight: </b>' + d.position_weight_forward.toFixed(2) + '<br>'
                + '<b>Backward position weight: </b>' + d.position_weight_backward.toFixed(2) + '<br>';
            if (d.tooltip !== d.pure_word){
                html += '<p>' + d.tooltip + '</p>';
            }
            
            tooltip.style("display", "inline");	
            tooltip.transition()		
                .duration(200)		
                .style("opacity", .9);		
            tooltip.html(html);	
            dataLayer.push({
                'event': 'mouseover_lc_term',
                'lc_pure_word': d.pure_word,
                'lc_category': d.category
            });
        })					
        .on("mouseout", function(d) {
            tooltip.style("display", "none");		
            tooltip.transition()
                .duration(500)		
                .style("opacity", 0);	
        })
}

function showRaw(data){
    $('.lcRawRow, #lcRawTop').html('');
    $('#lcRawTop').prepend('<h3>' + data['concepts']['story_what_about'] + ' <a href="#lcRawBlock">Check extracted concepts</a></h3>');
    
    $('#lcRawRow1').append(getProperNoun(data['concepts']['topic_words'], 'Topics'));

    if (data['concepts']['categories']['Person']) {
        $('#lcRawRow1').append(getCategoryWords(data['concepts']['categories']['Person'], 'Person'));
    }

    if (data['concepts']['categories']['Location']) {
        $('#lcRawRow1').append(getCategoryWords(data['concepts']['categories']['Location'], 'Location'));
    }

    if (data['concepts']['categories']['Organization']) {
        $('#lcRawRow1').append(getCategoryWords(data['concepts']['categories']['Organization'], 'Organization'));
    }

    $('#lcRawRow2').append('<br class="clear">');

    if (data['concepts']['categories']['Time']) {
        $('#lcRawRow2').append(getCategoryWords(data['concepts']['categories']['Time'], 'Time'));
    }

    if (data['concepts']['categories']['Others']) {
        $('#lcRawRow2').append(getCategoryWords(data['concepts']['categories']['Others'], 'Others'));
    }

    if (data['concepts']['sentiment']['positive']) {
        $('#lcRawRow2').append(getCategoryWords(data['concepts']['sentiment']['positive'], 'Positive'));
    }

    if (data['concepts']['sentiment']['negative']) {
        $('#lcRawRow2').append(getCategoryWords(data['concepts']['sentiment']['negative'], 'Negative'));
    }
}

function getProperNoun(items, title){
    html = '<div class="storyWordCategory">'
    html += '<h3  class="properNoun">' + title + '</h3>';
    html += '<div class="properNoun">';
    divider = '';
    items.forEach(item => {
        html += divider + '<span>' + item + '</span>';
        divider = ', ';
    });
    html += '</div>';
    html += '</div>';
    return html;
}

function getWords(items, className){
    if(!items) return;

    html = '<div class="storyWordCategory">'
    html += '<h3 class="' + className.toLowerCase() + '">' + className + '</h3>';
    html += '<div class="' + className.toLowerCase() + '">';

    divider = '';
    items.forEach(item => {
        html += divider + '<span>' + item['pure_word'] + '</span> (' + item['count'] + ')';
        divider = ', ';
    });

    html += '</div>';
    html += '</div>';
    return html;
}

function getCategoryWords(items, className){
    if(!items) return;

    html = '<div class="storyWordCategory">'
    html += '<h3 class="' + className.toLowerCase() + '">' + className + '</h3>';
    html += '<div class="' + className.toLowerCase() + '">';

    divider = '';
    items.forEach(item => {
        html += divider + '<span>' + item + '</span>';
        divider = ', ';
    });

    html += '</div>';
    html += '</div>';
    return html;
}

function getCurrentDateTime(){
    var now = new Date();
    var date = now.getFullYear() + '-' + now.getMonth() + '-' + now.getDate();
    var time = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
    return date + ' ' + time;
}
function loadCommonDetails(data, condition) {
    var description = '';
    if(condition == 'text'){
        description = "In this task, read the given text and then answer the given questions."
    } else if(condition == 'viz'){
        description = "In this task, interpret the visualization and then answer the given questions."
     }
    $('#story_source').val('bbc');
    $('#condition').val(condition);
    $('#story_date').val(data['pubDate']);
    $('#story_link').val(data['link']);
    $('#story_title').val(data['title']);
    $('#taskTitle').text(data['title']);
    $('#taskDescription').text(description);
    $('#lc_' + condition).show();
}

function loadLcText(data){
    $('#lc_text_display').html(data['content']);
    $('#lc_text').show();
}

function loadLcViz(data){
    var lcResponse = data;
    lcResponse['concepts']['story_words'][0]['pure_word'] = '← - ' + lcResponse['concepts']['story_words'][0]['pure_word'];
    $('#lcLoading').hide();
    $('#lcVizualization').html('');
    displayLc(lcResponse['concepts']['story_words'], 'position_weight_forward');
    
    $('#storySurveyForm').show();
    $('.lcRawRow').show();

    $('#lc_viz, .lcVizualization').show();
    $('#lc_viz_display .loadingImage').hide();
    $('#taskTitle').text(lcResponse['title']);
}

function loadKnowledgeGraph(data){
    var lcResponse = data;
    $('#knowledgegraph').show();
    $('#knowledgegraphLoading').show();
    if (lcResponse['concepts']['graph']) {
        displayKnowledgeGraph(lcResponse['concepts']['graph']['links'], lcResponse['concepts']['graph']['nodes']);
        $('#knowledgegraphLoading').hide();
    }

    $('.loadingImage').hide();
    $('#lc_viz, #lcTitle, .lcRawRow').show();
}

function load(condition, data){
    $('#lc_viz, .lcVizualization, #knowledgegraph, #lc_text').hide();

    if (!data) {
        return;
    }
    
    showRaw(data);
    if(condition == 'viz'){
        loadLcViz(data);
        $('#lc_text_questions').show();
    }else if(condition == 'text'){
        loadLcText(data);
        $('#lc_text_questions').show();
    }else if(condition == 'graph'){
        loadKnowledgeGraph(data);
        $('#knowledgegraph').show();
        $('#knowledgegraphLoading').show();
    }else if(condition == 'all'){
        loadLcViz(data);
        loadLcText(data);  
    }else{
        loadLcViz(data);
        loadKnowledgeGraph(data);
        loadLcText(data);  
    }
    
    var date = data['pubDate'].substring(0, 10);
    var dateParts = date.split("-")
    $('#publishedDate').html(dateParts[2] + '/' + dateParts[1] + '/' + dateParts[0]);
}

function fetchAndLoad(condition){
    $.ajax("/data/lc/" + getUrlParams('key') + '.json', {
        method: "GET",
        contentType: "application/json"
    }).done(function (data) {
        loadCommonDetails(data, condition);
        load(condition, data);
    });
}

function displayKnowledgeGraph(links, nodes) {
    var margin = {top: 10, right: 10, bottom: 10, left: 10},
        width = 800 - margin.left - margin.right,
        height = 800 - margin.top - margin.bottom;

    d3.select("#knowledgegraphVizualization").select("svg").remove();
    d3.select("#knowledgegraphVizualization").select("div").remove();

    var svg = d3.select("#knowledgegraphVizualization")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g");
    var tooltip = d3.select("#knowledgegraphVizualization").append("div")	
        .attr("class", "tooltip")				
        .style("opacity", 0);
  
    svg.append('defs').append('marker')
        .attrs({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':13,
            'refY':0,
            'orient':'auto',
            'markerWidth':13,
            'markerHeight':13,
            'xoverflow':'visible'})
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke','none');

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(100).strength(1))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    var link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr('marker-end','url(#arrowhead)')

    link.append("title")
        .text(function (d) {return d.type;});

    edgepaths = svg.selectAll(".edgepath")
        .data(links)
        .enter()
        .append('path')
        .attrs({
            'class': 'edgepath',
            'fill-opacity': 0,
            'stroke-opacity': 0,
            'id': function (d, i) {return 'edgepath' + i}
        })
        .style("pointer-events", "none");

    edgelabels = svg.selectAll(".edgelabel")
        .data(links)
        .enter()
        .append('text')
        .style("pointer-events", "none")
        .attrs({
            'class': 'edgelabel',
            'id': function (d, i) {return 'edgelabel' + i},
            'font-size': 10,
            'fill': '#aaa'
        });

    edgelabels.append('textPath')
        .attr('xlink:href', function (d, i) {return '#edgepath' + i})
        .style("text-anchor", "middle")
        .style("pointer-events", "none")
        .style("fill", function(d){return kgColor[d.color];})
        .attr("startOffset", "50%")
        .text(function (d) {return d.type});
        

    var node = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node");
        // .call(d3.drag()
        //         .on("start", dragstarted)
        //         .on("drag", dragged)
        //         //.on("end", dragended)
        // );

    node.append("circle")
        .attr("r", 5)
        .style("fill", function (d, i) {return kgColor[d.color];})

    node.append("title")
        .text(function (d) {return d.id;});

    node.append("text")
        .attr("dy", -3)
        .text(function (d) {return d.name})
        .on("mouseover", function(d) {		
            tooltip.transition()		
                .duration(200)		
                .style("opacity", .9);		
            tooltip.html(
                '<b>' + d.name + '</b></br>'
                + '<b>' + d.label + '</b></br>'
                + '<p>' + d.tooltip + '</p>'
                )	
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 28) + "px");	
            })					
        .on("mouseout", function(d) {		
            tooltip.transition()
                .duration(500)		
                .style("opacity", 0);	
        });

    simulation
        .nodes(nodes)
        .on("tick", function() {
            link
                .attr("x1", function (d) {return d.source.x;})
                .attr("y1", function (d) {return d.source.y;})
                .attr("x2", function (d) {return d.target.x;})
                .attr("y2", function (d) {return d.target.y;});
        
            node
                .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});
        
            edgepaths.attr('d', function (d) {
                return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
            });
        
            edgelabels.attr('transform', function (d) {
                if (d.target.x < d.source.x) {
                    var bbox = this.getBBox();
        
                    rx = bbox.x + bbox.width / 2;
                    ry = bbox.y + bbox.height / 2;
                    return 'rotate(180 ' + rx + ' ' + ry + ')';
                }
                else {
                    return 'rotate(0)';
                }
            });
        });

    simulation.force("link")
        .links(links);
}

function submitContentForm(){
    var condition = 'viz';
    $('#lc_' + condition).show();
    $(window).scrollTop(0);
    $.ajax(analysisUrl + "/lc", {
        data: JSON.stringify({
            'title': $("#title").val(),
            'content': $("#content").val(),
            'pubDate': $("#pubDate").val()
        }),
        method: "POST",
        contentType: "application/json"
    }).done(function (data) {
        //localStorage.setItem('content_input', JSON.stringify(data));
        load(condition, data);
        if (data['concepts']['graph']) {
            $('#knowledgegraph').show();
            displayKnowledgeGraph(data['concepts']['graph']['links'], data['concepts']['graph']['nodes']);
        }
    });
}

function registerContentFormValidation(){
    $("form[id='lcContentForm']").validate({
        rules: {
            title: {
                required: true,
                minlength: 10
            },
            pubDate: {
                required: true,
                story_date: true
            },
            content: {
                required: true,
                minlength: 500
            }
        },
        // Specify validation error messages
        messages: {
            title: {
                required: "Please enter title",
                minlength: jQuery.validator.format("At least {0} characters required!")
            },
            pubDate: {
                required: "Please enter published date"
            },
            content: {
                required: "Please enter content",
                minlength: jQuery.validator.format("At least {0} characters required!")
            }
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            submitContentForm();
        }
    });
}

function loadLcSurveyFormValidation(){
    $("form[id='storySurveyForm']").validate({
        rules: {
            when_happened: { required: true },
            who: { required: true, minlength: 5 },
            what: { required: true, minlength: 5 },
            where_location: { required: true, minlength: 5 },
            why: { required: true, minlength: 5, easeCheck: true },
            summary: { required: true, minlength: 100 } 
        },
        submitHandler: function(form) {
            populateEndTime();
            submitSurveyForm();
        }
    });
}

function submitSurveyForm(){
    $('#storySurveyFormSubmit').hide();
    $('#surveyLoading').show();

    var data = $('#storySurveyForm').serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    
    $( "#error", "#message").html('');
    $.ajax({
        url : feedbackUrl + "/survey", // Url of backend (can be python, php, etc..)
        type: "POST", // data type (can be get, post, put, delete)
        dataType: 'json',
        data : JSON.stringify(data), // data in json format
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        success: function(response, textStatus, jqXHR) {
            if(response.result.errors){
                $("#error").html(response.result.errors);
                $('#storySurveyForm, #storySurveyFormSubmit').show();
                $('#surveyLoading').hide();
            }else{
                $( "#message" ).html('Thanks for the review.');
                $('#storySurveyForm, #surveyLoading').hide();
            }
            $("html").animate({ scrollTop: $("#lc_text_questions").offset().top }, "slow");
            
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#storySurveyForm, #storySurveyFormSubmit').show();
            $('#surveyLoading').hide();
            $( "#error").html('Failed to save review.');
            $("html").animate({ scrollTop: $("#lc_text_questions").offset().top }, "slow");
        }
    });
}

$.validator.addMethod("easeCheck", function(value, element) {
    $('#rating_error').html('');
    var valueChecked = $("input[name='ease']:checked").val();
    if(!valueChecked){
        $('#rating_error').append('<label class="error" for="ease">This field is required.</label>');
    }
    return true;
}, "");


$(function() {
    var condition = getUrlParams('condition');
    var key = getUrlParams('key');
    
    if($('#lcContentForm').length){
        registerContentFormValidation();
        $('#lcContentFormSubmit').on('click', function(){
            $('#lcContentForm').submit();
        });
    }else{
        if(condition != 'all'){
            loadLcSurveyFormValidation();
            $('#storySurveyFormSubmit').on('click', function(){
                $('#storySurveyForm').submit();
            });
        }

        fetchAndLoad(condition, key);
        
    }
});

