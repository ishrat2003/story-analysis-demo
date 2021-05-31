var dateFormat = 'yy-mm-dd';

function setDate(dateString, divId){
    var dateParts = dateString.split("-")
    $(divId).datepicker('setDate', new Date(dateParts[0], dateParts[1], dateParts[2]));
}

function getGcDateData(){
    return {
        "start": $('#from_datepicker').datepicker({ dateFormat: dateFormat }).val(),
        "end": $('#to_datepicker').datepicker({ dateFormat: dateFormat }).val()
    };
}

function fillToday(){
    var today = new Date();
    var todayString = today.getFullYear() + '-' + getDoubleDigit(today.getMonth() + 1) + '-' + getDoubleDigit(today.getDate());
    $('#from_datepicker').val(todayString);
    $('#to_datepicker').val(todayString);
}

function getDoubleDigit(numberString){
    return String(numberString).padStart(2, '0');
}

$( function() {
    $.validator.addMethod("story_date", function(value, element) {
        return this.optional(element) || /^[0-9]{4}\-[0-9]{2}\-[0-9]{2}/.test(value);
    }, "Please specify correct date. Ex: 2021-11-11");

    $( ".datepicker" ).datepicker({ dateFormat: dateFormat });
});
