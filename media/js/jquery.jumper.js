(function($)
{
  var template = 
"<div id='jumperBox' title='jumper'>" +
  "<p>Enter the contents of the link you wish to visit</p>" +
  "<div><input id='jumperInput' type='text'/></div>" +
  "<div id='jumperDetails'></div>"
"</div>";

var jumperBuffer = {};
var inputBuffer = "";
var cache = [];
var numSelected = 0;
var UNKNOWN_KEYCODE = 0;
var G_KEYCODE = 103;
var L_KEYCODE = 108;
var BACKSPACE_KEYCODE = 8;
var ENTER_KEYCODE = 13;

$(function()
{
	$('a').live('click', function()
	{
		if(this.href && $.trim(this.href).indexOf('javascript') !== 0)
		{
			window.location.href = this.href;
			return false;
		}
		return true;
	});
	
	$('#jumperInput').live('keypress', function(evt)
  {
  	inputBuffer = inputBuffer.replace(/^\s+/, '');
  	
    if( inputBuffer !== "" )
      $(cache).removeClass('jumper');
    var keyCode = evt.which;
    
    if( keyCode === BACKSPACE_KEYCODE )
    {
      inputBuffer = inputBuffer.substr(0, inputBuffer.length-1);
      getClickables(inputBuffer, false);
    }
    else if( keyCode !== ENTER_KEYCODE && keyCode !== UNKNOWN_KEYCODE )
    {
      inputBuffer += String.fromCharCode(keyCode);
      getClickables(inputBuffer, true);
    }

    if( inputBuffer !== "" )
      numSelected = $(cache).addClass('jumper').length;
    $('#jumperInput').val(inputBuffer);

    if( inputBuffer === "" )
      numSelected = 0;

    $('#jumperDetails').text('You have selected ' + numSelected + ' elements');

    if( keyCode === ENTER_KEYCODE )
    {
      $(cache).click();
      return true;
    }

    return false;
  });
});

function clearJumperBuffer()
{
  jumperBuffer = {};
}

function clearInputBuffer()
{
  inputBuffer = "";
}

function getClickables(text, useCache)
{
	var selector = useCache ? cache : '*';
	var currentClickables = [];
	$(selector, 'body').each(function(i)
	{
		var that = $(this);
		var events = $.data(this, 'events');
		if(that.is('a, [onclick]') || (events && events.click))
		{
			if(that.text().toLowerCase().indexOf(text.toLowerCase()) !== -1)
			{
				currentClickables.push(this);
			}
		}
	});
	cache = currentClickables;
	return cache;
}

function jumperClose(evt, ui)
{
	$('#jumperInput').val('');
	$(cache).removeClass('jumper');
	clearInputBuffer();
	clearJumperBuffer();
	$('#jumperDetails').text('');
}

function displayJumper()
{
  if( $.find('#jumperBox').length === 0 )
  {
    $('body').append(template);
    $('#jumperBox').dialog({
    	close: jumperClose
    });
  }
  else
  {
  	$('#jumperBox').dialog('open');
  }
  $('#jumperInput').val('').focus();
  getClickables("");
}

$(document).keypress(function(evt)
{
	if(!$(evt.target).is('input:text, textarea'))
	{
    var keyCode = evt.which;
    if( keyCode === L_KEYCODE && jumperBuffer[G_KEYCODE] )
    {
      displayJumper();
      clearJumperBuffer();
    }
    else if( keyCode === G_KEYCODE )
    {
      jumperBuffer[G_KEYCODE] = true;
    }
    else
    {
      clearJumperBuffer();
    }
	}
});

})(jQuery);
