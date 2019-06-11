<div class="content-wrapper">
    <div class="container-fluid">
      <!-- Breadcrumbs-->
      <ol class="breadcrumb">
        <li class="breadcrumb-item active">Live Stream</li>
      </ol>
      <!-- Icon Cards-->
      <div class="card mb-3">
        <div class="card-header">
          <i class="fa fa-wrench"></i> Video Actions
         </div>
        <div class="card-body text-center">
            <form action="/stop" method="post" enctype="multipart/form-data">
              <div class="btn-group" role="group">
                  <input type="submit" class="btn btn-primary" value="Connect" name='Connect'>
                  <input type="submit" class="btn btn-success" value="Start" name='Start'/>
                  <input type="submit" class="btn btn-danger" value="Stop" name='Stop'/>
                  <!--
                  <input type="submit" class="btn btn-default btn-block" value="NotificationH" name='NotificationH'>
                  <input type="submit" class="btn btn-default btn-block" value="NotificationP" name='NotificationP'>
                  -->
              </div>
            </form>                                        			
        </div>
        <div class="card-footer small text-muted">
        </div>
      </div> 
      
          <!-- Area Chart Example-->
      <div class="card mb-3">
        <div class="card-header">
          <i class="fa fa-window-maximize"></i> Live Video Streaming
         </div>
        <div class="card-body">
        	  <img src="{{ get_url('video_feed') }}" />                                        			
        </div>
        <div class="card-footer small text-muted">
        </div>
      </div>
      
    </div>
                
  </div>