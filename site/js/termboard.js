var dateFormat = 'yyyy-mm-dd';
var baseUrl = "http://127.0.0.1:3500";
var currentHost = "";
var source = 'tpl';

function getParams(){
    var queryString = window.location.search;
    queryString = decodeURIComponent(queryString.substring(1, queryString.length));
    var params = queryString.split("&");
    
    var topicKeys = [];
    var from, to, key, task;
    if(params.length){
        params.forEach(item => {
            if(item.includes("topic_keys")){
                topicKeys.push(item.replace(/topic_keys\[\]=/, ''));
            }else if(item.includes("from")){
                from = item.replace(/from\[\]=/, '');
            }else if(item.includes("to")){
                to = item.replace(/to\[\]=/, '');
            }else if(item.includes("task")){
                task = item.replace(/task\[\]=/, '');
            }if(item.includes("key")){
                key = item.replace(/key=/, '');
            }
        });
    }
    return [topicKeys, from, to, key, task];
}

function displayDocuments(documents){
    if(documents.length){
        documents.forEach(item => {
            var tbCondition = getUrlParams('condition');
            var tbKey = getUrlParams('key');
            var key = item.link.replace('https://www.bbc.co.uk/news/', '');
            key = item.link.replace('https://www.thepharmaletter.com/article/', '');
            var analysisLink = '/demo/lc.html?condition=all&key=' + key + '&tb_condition=' + tbCondition + '&tb_key=' + tbKey;
            var liHtml = '<li>'
                + '<h4>' + item.title + '</h4>'
                + '<span>' + item.date + '</span>'
                + '<p>' + item.description + '</p>'
                + '<p><a class="documentList" target="_blank" href="' + analysisLink + '">Local Context Analysis</a> |'
                + '<a class="documentListReference" target="_blank" href="' + item.link + '">Reference</a></p>'
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

function loadTermBoard(){
    var params = getParams();
    var data = {
        'topic_keys': params[0],
        'from': params[1],
        'to': params[2],
        'key': params[3],
        'task': params[4]
    };
    if (data['task']){
        $("#termsboardSurveyForm").show();
    }
    console.log(currentHost + "/data/" + source + "/termsboard/" + data['key'] + '.json');
    $.ajax({
        type: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
        url: currentHost + "/data/" + source + "/termsboard/" + data['key'] + '.json',
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
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log("error");
            console.log(XMLHttpRequest.responseText)
            console.log(textStatus);
            console.log(errorThrown );
        }
    });
}

function loadFormValidation(){
    $("form[id='termsboardSurveyForm']").validate({
        rules: {
            summary: { required: true, minlength: 500 } 
        },
        messages: {
            summary: {
                required: "This field is required"
            }
        },
        submitHandler: function(form) {
            populateEndTime();
            submitSurveyForm();
        }
    });
}

function submitSurveyForm(){
    if(!checkEase()) {
        return;
    }
    $('#termsboardSurveyFormSubmit').hide();
    $('#surveyLoading').show();

    var data = $('#termsboardSurveyForm').serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    
    $( "#error", "#message").html('');
    //console.log(data);
    $.ajax({
        url : feedbackUrl + "/feedback", // Url of backend (can be python, php, etc..)
        type: "POST", // data type (can be get, post, put, delete)
        dataType: 'json',
        data : JSON.stringify(data), // data in json format
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        success: function(response, textStatus, jqXHR) {
            var errors = null;
            if(response.body){
                var responseDetails = JSON.parse(response.body);
                if(responseDetails && responseDetails.result.errors){
                    errors = responseDetails.result.errors;
                }
            } 
            if(errors){
                $("#error").html(errors);
                $("#error").append('<p>Please make sure ypu have filled in the <a href="/experiment#participantEntry">participant details</a> before submitting the form.</p>');
                $('#termsboardSurveyForm, #termsboardSurveyFormSubmit').show();
                $('#surveyLoading').hide();
            }else{
                $( "#message" ).html('Thanks for the review.');
                $('#termsboardSurveyForm, #surveyLoading').hide();
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#termsboardSurveyForm, #termsboardSurveyFormSubmit').show();
            $('#surveyLoading').hide();
            $( "#error").html('Failed to save review.');
        }
    });
}

function checkEase(){
    $('#rating_error').html('');
    var valueChecked = $("input[name='ease']:checked").val();
    if(!valueChecked){
        $('#rating_error').append('<label class="error" for="ease">This field is required.</label>');
        return false;
    }
    return true;
}

$( function() {
    loadTermBoard();
    var condition = getUrlParams('condition');
    $('#condition').val(condition);
    if(condition == 'text'){
        $('.storyboard').hide();
    }
    $('#key').val(getUrlParams('key'));
    $('#story_term').val(getUrlParams('key'));

    if(condition != 'all'){
        loadFormValidation();
        $('#termsboardSurveyFormSubmit').on('click', function(){
            $('#termsboardSurveyForm').submit();
        });
    }
});