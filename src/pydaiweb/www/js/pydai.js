/**************************************************************
                     Constants
**************************************************************/

commandLineVisible = true;
currentScr = 'main';
availableDevs = [];

/*************************************************************
                     Code
*************************************************************/

$(function(){
    $('#commandLine').keypress(cmdLineKeyPress);
    $.get('/screenupdate.pdsp?availableDevs=true', 
        function(data){
            availableDevs = data.availableDevs;
        }, 'json');
    $.post('/cmd.pdsp',encodeURI('cmd=query devman'),function(data){},'json');
    UpdateScreen();
});

function animateComLine() {
    $('#commandLineSlide').slideToggle('slow');
    $('.content').animate({ bottom : (commandLineVisible ? '35px' : '60px') }, 'slow');
    commandLineVisible = !commandLineVisible;
}

function UpdateScreen()
{
    $.post('/screenupdate.pdsp',
	   '',
	   function(data){
    	   if(data.hasOwnProperty('screen')){
	       $.each(data.screen, function(scr, contents){
		   if($('#' + scr).length == 0)
		   {
		       $('#tabmenu').append('<li><a href="javascript:void(0);" onclick="changeScreen(\''+scr+'\');" id="' + scr + '_a">' + 
					    scr.toLowerCase().replace(/\b[a-z]/g, function(letter){ 
						return letter.toUpperCase(); 
					    }) + '</a></li>');
		       $('#contentArea').append('<div id="' + scr + '" class="content"></div>');
		       $('#' + scr).css("display", "none");
		   }
		   $('#' + scr).append(contents[1] + '<br/>');
	       });
	       }
	       setTimeout('UpdateScreen()', 1000);
	   },
	   'json')
	   .error(function(xhr, ajaxOptions, thrownError) {alert('error!' + thrownError);});
}

function changeScreen(scr)
{
    if(scr != currentScr)
    {
    $.post('/screenupdate.pdsp', 'window=' + scr, 
    function(data) {
    	$('#' + currentScr).css("display", "none");
	    $('#' + currentScr + '_a').removeClass("active");
    	$('#' + scr).css("display", "inline");
	    $('#' + scr + '_a').addClass("active");
	    currentScr = scr;
	    }, 'json');
    }
}

function cmdLineKeyPress(event)
{
    if(event.which == 13)
    {
        $('#' + currentScr).append('<br/>>>> ' + $('#commandLine').val() + '<br/><br/>')
    	$.post('/cmd.pdsp',$('#commandLine').serialize(),function(data){},'json');
	    $('#commandLine').val('');
    }
}

/*****************************************************************
                          Menu Code
*****************************************************************/

function addDeviceClick()
{
    var optionHTML = '';
    $.each(availableDevs, function(i, dev){
        optionHTML = optionHTML + '<option value="' + dev + '">' + dev + '</option>';
    });
    var overlayHTML = '<div id="popup_total"><div id="overlay" class="overlay"></div><div id="popup" class="popup">' +
                      '<div id="popup_title" class="popup_title">Add Device...</div><div id="popup_content" class="popup_content">' + 
                      'Device: <select id="deviceSelect">' + optionHTML + '</select>' + 
                      '<br/><br/>Device Name: <input type="text" id="deviceName" value="Not Implemented Yet"/>' +
                      '<br/><br/><div id="popup_buttons"><input type="submit" value="Ok" onclick="okPopupClick();" />' +
                      ' <input type="submit" value="Cancel" onclick="closePopup();" /></div>' +
                      '</div></div></div>';

    $('body').append(overlayHTML);
    
    left = $('#popup').width() / 2;
    ptop = $('#popup').height() / 2;
    
    alert('' + left + ':' + ptop);
    
    $('#popup').css({
        'margin-left': '-' + left + 'px',
        'margin-top': '-' + ptop + 'px'
    });
    
    $('#popup_total').css({ 'visibility': 'visible', 'display': 'none' });
    
    $('#popup_total').fadeIn('fast');
}

function closePopup()
{
    $('#popup_total').fadeOut('fast', function(){ $('#popup_total').remove(); });
}

function okPopupClick()
{
    /*
    if($('#deviceName').val() == '')
    {
        alert('"Device Name" needs a value.');
        return;
    }
    */
    $.post('/cmd.pdsp',encodeURI('cmd=new ' + $('#deviceSelect').val() /*+ ' as ' + $('#deviceName').val()*/),function(data){},'json');
    closePopup();
}
