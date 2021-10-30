function populateUserData(){
    $('#user_code').val(localStorage.getItem('user_code'));
    $('#gender').val(localStorage.getItem('gender'));
    $('#age_group').val(localStorage.getItem('age_group'));
    $('#experiment_date_datepicker').val(localStorage.getItem('experiment_date_datepicker'));
    $('#agreed').val(localStorage.getItem('agreed'));
    $('#level').val(localStorage.getItem('level'));
    $('#department').val(localStorage.getItem('department'));
    $('#dob_datepicker').val(localStorage.getItem('dob_datepicker'));
    $('#disability').val(localStorage.getItem('disability'));
}

function populateOpenTime(){
    $('#open_timestamp').val(Date.now());
    $('#open_date_time').val(getCurrentDateTime());
}

function populateEndTime(){
    var end = Date.now();
    $('#close_timestamp').val(end);
    $('#close_date_time').val(getCurrentDateTime());

    var start = $('#open_timestamp').val();
    var diff = end - start;
    $('#time_taken_in_seconds').val(diff);
}

function getSelectionText() {
    var text = '';
    if (window.getSelection) {
      text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != 'Control') {
      text = document.selection.createRange().text;
    }
    return text;
}

var dataLayer = [];

$(function() {
    dataLayer.push({'user_code': localStorage.getItem('user_code')});
    dataLayer.push({'title': $('title').text()});
    
    populateUserData();
    populateOpenTime();

    // Declare function on copy event
    document.addEventListener('copy', function(e){
        var copiedFrom = 'Unknown';
        if (e.target.id) copiedFrom = e.target.id;
        else if (e.target.parentElement.id) copiedFrom = e.target.parentElement.id;
        else if (e.target.parentElement.parentElement.parentElement.parentElement.parentElement.id) copiedFrom = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.id;

        dataLayer.push({
            'event': 'text_copied',
            'clipboard_text': getSelectionText(),
            'clipboard_length': getSelectionText().length,
            'copied_from': copiedFrom.replace('#', '')
        });
        
    });
});