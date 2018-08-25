function createClockRow(program_id, name, state, automatic){
    // creates <tbody> element
    var myTableBody = document.createElement("TBODY");

    // creating row
    var myRow = document.createElement("TR");

    // creates a <td> element
    var myNameLabelCell = document.createElement("TD");
    var myTimeOnCell = document.createElement("TD");
    var myTimeOffCell = document.createElement("TD");
    var myTimeLabelCell = document.createElement("TD");
    var myStateButtonCell = document.createElement("TD");
    var myCheckboxCell = document.createElement("TD");

    // creates name Label element
    var myNameLabel = document.createElement("LABEL");
    myNameLabel.id = "clockNameLabel" + program_id;
    var myNameTextNode = document.createTextNode(name + "-" + program_id);
    myNameLabel.appendChild(myNameTextNode);

    // created "Time On" label element
    var myTimeOnLabel = document.createElement("LABEL");
    myTimeOnLabel.id = "clockTimeOnLabel" + program_id;

    // created "Time Off" label element
    var myTimeOffLabel = document.createElement("LABEL");
    myTimeOffLabel.id = "clockTimeOffLabel" + program_id;

    // creates time Label element
    var myTimeLabel = document.createElement("LABEL");
    myTimeLabel.id = "clockTimeLabel" + program_id;

    // creates button element "State"
    var myStateButton = document.createElement('input');
    myStateButton.type = 'button';
    myStateButton.id = "clockStateButton" + program_id;
    if (state == 0){myStateButton.value = 'OFF';}
    else{myStateButton.value = 'ON';}
    myStateButton.addEventListener('click', function(){
        clickClockStateButton(program_id, myStateButton.id);
    });

    // creates a label for checkbox ...
    var myAutomaticLabel = document.createElement("LABEL");
    myAutomaticLabel.id = "clockAutomaticLabel" + program_id;

    // creates a checkbox
    var myCheckbox = document.createElement("input");
    myCheckbox.type = 'checkbox';
    myCheckbox.id = "clockCheckbox" + program_id;
    if (automatic == 0){
        myCheckbox.checked = false;
        var myAutomaticTextNode = document.createTextNode("Manual");
    }
    else {
        myCheckbox.checked = true;
        var myAutomaticTextNode = document.createTextNode("Automatic");
    }
    myCheckbox.addEventListener('change', function(){
        enableDisableClockButton(myCheckbox, myStateButton.id);
        changeClockAutomaticLabelText(myCheckbox.checked, myAutomaticLabel.id, program_id);
    });

    //... creates a label for checkbox ...
    myAutomaticLabel.htmlFor = myCheckbox.id;
    myAutomaticLabel.appendChild(myAutomaticTextNode);

    // appends the elements we created into the cell <td>
    myNameLabelCell.appendChild(myNameLabel);
    myTimeOnCell.appendChild(myTimeOnLabel);
    myTimeOffCell.appendChild(myTimeOffLabel);
    myTimeLabelCell.appendChild(myTimeLabel);
    myStateButtonCell.appendChild(myStateButton);
    myCheckboxCell.appendChild(myCheckbox);
    myCheckboxCell.appendChild(myAutomaticLabel);

    // appends the cell <td> into the row <tr>
    myRow.appendChild(myNameLabelCell);
    myRow.appendChild(myTimeOnCell);
    myRow.appendChild(myTimeOffCell);
    myRow.appendChild(myTimeLabelCell);
    myRow.appendChild(myStateButtonCell);
    myRow.appendChild(myCheckboxCell);

    // appends the row <tr> into the TableBody
    myTableBody.appendChild(myRow);

    return myTableBody;
};

function toggleClockButton(buttonID){
    var elem = document.getElementById(buttonID);
    if (elem.value=="OFF"){
        elem.value = "ON";
    }
    else {
        elem.value = "OFF";
    }
};

function clickClockStateButton(program_id, buttonID){
    toggleClockButton(buttonID);
    socket.emit('clock_change_state_manual', {program_id: program_id});
};

function enableDisableClockButton(checkbox, stateButtonID) {
    if(checkbox.checked == false){
        document.getElementById(stateButtonID).disabled = false;
    }
    else{
        document.getElementById(stateButtonID).disabled = true;
    }
};

function changeClockAutomaticLabelText(checked, labelID, program_id){
    if (checked == true){
        document.getElementById(labelID).innerHTML = "Automatic";
        // emit module program_id to resume timer
        socket.emit('clock_resume_timer', {program_id: program_id});
        //console.log('module countdown ' + program_id + ' timer resumed');
    }
    else{
        // set countdown module to manual
        document.getElementById(labelID).innerHTML = "Manual";
        // emit module program_id to pause timer
        socket.emit('clock_pause_timer', {program_id: program_id});
        //console.log('module countdown ' + program_id + ' timer paused');
    }
};