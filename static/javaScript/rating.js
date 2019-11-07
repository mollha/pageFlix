$(document).ready(function() {


    // When a book is clicked, the rating box is shown
    $('.img-border').on('click', function(event) {
        let images = [].slice.call(document.querySelectorAll('.img-border'), 0); // get all images inside frame1, and convert to array
        let index = images.indexOf(this);
        let newa = this.parentNode.parentNode.parentNode.querySelectorAll('form #input_row .col-4');
        let input_col = newa[index];
        newa[index].querySelector('input').focus();
	});

});