/**************************************************************
                     Constants
**************************************************************/

commandLineVisible = true;
currentScr = 'main';

/*************************************************************
                     Code
*************************************************************/

$(function(){
    $('#commandLine').keypress(cmdLineKeyPress);
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
	       $.each(data, function(scr, txt){
		   if($('#' + scr).length == 0)
		   {
		       $('#tabmenu').append('<li><a href="javascript:void(0);" onclick="changeScreen(\''+scr+'\');">' + 
					    scr.toLowerCase().replace(/\b[a-z]/g, function(letter){ 
						return letter.toUpperCase(); 
					    }) + '</a></li>');
		       $('#contentArea').append('<div id="' + scr + '" class="content"></div>');
		       $('#' + scr).css("display", "none");
		   }
		   $('#' + scr).append(txt + '<br/>');
	       });
	       setTimeout('UpdateScreen()', 1000);
	   },
	   'json')
	   .error(function(xhr, ajaxOptions, thrownError) {alert('error!' + thrownError);});
}

function changeScreen(scr)
{
    if(scr != currentScr)
    {
	$('#' + currentScr).css("display", "none");
	$('#' + scr).css("display", "inline");
	currentScr = scr;
    }
}

function cmdLineKeyPress(event)
{
    if(event.which == 13)
    {
	$.post('/cmd.pdsp',$('#commandLine').serialize(),function(data){},'json');
	$('#commandLine').val('');
    }
}

/*****************************************************************
                          Menu Code
*****************************************************************/

function addDeviceClick()
{
    var overlayHTML = '<div id="overlay" class="overlay"><div id="popup" class="popup">' + 
                      'Device: <select id="deviceSelect"><option value="Device 1">Device 1</option></select>' + 
                      '<br/><br/>Device Name: <input type="text" id="deviceName"/>' +
                      '</div></div>';

    $('body').append(overlayHTML);
    $('#overlay').fadeIn('fast');
}
