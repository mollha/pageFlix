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
		$("html").load("/view");
	});

	$('#refreshIcon').on('click', function(event) {
		$.ajax({
			type : 'GET',
			url : '/getuser',
			success: function(response){
			    $("#userInput").val(response);
            }
		});
	});

});