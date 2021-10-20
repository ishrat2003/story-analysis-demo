var feedbackUrl = "https://247dtw4y0i.execute-api.eu-west-1.amazonaws.com/Production";
//var feedbackUrl = "http://127.0.0.1:3500";
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

$(function() {
  $.gdprcookie.init({
      title: "Cookies & Privacy Policy",
      message: "<p style='text-align:justify'>This site uses cookies to understand the use of terms in reading and writing." +
      " This is an academic site. The collected user experience is used for academic analysis." +
      " This site doesn’t preserve any user identifiable information. Collected data is anonymized." +
      " Please accept the cookies and the privacy policy to continue.</p>"
      
  });
  
});