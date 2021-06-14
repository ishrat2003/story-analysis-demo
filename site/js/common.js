var feedbackUrl = "http://127.0.0.1:3500";
var analysisUrl = "http://127.0.0.1:3500";
var source = 'tpl';

function countChar(val) {
  $('#charNum').text(val.value.length);
};

function getUrlParams(key){
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(key);       
}

function getCurrentDateTime(){
  var now = new Date();
  var date = now.getFullYear() + '-' + now.getMonth() + '-' + now.getDate();
  var time = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
  return date + ' ' + time;
}