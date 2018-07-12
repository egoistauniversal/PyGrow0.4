function createCountdownRow(program_id, name, state, automatic){
    // creates <tbody> element
    var myTableBody = document.createElement("TBODY");

    // creating row
    var myRow = document.createElement("TR");

    // creates a <td> element
    var myNameLabelCell = document.createElement("TD");
    var myTimeLabelCell = document.createElement("TD");
    var myStateButtonCell = document.createElement("TD");
    var myResetButtonCell = document.createElement("TD");
    var myCheckboxCell = document.createElement("TD");

    // creates name Label element
    var myNameLabel = document.createElement("LABEL");
    myNameLabel.id = "countdownNameLabel" + program_id;
    var myNameTextNode = document.createTextNode(name + "-" + program_id);
    myNameLabel.appendChild(myNameTextNode);

    // creates time Label element
    var myTimeLabel = document.createElement("LABEL");
    myTimeLabel.id = "countdownTimeLabel" + program_id;
    // myTimeLabel.dataset.timeleft = "test1";
    // myTimeLabel.setAttribute('data-newtime', 'test2');

    // creates button element "State"
    var myStateButton = document.createElement('input');
    myStateButton.type = 'button';
    myStateButton.id = "countdownStateButton" + program_id;
    if (state == 0){myStateButton.value = 'OFF';}
    else{myStateButton.value = 'ON';}
    myStateButton.addEventListener('click', function(){
        clickCountdownStateButton(program_id, myStateButton.id);
    });

    // creates button element "Reset"
    var myResetButton = document.createElement('input');
    myResetButton.type = 'button';
    myResetButton.id = "countdownResetButton" + program_id;
    myResetButton.value = "Reset";
    myResetButton.addEventListener('click', function(){
        clickCountdownResetButton(program_id);
    });

    // creates a label for checkbox ...
    var myAutomaticLabel = document.createElement("LABEL");
    myAutomaticLabel.id = "countdownAutomaticLabel" + program_id;

    // creates a checkbox
    var myCheckbox = document.createElement("input");
    myCheckbox.type = 'checkbox';
    myCheckbox.id = "countdownCheckbox" + program_id;
    if (automatic == 0){
        myCheckbox.checked = false;
        var myAutomaticTextNode = document.createTextNode("Manual");
    }
    else {
        myCheckbox.checked = true;
        var myAutomaticTextNode = document.createTextNode("Automatic");
    }
    myCheckbox.addEventListener('change', function(){
        enableDisableCountdownButton(myCheckbox, myStateButton.id, myResetButton.id);
        changeCountdownAutomaticLabelText(myCheckbox.checked, myAutomaticLabel.id, program_id);
    });

    //... creates a label for checkbox ...
    myAutomaticLabel.htmlFor = myCheckbox.id;
    myAutomaticLabel.appendChild(myAutomaticTextNode);

    // appends the elements we created into the cell <td>
    myNameLabelCell.appendChild(myNameLabel);
    myTimeLabelCell.appendChild(myTimeLabel);
    myStateButtonCell.appendChild(myStateButton);
    myResetButtonCell.appendChild(myResetButton);
    myCheckboxCell.appendChild(myCheckbox);
    myCheckboxCell.appendChild(myAutomaticLabel);

    // appends the cell <td> into the row <tr>
    myRow.appendChild(myNameLabelCell);
    myRow.appendChild(myTimeLabelCell);
    myRow.appendChild(myStateButtonCell);
    myRow.appendChild(myResetButtonCell);
    myRow.appendChild(myCheckboxCell);

    // appends the row <tr> into the TableBody
    myTableBody.appendChild(myRow);

    return myTableBody;
};

function toggleCountdownButton(buttonID){
    var elem = document.getElementById(buttonID);
    if (elem.value=="OFF"){
        // elem.style.backgroundColor = '#ccffcc';
        elem.value = "ON";
    }
    else {
        // elem.style.backgroundColor = '';
        elem.value = "OFF";
    }
};

function clickCountdownStateButton(program_id, buttonID){
    toggleCountdownButton(buttonID);
    socket.emit('countdown_change_state_manual', {program_id: program_id});
};

function clickCountdownResetButton(program_id){
    socket.emit('countdown_reset', {program_id: program_id});
}

function enableDisableCountdownButton(checkbox, stateButtonID, resetButtonID) {
    if(checkbox.checked == false){
        document.getElementById(stateButtonID).disabled = false;
        document.getElementById(resetButtonID).disabled = false;
    }
    else{
        document.getElementById(stateButtonID).disabled = true;
        document.getElementById(resetButtonID).disabled = true;
    }
};

function changeCountdownAutomaticLabelText(checked, labelID, program_id){
    if (checked == true){
        document.getElementById(labelID).innerHTML = "Automatic";
        // emit module program_id to resume timer
        socket.emit('resume_countdown_timer', {program_id: program_id});
        //console.log('module countdown ' + program_id + ' timer resumed');
    }
    else{
        // set countdown module to manual
        document.getElementById(labelID).innerHTML = "Manual";
        // emit module program_id to pause timer
        socket.emit('pause_countdown_timer', {program_id: program_id});
        //console.log('module countdown ' + program_id + ' timer paused');
    }
};

function printCountdownTimer(labelID, checkboxID, secondsLeft){
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
    },750);
};

function checkTimeFormat(i){
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
};