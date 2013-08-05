;if($ && $===jQuery) 
{

$(function()
{
	$('.response_link').click(function(evt) 
	{ 
		response_link_click(evt); 
	});
});

function response_link_click(evt)
{
	evt.preventDefault();
	var anchor = $(evt.target);
	var response_form = $(".response_form", anchor.parent());
	anchor.css('display', 'none');
	response_form.css('display', 'block');
	$('.response_form').submit(function(evt)
	{
		evt.preventDefault();
		evt.stopPropagation();
	});
	$("a.response_button", response_form).one('click', function(evt)
	{
		post_response(evt);
	});
}

function post_response(evt)
{
	evt.preventDefault();
	evt.stopPropagation();
	var anchor = $(evt.target);
	var response_form = $(anchor.parent());
	var form_str = response_form.serialize();
	alert(form_str);
	data = {post_text: 'ajaxy comment being faked', post_timestamp: '2009-07-21', user: 'George IV' }
	//$.post(response_form.attr('href'), form_str, function(data){post_response_callback(data, response_form.parent())}, "json");
	setTimeout(function(){post_response_callback(data, response_form.parent())}, 1000);
}

function post_response_callback(data, response_container)
{
	response_container = $(response_container);
	var response_form = $(".response_form", response_container);
	$('div > textarea', response_form).val("");
	response_form.css('display', 'none');
	$(".response_link", response_container).css('display', 'inline');
	var comment_list = $("ul", response_container);
	var comment_template = '' +
'<li class="comment">' +
'	<span class="comment_username">{user}</span>:' + 
'	{post_text}' + 
'</li>';
	for(var prop in data)
	{
		comment_template = comment_template.replace(new RegExp("{"+prop+"}", "g"), data[prop]);
	}
	comment_list.append(comment_template);
}

};
