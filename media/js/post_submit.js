;(function($)
{
	$(function()
	{
		$('#submit_button').click(function(evt)
		{
			evt.preventDefault();
			evt.stopPropagation();
			post_submit(evt);
		});
	});
	
	function post_submit(evt)
	{
		var anchor = $(evt.target);
		var post_form = anchor.parent();
		post_form.submit();
	}
	
})(jQuery);