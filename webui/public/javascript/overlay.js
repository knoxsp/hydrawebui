function add_overlay(inner_html){
	//Find the overlay template from the dom and clone it.
	var overlay_html = $('#overlay').clone();

	overlay.setAttribute('id', "exposed_overlay")

	//Add the new overlay to the body
	$('body').append(overlay_html);
	
	//Insert the required html
	var content = $('#exposed_overlay .content');
	content.html(inner_html);
	
	//show the overlay.
	$('#exposed_overlay').removeClass('hidden');

	var table_content = $('#exposed_overlay .content table');
	if (table_content != undefined){
	    table_content.DataTable({
        	pageSize: 10,
        	sort: [true, true, true, true],
        	filters: [true, false, false, false],
        	filterText: 'Type to filter... '
    	}) ;
	}

}

function delete_overlay(){

	var current_overlay = $('#exposed_overlay');

	if (current_overlay != undefined){
		current_overlay.remove();
	}
}

$(document).on('click', '.cancel', function(){delete_overlay()});

$(document).keyup(function(e) {
	var current_overlay = $('#exposed_overlay');
	if (current_overlay != undefined){
  		if (e.keyCode == 27) { 
  			delete_overlay();
  		}
  	}
});


