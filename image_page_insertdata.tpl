<div class="content-wrapper">
    <div class="container-fluid">
      <!-- Breadcrumbs-->
      <ol class="breadcrumb">
        <li class="breadcrumb-item active">Image Database</li>
      </ol>
      
	  <div class="row">
        <div class="col-lg-6">
          <!-- Example Bar Chart Card-->
          <div class="card mb-3">
            <div class="card-header">
              <i class="fa fa-picture-o"></i> Upload Image</div>
            <div class="card-body">
              <div class="row">
                <form action="/upload" method="post" enctype="multipart/form-data">				  
				  <div class="form-group">
                    <!--<label for="usr">Name:</label>-->
                    <input type="text" name='name' class="form-control" id="usr" placeholder="Name">
                </div>
                <div class="form-group">
        				<!--<label for="exampleFormControlFile1">Upload the file</label>-->
    					<input type="file" name='upload' class="form-control-file" id="exampleFormControlFile1">
				  </div>
                <input type="submit" class="btn btn-primary btn-block" value='Submit'/>                
				</form>
                
              </div>
            </div>
            <div class="card-footer small text-muted"></div>
          </div>
        </div>
        <div class="col-lg-6">
          <!-- Train Section-->
          <div class="card mb-3">
            <div class="card-header">
              <i class="fa fa-microchip"></i> Train</div>
            <div class="card-body">
                <form action="/train" method="post" enctype="multipart/form-data">
                  <input type="submit" class="btn btn-warning btn-block" value="Train"/>
                </form>
              
            </div>
            <div class="card-footer small text-muted"></div>
          </div>
          
        </div>
      </div>
	  
	  <!-- Area Chart Example-->
      <div class="card mb-3">
        <div class="card-header">
          <i class="fa fa-database"></i> Image Library
        </div>
        <div class="card-body">

		        %for item in image_info:
        		        %for i in item:
                        <div class="gallery-item">
                        <img class="object-fit_contain" src="{{ get_url('static', filename=i) }}" width="130px" height="130px"/>
                        </div>
        		        
                    %end
                %end    
        </div>
        <div class="card-footer small text-muted"></div>
      </div>
      
    
  </div>