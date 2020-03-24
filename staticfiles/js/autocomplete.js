$(document).ready(function() {
    $('#searcher').autocomplete({source: function (query, process) {
        return $.getJSON(
            '{% url "search:autocomplete" %}', // this is the url for the view we created in step 1
             { query : query },
             function (data) {
                console.log(data) ;
                return process(data);
             });
        }});
 });
