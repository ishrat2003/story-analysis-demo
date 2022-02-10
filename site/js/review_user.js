$(function() {
    $('.taskTab').on('click', function(){
        var taskId = $(this).data('task');
        $('.task').hide();
        $('#task' + taskId).show();
    });
    $('.tbTaskTab').on('click', function(){
        var taskId = $(this).data('task');
        $('.tbTask').hide();
        $('#tbTask' + taskId).show();
    });

    var code = getUrlParams('code');
    $.ajax({
        type: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
        url: '/data/users/' + code + '.json',
        success: function(result){
            console.log(result);
            $('#user_code .populateData').html(code);
            if(result['lc']){
                for (var key in result['lc']){
                    var element = result['lc'][key];
                    console.log(element);
                    var task = '.' + element['task_key'];
                    $(task + ' .key .populateData').html(element['task_key']);
                    $(task + ' .story_title .populateData').html(element['story_title']);
                    $(task + ' .when_happened .populateData').html(element['when_happened']);
                    $(task + ' .who .populateData').html(element['who']);
                    $(task + ' .what .populateData').html(element['what']);
                    $(task + ' .where_location .populateData').html(element['where_location']);
                    $(task + ' .why .populateData').html(element['why']);
                    $(task + ' .summary .populateData').html(element['summary']);
                }
            }
            if(result['tb']){
                for (var key in result['tb']){
                    var element = result['tb'][key];
                    console.log(element);
                    var task = '.' + element['task_key'];
                    $(task + ' .story_term .populateData').html(element['task_key']);
                    $(task + ' .summary .populateData').html(element['summary']);
                }
            }
        },
        dataType: 'json',
        error: function () {
            console.log("error");
        }
        });
  });