var rcTopics = [
    ["case1", "case2"],
    ["case2", "case1"]
];

function getTasks(taskConditions, topics, tasksPerCondition, prefix){
    var allTasks = {};
    var count = 0;
    $.each(taskConditions, function( index, textOrViz ) {
        textOrViz = prefix + textOrViz;
        if(!allTasks[textOrViz]){
            allTasks[textOrViz] = [];
        }
        $.each(topics, function( topicIndex, task ) {
            if (topicIndex < count) {
                return;
            }
            if (allTasks[textOrViz].length >= tasksPerCondition){
                return;
            }
            allTasks[textOrViz].push(task);
            count++;
        });
    });

    return allTasks;
}

function getTopicsForSession(latinSquareDistribution, totalTopics){
    var userId = localStorage.getItem('user_id');
    var topicsIndex = userId % totalTopics;
    return latinSquareDistribution[topicsIndex]
}

function loadLcTasks(taskConditions, totalCondition){
    var latinSquareDistribution = [
        ["case1", "case2", "case3", "case4"],
        ["case2", "case3", "case4", "case1"],
        ["case3", "case4", "case1", "case2"],
        ["case4", "case1", "case2", "case3"]
    ];
    var totalTasksPerCondition = latinSquareDistribution[0].length / totalCondition;
    var topics = getTopicsForSession(latinSquareDistribution, latinSquareDistribution[0].length);
    return getTasks(taskConditions, topics, totalTasksPerCondition, 'lc_');
}

function loadRcTasks(taskConditions, totalCondition){
    var latinSquareDistribution = [
        ["case1", "case2"],
        ["case2", "case1"]
    ];
    var totalTasksPerCondition = latinSquareDistribution[0].length / totalCondition;
    var topics = getTopicsForSession(latinSquareDistribution, latinSquareDistribution[0].length);
    return getTasks(taskConditions, topics, totalTasksPerCondition, 'termsboard_');
}

function loadTasks(){
    var conditions = [
        ['text', 'viz'],
        ['viz', 'text']
    ];
    
    var userId = localStorage.getItem('user_id');
    if(!userId){
        alert("Please fill in participant details for loading tasks.");
        window.location.href = "/experiment";
        return;
    }
    var conditionIndex = userId % conditions[0].length;
    var taskConditions = conditions[conditionIndex];
    const lcTasks = loadLcTasks(taskConditions, conditions[0].length);
    const rcTasks = loadRcTasks(taskConditions, conditions[0].length);
    const tasks = Object.assign(lcTasks, rcTasks);

    $.getJSON( "/data/tasks.json", function( data ) {
        $.each(Object.keys(tasks), function( index, taskType ) {
            var realIndex = index + 1;
            var type = taskType.replace(/_[a-z]+/, '');
            var condition = taskType.replace(/[a-z]+_/, '');
            var pId = '#task' + realIndex + 'P';
            var ulId = '#task' + realIndex + 'Ul';
            $(pId).text(data[taskType]['description']);
            $.each(tasks[taskType], function(taskIndex, taskName ) {
                var href = encodeURI("/demo/" + type + ".html?condition=" + condition 
                    + "&task=" + taskName + "&key=" 
                    + data[type][taskName]['key']);
                $(ulId).append('<li><a href="' + href + '">' + data[type][taskName]['title'] + '</a></li>');
            });
        });
    });

}


$( function() {
    loadTasks();
});