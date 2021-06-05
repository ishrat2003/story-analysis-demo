var dateFormat = 'yyyy-mm-dd';
var baseUrl = "http://127.0.0.1:3500";

function getParams(){
    var queryString = window.location.search;
    queryString = decodeURIComponent(queryString.substring(1, queryString.length));
    var params = queryString.split("&");
    
    var topicKeys = [];
    var from, to, key;
    if(params.length){
        params.forEach(item => {
            if(item.includes("topic_keys")){
                topicKeys.push(item.replace(/topic_keys\[\]=/, ''));
            }else if(item.includes("from")){
                from = item.replace(/from\[\]=/, '');
            }else if(item.includes("to")){
                to = item.replace(/to\[\]=/, '');
            }if(item.includes("key")){
                key = item.replace(/key=/, '');
            }
        });
    }
    return [topicKeys, from, to, key];
}

function displayDocuments(documents){
    if(documents.length){
        documents.forEach(item => {
            var key = item.link.replace('https://www.bbc.co.uk/news/', '');
            var analysisLink = '/demo/lc.html?condition=all&key=' + key;
            var liHtml = '<li>'
                + '<h4>' + item.title + '</h4>'
                + '<span>' + item.date + '</span>'
                + '<p>' + item.description + '</p>'
                + '<p><a target="_blank" href="' + analysisLink + '">Local Context Analysis</a> | <a target="_blank" href="' + item.link + '">BBC Reference</a></p>'
                + '</li>';
            $("#documentsItems").append(liHtml);
        });
    }
}

function drawWhenBarChart(rows){
    var data = rows.map(function(d) { 
        return {
            date : d3.timeParse("%Y-%m-%d")(d.date), 
            value : d.value
        }
    });

    drawMapBlocksPerDateGraph('whenBox', data, "whenBarChart", 365, 300);
}

function drawBubbleCard(data, cardColor, divId){
    var children = [];
    ['consistent', 'old_to_new', 'new_to_old'].forEach(node => {
        if(data[node] && data[node].length){
            children.push({
                "name": node,
                "children": data[node],
                "relations": data[node + '_relations']
            });
        }
    });

    if(!children.length) return;
    var processedData = {
        "name": "terms",
        "children": children
    }
    displayPackedBubbles("#" + divId, 330, 330, cardColor, processedData, true);   
}

function loadTermBoard(order, direction){
    var params = getParams();
    var data = {
        'topic_keys': params[0],
        'order': order,
        'direction': direction,
        'from': params[1],
        'to': params[2],
        'key': params[3]
    };
    $.ajax({
        type: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
        url: "/data/termsboard/" + data['key'] + '.json',
        success: function(result){
            $(".termboardBox, #documentsItems").html("");
            if(result && result['description']){
                $('#termBoardDescription').text(result['description']);
            }
            if(result && result['documents']){
                displayDocuments(result['documents']);
            }
            if(result && result['when']){
                drawWhenBarChart(result['when']);
            }
            if(result && result['board'] && result['board']['who']){
                drawBubbleCard(result['board']['who'], '#e6ffb3', 'whoBox');
            }
            if(result && result['board'] && result['board']['where']){
                drawBubbleCard(result['board']['where'], '#88cc00', 'whereBox');
            }
            if(result && result['board'] && result['board']['what_topic']){
                drawBubbleCard(result['board']['what_topic'], '#e6ffb3', 'whatTopicBox');
            }
            if(result && result['board'] && result['board']['what_action']){
                drawBubbleCard(result['board']['what_action'], '#88cc00', 'whatActionBox');
            }
            if(result && result['board'] && result['board']['why_positive']){
                drawBubbleCard(result['board']['why_positive'], '#e6ffb3', 'whyPositiveBox');
            }
            if(result && result['board'] && result['board']['why_negative']){
                drawBubbleCard(result['board']['why_negative'], '#88cc00', 'whyNegativeBox');
            }
        },
        dataType: 'json',
        error: function () {
            console.log("error");
        }
    });
}

$( function() {
    loadTermBoard('score', 'desc');

    $('#orderDocument').on('change', function(){
        var selectedValue = $(this).val();
        if(selectedValue == 'date_asc'){
            loadTermBoard('date', 'asc');
        }else if(selectedValue == 'date_desc'){
            loadTermBoard('date', 'desc');
        }else{
            loadTermBoard('score', 'desc');
        }
    });
});