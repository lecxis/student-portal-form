window.onload=function(){
    $('#myModal').modal('show');
    $('#student-form').submit(function(event){
        let first= $('#firstName').val();
        let middle= $('#middleName').val();
        let last= $('#lastName').val();
        let email= $('#email').val();
        let dob= $('#dob').val();
        let gender= $("input[name='gender']:checked").val();
        let phone= $('#phoneNumber').val();
        let address= $('#address').val();
        let state= $('#state').val();
        let lga= $('#lg').val();
        let NOK= $('#nok').val();
        let jamb= $('#jamb').val();
        
        let data= JSON.stringify({
            'firstName': first,
            'middleName': middle,
            'lastName': last,
            'email': email,
            'dateOfBirth': dob,
            'gender': gender,
            'phoneNumber': phone,
            'address': address,
            'state': state,
            'lga': lga,
            'NextOfKin': NOK,
            'jambScore': jamb
        });
        $.ajax({
            url:'/form',
            type: 'POST',
            dataType: 'json',
            data: data,
            contentType: 'application/json, charset=UTF-8',
            success: function(data){

            if (data=='success'){
                console.log('image wil be loaded...')
            let data2 =new FormData();
            data2.append('file', $('#image')[0].files[0]);
            data2.append("path", first+middle+last+'.png');

            $.ajax({
            url:'/form',
            type: 'POST',
            data: data2,
            enctype:'multipart/form-data',
            processData: false,
            contentType: false,
            success: function(data2){
                //console.log(date,code,response);
                console.log('response ',data2);
            setTimeout(function(){
                window.location.href = data2;
            },800)
            // event.preventDefault();
            },
            error:function(request,status, message){
                console.log(request.responseJSON.message);
                console.log('error occured')
             }
        })
            }
            else if (data='failure'){
                console.log('failed....')
                location.reload();
            }
            },
            error:function(err){
                console.log(err);
            }
        })
   
        }
    );

    // Function to open individual pages
    $('.view').click(function(){
       // let personId=$(this).attr('id');
       window.location.href = "person/"+$(this).attr('id');
        
        }
    );
    //change admission sataus of student
    $('.aStatus').change(function(){
        var status=document.querySelector('.aStatus').value;
        console.log(status);
        var id= $(this).attr('id');
        $.ajax({
            url:'/status',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'id': id,
                'status':status
            }),
            contentType: 'application/json, charset=UTF-8',
            success: function(data){
                if (data=='success')
                    location.reload();
            },
            error:function(err){
                console.log(err);
            }
        })
    });   
};

// populate state and local government
var populateSelect = function(){
    fetch('/states')
      .then(function (response) {
          return response.json();
      }).then(function (text) { 
        var states = text;
             document.querySelector('#state').addEventListener("change", updateLga);
            function updateLga(){
                var state=document.querySelector('#state').value;
                document.querySelector('#lg').innerHTML="";
                var lga;
                states.forEach(function(value){
                    if(state==value.state){
                        lga=value.local;
                    }
                });
                lga.forEach(function(value){
                    document.querySelector('#lg').innerHTML+=`<option>${value}</option>`
                });
            }
    });
}
  