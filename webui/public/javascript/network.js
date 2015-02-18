insert_node = function(data, x, y){
    alert(data);
};

get_node = function(node_id){
    $.ajax({url:"/node/"+node_id,
           dataType:'json',
           success:insert_node});
};


$(document).on("click", ".node", function(){
   var net_id = this.id.split('_')[1];

    $('#scenario_list .table-row').addClass('hidden');

   var scenario_container = $('#network_'+net_id+'_scenarios').removeClass('hidden');

});

var sig = {
        container: 'static_graph',
        settings: {
            defaultNodeColor: '#ec5148',
        }
    }

$(document).ready(function(){
    $('#nodetable').DataTable({
        pageSize: 10,
        sort: [true, true, true, true],
        filters: [true, false, false, false],
        filterText: 'Type to filter... '
    }) ;

    $('#linktable').DataTable({
        pageSize: 10,
        sort: [true, true, true, true],
        filters: [true, false, false, false],
        filterText: 'Type to filter... '
    }) ;

    $('#linktable_wrapper').addClass('hidden');
    
    sig.graph = json_net;
    sig = new sigma(sig);
});

$(document).on('click', '#linktab', function(){
    $('#nodetable').addClass('hidden');           
    $('#nodetable_wrapper').addClass('hidden');           
    $('#linktable').removeClass('hidden');           
    $('#linktable_wrapper').removeClass('hidden');           
});

$(document).on('click', '#nodetab', function(){
    $('#linktable').addClass('hidden');           
    $('#linktable_wrapper').addClass('hidden');           
    $('#nodetable').removeClass('hidden');           
    $('#nodetable_wrapper').removeClass('hidden');           
});


$(document).on('click', '.noderow', function(){
    var success = function(data){
        add_overlay(data);
    }
    
    var node_id = this.id.split('_')[1]
    $.ajax({
        url:'/node?node_id='+node_id+'&scenario_id='+scenario_id,
        success:success,
    });

});

$(document).on('click', '.attributes .attribute.timeseries', function(){
    var ts_data = $(".attrval .contents", this).html();
    var js_data = jQuery.parseJSON(ts_data); 
    var index = [];
    for (t in js_data){
        index.push({"mData": t});
        console.log(t);
    }
    var data = []
    for (t in js_data[0]){
        data.push({'time':t, 'value':js_data[0][t]})
    }
    
    $("table", this).dataTable({
        'aaData':data,
        "aoColumns": [{"mData": 'time'}, {"mData": 'value'}],
    });
    var t = $("table", this).removeClass('hidden');

   /* var ts_table = $(
     '<table>' + $.map(js_data['0'], function(value,key){
         console.log(value);
         return '<tr><td>'+key+'</td><td>'+value+'</td></tr>'
      }).join('')+'</table>'
    );
    var x = $(".attrval", this);
    x.append(ts_table);*/
});


