$( function() {
    $("form[id='storyUserForm']").validate({
        // Specify validation rules
        rules: {
          // The key name on the left side is the name attribute
          // of an input field. Validation rules are defined
          // on the right side
          user_code: {
              required: true,
              minlength: 4
          },
          age_group: {
              required: true
          },
          experiment_date_datepicker: {
            required: true,
            story_date: true
          },
          department: {
            required: true,
            minlength: 8
          },
          level: "required",
          agreed: "required",
          gender: "required"
        },
        // Specify validation error messages
        messages: {
          user_code: {
              required: "Please enter your user code",
              minlength: jQuery.validator.format("At least {0} characters required!")
          },
          age_group: {
              required: "Please select age group"
          },
          experiment_date_datepicker: {
              required: "Please enter your date of experiment"
          },
          department: {
            required: "Please enter your department"
          },
          level: {
            required: "Please select your academic level"
          },
          agreed: {
            required: "Please agree the data usage term"
          },
          gender: {
            required: "Please select gender"
          }
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function(form) {
            var userCode = $('#user_code').val()
            localStorage.setItem('user_code', userCode);
            localStorage.setItem('user_id', Number(userCode.replace(/[a-zA-Z\-_]+/, "")));
            localStorage.setItem('age_group', $('#age_group').val());
            localStorage.setItem('experiment_date_datepicker', $('#experiment_date_datepicker').val());
            localStorage.setItem('department', $('#department').val());
            localStorage.setItem('level', $('#level').val());
            localStorage.setItem('gender', $('#gender').val());
            localStorage.setItem('disability', $('#disability').prop( "checked" ));
            localStorage.setItem('agreed', $('#agreed').prop( "checked" ));
            window.location.href = "/experiment/steps/tasks.html";
        }
      });
    $('#userFormSubmit').on('click', function(){
      $('#storyUserForm').submit();
    });
});
