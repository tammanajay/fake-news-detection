	
	jQuery( document ).ready(function() {
		// Doctors - show tests under category		
		jQuery('#catid').on('change',function(){
			var catid = jQuery(this).val();		
			if (catid != '') {				
				jQuery.ajax({
					url: '/doctorapp/getTestFromCategory/',
					dataType:'json',	
					data: { 'catid' : catid },
					success: function(data) {						
						var jsonobj = JSON.parse(data);						
						if(jsonobj) {
							jQuery('#testid').empty();
							jQuery("#testid").append('<option>--Select--</option>');
							jsonobj.forEach(function(jsonobj) {								
								jQuery("#testid").append('<option value="'+jsonobj.pk+'">'+jsonobj.fields.test_name+'</option>');
							});
						} else {
							jQuery("#testid").empty();
						}
					}
				});
			}
			else {
				jQuery('#testid').val('').hide();			
			}
					
		});


		// Doctors - show subtest under tests
		jQuery('#testid').on('change',function(){
			var testid = jQuery(this).val();		
			if (testid != '') {				
				jQuery.ajax({
					url: '/doctorapp/getSubTestFromTest/',
					dataType:'json',	
					data: { 'testid' : testid },
					success: function(data) {						
						var jsonobj = JSON.parse(data);						
						if(jsonobj) {
							jQuery('#subtest_id').empty();
							jQuery("#subtest_id").append('<option>--Select--</option>');
							jsonobj.forEach(function(jsonobj) {								
								jQuery("#subtest_id").append('<option value="'+jsonobj.pk+'">'+jsonobj.fields.subtest_name+'</option>');
							});
						} else {
							jQuery("#subtest_id").empty();
						}
					}
				});
			}
			else {
				jQuery('#subtest_id').val('').hide();			
			}
					
		});

		// LabTechnition - show subtests by orderid
		jQuery('#order_id').on('change',function(){
			
			var order_id = jQuery(this).val();
			//alert(order_id)		
			if (order_id != '') {				
				jQuery.ajax({
					url: '/labtechnitionapp/getSubTestsByOrderId/',
					dataType:'json',	
					data: { 'order_id' : order_id },
					success: function(data) {	
						//alert(data)					
						var jsonobj = JSON.parse(data);						
						if(jsonobj) {
							jQuery('.SubTest').empty();
							var html = '';							
							jsonobj.forEach(function(jsonobj) {
								html = html+'<div class="wrap-input100 validate-input m-b-23">'+
								'<span class="label-input100">Subtest Name</span>'+
								'<input type="text" name="SubTest" value="'+jsonobj.fields.SubTest+'" class="SubTest form-control" disabled=true >'+
								'<span class="focus-input100" data-symbol="&#xf206;"></span>'+
							'</div>'+
							'<div class="wrap-input100 validate-input m-b-23" data-validate = "Value is required">'+
								'<span class="label-input100">Value</span>'+
								'<input type="text" name="SubTest" value="" class="form-control" placeholder="Enter value..">'+
								'<span class="focus-input100" data-symbol="&#xf206;"></span>'+
							'</div>';	
							});
							jQuery("#subtests").html(html);
						} else {
							jQuery("#subtest_id").empty();
						}
					}
				});
			}
			else {
				jQuery('.SubTest').val('').hide();			
			}
					
		});

		
	});
				 


