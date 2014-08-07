 $('.table-hover tr').click(function() {
	   	 var rowId = $(this).data("rowKey");
	   	 
	 	 $.ajax({
	   	    type : 'GET',
	   	    url : "http://127.0.0.1:5000/load_ajax/"+rowId,
	   	    success: function(data) {
	   	    	data = jQuery.parseJSON(data);
	   	    	show_graph(data, rowId)
	   	    },
	   	 error:function(){alert(rowId);}
	   	});
	   	 
	   	     
	     $('#myModal').on('show', function () {
		        $(this).find('.modal-body').css({
		               width:'auto', 
		               height:'auto',  
		               'max-height':'100%'
		        });
		 	  });
	     $('#myModal').modal('show');
    });
 
 
 function show_graph (data, rowId) {
	
	 $('#graph-container').highcharts({
	        title: {
	            text: 'CPU & Memory Usage',
	            x: -20 //center
	        },
	        subtitle: {
                text: 'Process Id : ' + rowId,
                x: -20
            },
	        
	        xAxis: {
	             type: 'datetime',
		         dateTimeLabelFormats: {
		             day:'%H:%M' 
		         }
	        },
	        plotOptions: {
	            series: {
			        pointStart:Date.UTC(data[2][0],data[2][1]-1,data[2][2],data[2][3],data[2][4]),
		            pointInterval: ( 3600 * 1000 )/24 
	            }
	        },
	        yAxis: {
	            title: {
	                text: 'Usage (%)'
	            },
	            plotLines: [{
	                    value: 0,
	                    width: 1,
	                    color: '#808080'
	                }]
	           
	        },
	        tooltip: {
	            valueSuffix: '%'
	        },
	        legend: {
	            layout: 'vertical',
	            align: 'right',
	            verticalAlign: 'middle',
	            borderWidth: 0
	        },
	        series: [{
	            name: 'CPU Usage',
	            data: data[0]
	        },
	        
	        {
	            name: 'Memory Usage',
	            data: data[1]
	        }]
	    });
	}
 
 $(function(){
	   
	    $('.nav-tabs a').on('click', function (e) {
	        e.preventDefault();
	        $(this).tab('show');
	    });
	    
	});