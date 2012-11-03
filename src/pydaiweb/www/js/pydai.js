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
    var overlayHTML = '<div id="overlay" class="overlay"><div id="popup" class="popup">' + 
                      'Device: <select id="deviceSelect"><option value="Device 1">Device 1</option></select>' + 
                      '<br/><br/>Device Name: <input type="text" id="deviceName"/>' +
                      '</div></div>';

    $('body').append(overlayHTML);
    $('#overlay').fadeIn('fast');
}
