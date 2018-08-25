function printTimer(labelID, checkboxID, secondsLeft){
    var hours = "";
    var minutes = "";
    var seconds = "";
    var timeout = new Date();

    // adding "+1" in order to print correct initial amount of second when the page loads and checkbox is set to manual
    timeout.setSeconds(timeout.getSeconds() + secondsLeft + 1);

    var countdownTimer = setInterval(function(){
        if (document.getElementById(checkboxID).checked == false){
            // console.log(document.getElementById(checkboxID).checked);
            clearInterval(countdownTimer);
        }

        var now = new Date();
        var myTimer = new Date(timeout - now);

        if (now <= timeout){
            hours = myTimer.getHours();
            minutes = myTimer.getMinutes();
            seconds = myTimer.getSeconds();

            hours = checkTimeFormat(hours);
            minutes = checkTimeFormat(minutes);
            seconds = checkTimeFormat(seconds);

            document.getElementById(labelID).innerHTML = hours + ":" + minutes + ":" + seconds;
        }
        if(now >= timeout)
            clearInterval(countdownTimer);
    },1000);
};

function secondsToTime(labelID, secs){
    var hours   = Math.floor(secs / 3600);
    var minutes = Math.floor((secs - (hours * 3600)) / 60);
    var seconds = secs - (hours * 3600) - (minutes * 60);

    hours = checkTimeFormat(hours);
    minutes = checkTimeFormat(minutes);
    seconds = checkTimeFormat(seconds);

    document.getElementById(labelID).innerHTML = hours + ":" + minutes + ":" + seconds;
};

function checkTimeFormat(i){
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
};