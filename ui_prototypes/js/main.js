;if($ && $===jQuery) 
{

$(function()
{
	$('#login_form_submit_button').click(function(evt) 
	{
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
	$.post(login_form.attr('action'), login_form.serialize(), login_form_submit_callback, "json");
}

var error_template = '' + 
'<div class="ui-widget">' + 
'	<div style="padding: 0pt 0.7em;" class="ui-state-error ui-corner-all">' + 
'		<p class="error_message">' + 
'			<span class="ui-icon ui-icon-alert"></span>' + 
'			<span class="attention">Error:</span> {error}' + 
'		</p>' + 
'	</div>' + 
'</div>';

var logged_in_template = '' + 
'<h3>Welcome to PyQ</h3>' + 
'<ul id="profile_information">' + 
'	<li>' + 
'		<a href="/users/{username}" title="Go to Profile">{username}</a>' + 
'	</li>' + 
'	<li>' + 
'		Profile info goes here' + 
'	</li>' + 
'	</li>' + 
'</ul>' + 
'<div id="login_form_action_container">' + 
'	<a href="#" class="button ui-corner-all" id="login_form_logout_button" title="Log Out">' + 
'		Log Out</a>' + 
'</div>';

login_form_submit_callback(data)
{
	var template = "";
	if(data.error)
	{
		for(var prop in data)
		{
			template = error_template.replace(new RegExp("{"+prop+"}", "g"), data[prop])
		}
	}
	else
	{
		for(var prop in data)
		{
			template = logged_in_template.replace(new RegExp("{"+prop+"}", "g"), data[prop]);
		}
		$('#login').html("");
	}
	$('#login').prepend(template);
}

function search_form_submit_action(evt)
{
	$('#search_form').submit();
}

};