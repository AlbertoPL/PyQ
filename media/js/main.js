;(function($)
{

$(function()
{
	$('#login_form').submit(function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		login_form_submit_action(evt);
	});
	$('#login_form_submit_button').click(function(evt) 
	{
		evt.stopPropagation();
		evt.preventDefault();
		login_form_submit_action(evt);
	});
	
	$('#search_form_button').click(function(evt)
	{
		search_form_submit_action(evt);
	});
});

function login_form_submit_action(evt)
{
	var login_form = $('#login_form');
	$.post(login_form.attr('action'), login_form.serialize(), function(data){login_form_submit_callback(data);}, "json");
}

function login_form_submit_callback(data)
{
	if(data.error)
	{
		for(var prop in data)
		{
			$('#login_error').html(
				$('#login_error').html().replace(new RegExp("{"+prop+"}", "g"), data[prop])
			).css("display", "block");
		}
	}
	else
	{
		for(var prop in data[0].fields)
		{
			$('#login > div:first').html(
					$('#login > div:first').html().replace(new RegExp("{"+prop+"}", "g"), data[0].fields[prop])
				).css("display", "block");
			$('div.nav.action_nav').css("display", "block");
		}
		$('#login_form').css("display", "none");
	}
}

function search_form_submit_action(evt)
{
	$('#search_form').submit();
}

})(jQuery);
