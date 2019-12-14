$(document).ready(function() {

    let colors = ["#98abc5", "#ccff99", "#7b6888", "#87f1ff", "#b300b3", "#c76be8", "#3cff26",
    "#3f95a1", "#ff4252", "#5e7c80", "#ff9442", "#ff99ff", "#6fbd84", "#ffd1de", "#98abc5", "#ccff99", "#7b6888", "#87f1ff", "#b300b3", "#c76be8", "#3cff26",
    "#3f95a1", "#ff4252", "#5e7c80", "#ff9442", "#ff99ff", "#6fbd84", "#ffd1de"];

    function count_occurrences(genres){
            let unique_genres = [];
            let genre_count = [];
            for(let genre in genres){
                genre = genres[genre];
                if(unique_genres.includes(genre)){
                    const index = unique_genres.indexOf(genre);
                    genre_count[index].value = ((genres.length * genre_count[index].value) + 1) / genres.length;
                }
                else{
                    unique_genres.push(genre);
                    genre_count.push({label: genre, value: 1 / genres.length});
                }
            }
            return genre_count;
        }

    let main_svg = d3.select("#svg-holder")
        .append("svg")
        .attr("class", "main_svg d-flex justify-content-center");

    let svg = main_svg
        .append("g")
        .attr("class", "svg_group");

    svg.append("g")
        .attr("class", "slices");
    svg.append("g")
        .attr("class", "labels");
    svg.append("g")
        .attr("class", "lines");


    let width = 600,
        height = 450,
        radius = Math.min(width, height) / 3.5;
    main_svg.attr("width", width);
    main_svg.attr("height", height);

    let pie = d3.pie()
        .sort(null)
        .value(function(d) {
        return d.value;
    });

    let arc = d3.arc()
        .outerRadius(radius * 0.8)
        .innerRadius(radius * 0.4);

    let outerArc = d3.arc()
        .innerRadius(radius * 0.9)
        .outerRadius(radius * 0.9);

    svg.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    let key = function(d){
        return d.data.label;};

    function change(data) {
        /* ------- PIE SLICES -------*/
        let slice = svg.select(".slices").selectAll("path.slice")
            .data(pie(data), function(d){
                return d.data.label;});

        slice.enter()
            .insert("path")
            .style("fill", function(d, i) {
                return colors[i]; })
            .attr("class", "slice");

        slice.transition().duration(1000)
            .attrTween("d", function(d) {
                this._current = this._current || d;
                let interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    return arc(interpolate(t));
                };
            });

        slice.exit()
            .remove();

        /* ------- TEXT LABELS -------*/

        let text = svg.select(".labels").selectAll("text")
            .data(pie(data), key);

        text.enter()
            .append("text")
            .attr("dy", ".35em")
            .style("font-size", "11px")
            .text(function(d) {
                return d.data.label;
            });

        function midAngle(d){
            return d.startAngle + (d.endAngle - d.startAngle)/2;
        }

        text.transition().duration(1000)
            .attrTween("transform", function(d) {
                this._current = this._current || d;
                let interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    let d2 = interpolate(t);
                    let pos = outerArc.centroid(d2);
                    pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
                    return "translate("+ pos +")";
                };
            })
            .styleTween("text-anchor", function(d){
                this._current = this._current || d;
                let interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    let d2 = interpolate(t);
                    return midAngle(d2) < Math.PI ? "start":"end";
                };
            });

        text.exit()
            .remove();

        /* ------- SLICE TO TEXT POLYLINES -------*/
        let polyline = svg.select(".lines").selectAll("polyline")
            .data(pie(data), key);

        polyline.enter()
            .append("polyline")
            .attr("fill", "none")
            .attr("stroke", "black");

        polyline.transition().duration(1000)
            .attrTween("points", function(d){
                this._current = this._current || d;
                let interpolate = d3.interpolate(this._current, d);
                this._current = interpolate(0);
                return function(t) {
                    let d2 = interpolate(t);
                    let pos = outerArc.centroid(d2);
                    pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
                    return [arc.centroid(d2), outerArc.centroid(d2), pos];
                };
            });

        polyline.exit()
            .remove();
    }


    // ---------------------------------------------------------------------------------------
    let current_book = null;
    let rating_box = $('#rating-box');
    let rating_feedback = $('#rating-feedback');
    let select_box = $('#search-input');
    const urlParams = new URLSearchParams(window.location.search);
    let user = urlParams.get('user');

    function createRecommenderComponent(position, title, genres){
        let div1 = document.createElement("div");
        div1.style = "min-height: 52px";
        div1.className = "row recommended-item";

        let div2 = document.createElement("div");
        div2.className = "col-1 d-flex justify-content-center";
        div2.style = "margin: 0px; padding: 0px;";

        let div2_p = document.createElement("p");
        div2_p.style = "text-align: center";
        div2_p.className = "my-auto";
        div2_p.innerHTML = position + '.';
        div2.appendChild(div2_p);
        div1.appendChild(div2);

        let div3 = document.createElement("div");
        div3.className = "col-6 d-flex";

        let div3_p = document.createElement("p");
        div3_p.style = "font-weight: bold; font-size: 13px;";
        div3_p.className = "rated-title my-auto";
        div3_p.innerHTML = title;
        div3.appendChild(div3_p);
        div1.appendChild(div3);

        let div4 = document.createElement("div");
        div4.className = "col-5 d-flex";

        let div4_p = document.createElement("p");
        div4_p.style = "font-weight: bold; font-size: 13px;";
        div4_p.className = "rated-title my-auto";
        div4_p.innerHTML = genres;
        div4.appendChild(div4_p);
        div1.appendChild(div4);
        return div1;
    }


    function refresh_recommendations(number){
        document.getElementById("add-recommendations").innerHTML = '';
        $.ajax({
			type : 'GET',
			url : '/getpredictions',
            data: {
			    user_id: user,
                number: number // initially, now need to get toggle value of how many recommendations to retrieve
            },
            contenttype: "application/json",
			success: function(response){
			    // render ratings
                let genre_array = [];
                if(response){
                    for(let i = 0; i < response.length; i ++){
                        let book_title = response[i][3];
                        let book_genres = response[i][6];   // need to do something with genres
                        // do something with non-parsed genres

                        let parsed_genres = parseGenres(book_genres);
                        genre_array = genre_array.concat(parsed_genres);
                        change(count_occurrences(genre_array));
                        let component = createRecommenderComponent((i + 1).toString(), book_title, parsed_genres.join(", "));
                        document.getElementById("add-recommendations").appendChild(component);
                    }

                    const buttons = document.querySelectorAll(".delete-button");
                    for (let button of buttons) {
                        button.addEventListener('click', initiateRatingDelete);
                    }

                    const current_ratings = document.querySelectorAll(".already-rated-book");
                    for (let current of current_ratings) {
                        current.addEventListener('click', openBookRating);
                    }
			    }
                return genre_array;
			}
		});
    }


    function createRatingComponent(rating_val, title, book_id){
        let my_div = document.createElement("div");
        my_div.setAttribute("data-book", book_id);
        my_div.setAttribute("data-title", title);
        my_div.style = "min-height: 40px";
        my_div.className = "row already-rated-book";

        let title_div = document.createElement("div");
        title_div.className = "col-9 d-flex";
        let inner_p = document.createElement("p");
        inner_p.style = "font-weight: bold; font-size: 13px";
        inner_p.className = "rated-title my-auto";
        inner_p.innerHTML = title;
        title_div.appendChild(inner_p);
        my_div.appendChild(title_div);

        let star_div = document.createElement("div");
        star_div.className = "col-2 d-flex";
        star_div.style = "margin: 0; padding:0";
        let inner_p_2 = document.createElement("p");
        inner_p_2.style = "font-weight:bold; color: #fcba03";
        inner_p_2.className = "rated-star my-auto";
        inner_p_2.innerHTML = rating_val + '<span class="fa fa-star checked" aria-hidden="true"></span>';
        star_div.appendChild(inner_p_2);
        my_div.appendChild(star_div);

        let bin_div = document.createElement("div");
        bin_div.className = "col-1 justify-content-center";
        bin_div.style = "margin: 0; padding:0";
        let bin_icon = document.createElement("i");
        bin_icon.className = "far fa-trash-alt delete-button";
        bin_icon.setAttribute("data-book", book_id);
        bin_div.appendChild(bin_icon);
        my_div.appendChild(bin_div);
        return my_div;
    }

    let initiateRatingDelete = function(){
        // delete rating
        let book_id = this.getAttribute("data-book");
        // delete rating
        $.ajax({
        data : {
            book_id : book_id,
            user_id: user
        },
        type : 'POST',
        url : '/deleterating',
        success: function(){
            // remove now from position
            document.getElementById('rating-box').value = '';
            populateAlreadyRated(user);
            if($('.slider').attr("data-check") === "off"){
            // 5 recommendations
            refresh_recommendations(5);
            }
            else{
                // 10 recommendations
                refresh_recommendations(10);
            }
            }
        });
    };

    let openBookRating = function(){
        reset_selection();
        let book_id = this.getAttribute("data-book");
        $.ajax({
			type : 'GET',
			url : '/getbook',
            data: {
			    user_id: user,
                book_id: book_id
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response);
			}
		});
    };


    function populateAlreadyRated(user_id){
        document.getElementById("ratings-window").innerHTML = '';
        $.ajax({
			type : 'GET',
			url : '/getalluserratings',
            data: {
			    user_id: user_id,
            },
			success: function(response){
			    if(response.length > 0){
                    for(let i = 0; i < response.length; i ++){
                        let book_id = response[i][0][0];
                        let book_rating = response[i][1];   // might need to use ParseInt
                        let book_title = response[i][0][3];
                        let component = createRatingComponent(book_rating, book_title, book_id);
                        document.getElementById("ratings-window").appendChild(component);
                    }
                        const buttons = document.querySelectorAll(".delete-button");
                        for (let button of buttons) {
                            button.addEventListener('click', initiateRatingDelete);
                        }

                        const current_ratings = document.querySelectorAll(".already-rated-book");
                        for (let current of current_ratings) {
                            current.addEventListener('click', openBookRating);
                        }
			    }
			    else{
			        document.getElementById('ratings-window').innerHTML = '<p style="font-size: 11px; margin-top: 10px; text-align: center">This user has no ratings!</p>';
                }
            }
		});
    }
    populateAlreadyRated(user);

    function populateUserField(user_id){
        document.getElementById('user-id-box').innerHTML = 'User '+ user_id;
    }

    function remove_rating_style(){
        document.getElementById('rating-feedback').innerHTML = '';
        rating_box.val('');
        rating_box.css("box-shadow", 'None');
    }

    function parseGenres(string_val){
        let genres = string_val.split("|");
        if(genres.length > 3){
            genres = genres.slice(0, 3);
        }
        return genres;
    }

    function reset_selection(){
        $('#search-input').get(0).selectedIndex = 0;
    }


    function render_ratings(response){
        let avg_rating = Math.round(parseInt(response.avg_rating));
        const checked_star = '<span class="fa fa-star'+' checked'+'"></span>';
        const unchecked_star = '<span class="far fa-star"></span>';
        let html_stars = checked_star.repeat(avg_rating) + unchecked_star.repeat(5 - avg_rating);
        document.getElementById('avg-rating-p').innerHTML = 'Avg. rating: '
            + html_stars + ' ' + response.avg_rating;

        current_book = response;
        let year = '<strong>Year: </strong>' + Math.round(parseInt(response.year)).toString();
        let title_box = document.getElementById('title_h1');
        title_box.setAttribute("data-id", response.id);
        title_box.innerHTML = response.title;
        document.getElementById('year_p').innerHTML = year;
        document.getElementById('author_p').innerHTML = '<strong>Author: </strong>' + response.authors;
        document.getElementById('genre_p').innerHTML = '<strong>Genre: </strong>' + response.genres;
        if(response.rating){
            document.getElementById('rating-box').value = parseInt(response.rating);}
        $('.img-border .book-img').attr("src", response.image_path);
    }

    function invalid_input(element){
		element.css("box-shadow", "0 0 10px rgb(255, 0, 0)");
	    rating_feedback.css("color", 'red');
    }

	function valid_input(element) {
		element.css("box-shadow", "0 0 10px rgb(0, 255, 63)");
		rating_feedback.css("color", "green");
    }

    function get_all_books(){
        // delete all books first
        $.ajax({
			type : 'GET',
			url : '/allbooks',
			success: function(response){
			    let html_text = '<option disabled selected value> -- Select a title -- </option>\n';
			    for (let i = 0; i < response.length; i++) {
			        html_text += '<option value="' + response[i][0] + '">' + response[i][3] + '</option>'
                }
			    document.getElementById('search-input').innerHTML = html_text;
            }
		});
    }

    select_box.on('change', function(){
        book_id = select_box.val();
        remove_rating_style();
        $.ajax({
			type : 'GET',
			url : '/getbook',
            data: {
			    user_id: user,
                book_id: book_id
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response);
			}
		});
    });


    function get_random_book(user_id){
        reset_selection();
        $.ajax({
			type : 'GET',
			url : '/randombook',
            data: {
                user_id: user_id
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response);
            }
		});
    }

    $('#refreshIcon').on('click', function(event){
        remove_rating_style();
        get_random_book(user);
    });


    function get_book(book_name){
        book_name = book_name || "hello";
        // Need to get a book from its title
        $.ajax({
			type : 'GET',
			url : '/getbook',
            data: {
                book_name: book_name
            },
            contenttype: "application/json",
			success: function(response){
			    render_ratings(response);
            }
		});
    }

    // When a book is clicked, the rating box is shown
    $('.img-border').on('click', function(event) {
        let input = this.parentNode.parentNode.parentNode.querySelector('#input_row input');
        input.focus();
	});

    rating_box.on('change', function(event){
        // validate
        let val = rating_box.val();
        if(val){
            if(Number.isNaN(val)){
                document.getElementById('rating-feedback').innerHTML = 'Rating must be a number from 1 to 5';
                invalid_input(rating_box);
            }
            else{
                let int_val = parseInt(val);
                if(int_val >= 1 && int_val <= 5){
                    document.getElementById('rating-feedback').innerHTML = '';
                    valid_input(rating_box);
                }
                else{
                    invalid_input(rating_box);
                    document.getElementById('rating-feedback').innerHTML = 'Rating must be a number from 1 to 5';
                }
            }
        }
        else{
            remove_rating_style();
        }
    });

    $('#submit-circle').on('click', function(event) {
        let title_box = document.getElementById('title_h1');
        $.ajax({
        data : {
            user_id: user,
            book_id: title_box.getAttribute("data-id"),
            rating : rating_box.val()
        },
        type : 'POST',
        url : '/updaterating',
        success: function(response){
            if(response){
                // If we get a non-empty response, rating value was invalid
                document.getElementById('rating-feedback').innerHTML = response;
                invalid_input(rating_box);
            }
            else{
                populateAlreadyRated(user);
                remove_rating_style();
                get_random_book(user);
                if($('.slider').attr("data-check") === "off"){
                // 5 recommendations
                refresh_recommendations(5);
                }
                else{
                    // 10 recommendations
                    refresh_recommendations(10);
                }
            }
        }
        });
    });

    $('.slider').on('click', function(){
        if(this.getAttribute("data-check") === "on"){
            this.setAttribute("data-check", "off");
            // 5 recommendations
            refresh_recommendations(5);
        }
        else{
            this.setAttribute("data-check", "on");
            // 10 recommendations
            refresh_recommendations(10);
        }
    });

    get_random_book('1');
    get_all_books();
    populateUserField(user);
    refresh_recommendations(5);
});