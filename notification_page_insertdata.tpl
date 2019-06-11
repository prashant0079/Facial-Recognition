<div class="content-wrapper">
    
    <div class="container-fluid">
      <!-- Breadcrumbs-->
      <ol class="breadcrumb">       
        <li class="breadcrumb-item active">Notifications</li>
      </ol>
      
      <!-- Example Notifications Card-->
          <div class="card mb-3">
            <div class="card-header">
              <i class="fa fa-bell-o"></i> Notifications</div>
            <div class="list-group list-group-flush small">
            
            %for col in data:
  
                  <a class="list-group-item list-group-item-action" href="#">
                    <div class="media">
                      <img class="d-flex mr-3 rounded-circle" class="object-fit_contain" src="{{ get_url('static', filename=col[2]) }}" width="70px" height="70px">
                      <div class="media-body">
                        Face detected : {{col[0]}}
                        <div class="text-muted smaller">On {{col[1]}}</div>
                      </div>
                    </div>
                  </a>    
              
              %end          
            </div>
            <div class="card-footer small text-muted"></div>
          </div>
     
      
  </div>