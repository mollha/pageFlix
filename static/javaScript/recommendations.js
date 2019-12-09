document.addEventListener("DOMContentLoaded", function(){
    let all_genres = ["horror", "vampire", "childrens"];
    let colors = ["#98abc5", "#ccff99", "#7b6888", "#87f1ff", "#b300b3",
    "#3f95a1", "#ff4252", "#5e7c80", "#ff9442", "#ff99ff"];


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
        radius = Math.min(width, height) / 2.5;
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

    let key = function(d){ return d.data.label; };

    function randomData (){
        let genres = [];
        for(let i = 0; i < 10; i++){
            let new_genre = all_genres[Math.floor(Math.random() * all_genres.length)];
            genres.push(new_genre);
        }
        console.log(genres);
        genres = count_occurrences(genres);
        return genres;
    }

    change(randomData());

    d3.select(".randomize")
        .on("click", function(){
            change(randomData());
        });


    function change(data) {

        /* ------- PIE SLICES -------*/
        let slice = svg.select(".slices").selectAll("path.slice")
            .data(pie(data), key);

        slice.enter()
            .insert("path")
            .style("fill", function(d, i) {
                return colors[i]; })
            .attr("class", "slice");

        slice
            .transition().duration(1000)
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

    change(randomData());
});

