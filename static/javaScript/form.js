$(document).ready(function() {

	$('#form').on('submit', function(event) {
		$.ajax({
			data : {
				name : $('#userInput').val(),
			},
			type : 'POST',
			url : '/process'
		});
		alert($('#userInput').val());
		event.preventDefault(); // HTML automatically tries to post the form, we therefore manually stop this

	});

});