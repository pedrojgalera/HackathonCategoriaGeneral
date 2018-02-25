
var jq = document.createElement('script');
jq.src="https:ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);

function loadJQuery(){

var waitForLoad = function () {
    if (typeof jQuery != "undefined") {
        console.log("jquery loaded..");
        // invoke any methods defined in your JS files to begin execution
        $('body').css('background','url(https://youngdentistrydelray.com/wp-content/uploads/2016/09/young-dentistry-office-tour-photo-6.jpg)');

    $('body').css('background-size','cover');
    $('body').css('background-opacity','0.4');
    } else {
        console.log("jquery not loaded..");
        window.setTimeout(waitForLoad, 500);
    }
 };
 window.setTimeout(waitForLoad, 500);   
}

//window.onload = loadJQuery;
loadJQuery();
