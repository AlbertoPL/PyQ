;(function($)
{

$(function()
{
	$('.response_link').click(function(evt) 
	{ 
		evt.stopPropagation();
		evt.preventDefault();
		response_link_click(evt); 
	});
	$('.delete').click(function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		delete_post(evt);
	});
	$('.edit').click(function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		edit_post_start(evt);
	});
	$('.upvote, .downvote').click(function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		vote(evt);
	});
	$('#post_answer_button').click(function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		post_answer(evt);
	});
	$('.answer_form').submit(function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		post_answer(evt);
	});
});

function vote(evt)
{
	var anchor = $(evt.target).parent();
	var direction = anchor.is('.upvote') ? 'up' : 'down';
	$.post(anchor.attr('href'), 'vote='+direction, function(data){ vote_callback(data, anchor.parent().parent()) }, "json");
}

function vote_callback(data, ballot_box)
{
	var vote_count = $('.vote_count', ballot_box);
	var current_count = new Number(vote_count.html());
	if( data.vote === 'upvote')
	{
		current_count++;
	}
	else if (data.vote === 'downvote')
	{
		current_count--;
	}
	
	if (data.unvote === 'downvote')
	{
		current_count++;
	}
	else if (data.unvote === 'upvote')
	{
		current_count--;
	}
	vote_count.html(current_count);
}

function edit_post_start(evt)
{
	var anchor = $(evt.target);
	var post_container = anchor.parent().parent();
	post_container.css('display', 'none');
	var post_text = $('p:first', post_container).html();
	var edit_form = post_container.next();
	edit_form.css('display', 'block');
	$('.edit_textarea', edit_form).html(post_text);
	var put_anchor = $('.button', edit_form);
	put_anchor.one('click', function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		edit_post(evt, edit_form);
	});
}

function edit_post(evt, edit_form)
{
	var anchor = $(evt.target);
	$.ajax(
	{
		type: 'PUT',
		url: anchor.attr('href'),
		data: edit_form.serialize(),
		dataType: 'json',
		success: edit_post_success
	});
}

function edit_post_success(evt)
{
	history.go(0);
}

function delete_post(evt)
{
	var anchor = $(evt.target);
	var container = anchor.attr('rel') == 'comment' ? 
		anchor.parent() : anchor.parent().parent();
	$.ajax({
		type: 'DELETE',
		url: anchor.attr('href'),
		dataType: 'json',
		success: function(data, textStatus){ delete_post_success(container, data, textStatus); }
	});
}

function delete_post_success(container, data, textStatus)
{
	container.css('display', 'none');
	if(data.url) location.href=data.url;
}

function response_link_click(evt)
{
	var anchor = $(evt.target);
	var response_form = $(".response_form", anchor.parent());
	anchor.css('display', 'none');
	response_form.css('display', 'block');
	$("a.response_button", response_form).one('click', function(evt)
	{
		evt.preventDefault();
		evt.stopPropagation();
		post_response(evt, response_form);
	});
	response_form.submit(function(evt)
	{
		evt.preventDefault();
		evt.stopPropagation();
		post_response(evt, response_form);
	});
}

function post_response(evt, response_form)
{
	var form_str = response_form.serialize();
	$.post(response_form.attr('action'), form_str, function(data){post_response_callback(data, response_form.parent())}, "json");
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
'<a rel="comment" title="Click here to delete this comment" href="/comment/{comment_id}/" class="delete"> X</a>' +
'	<span class="comment_username">{user}</span>:' + 
'	{post_text}' + 
'</li>';
	for(var prop in data)
	{
		comment_template = comment_template.replace(new RegExp("{"+prop+"}", "g"), data[prop]);
	}
	comment_list.append(comment_template);
	$('.delete:last').click(function(evt)
	{
		evt.stopPropagation();
		evt.preventDefault();
		delete_post(evt);
	});
}

function post_answer(evt)
{
	var answer_form = $(evt.target).is('form') ? evt.target : $(evt.target).parent();
	$.post(answer_form.attr('action'), 
			answer_form.serialize(), 
			function(data)
			{
				post_answer_callback(data, answer_form.parent());
			},
			"json"
	);
	$('textarea', answer_form).val('');
}

function post_answer_callback(data, answer_container)
{
	//console.log('post_answer_callback');
	history.go(0);
}

})(jQuery);
