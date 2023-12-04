//CHRISTIAN
function validateForm() {
    var urlInput = document.getElementById('urlInput').value;

    // Check if the URL input is empty
    if (urlInput.trim() === '') {
        alert('Please enter a website URL.');
        return false; // Prevent the form from being submitted
    }

    // You can add more validation if needed

    return true; // Allow the form to be submitted
}
function validateForm2() {
    var checkboxes = document.querySelectorAll('#myForm input[type="checkbox"]');
    var checkedCount = 0;

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkedCount++;
        }
    }

    if (checkedCount === 0) {
      alert('Please select items')
      return false;
    } else {
        return true;
    }
}
function validateForm3() {
    var radios = document.querySelectorAll('#myForm input[type="radio"]');
    var checkedCount = 0;

    for (var i = 0; i < radios.length; i++) {
      if (radios[i].checked) {
        checkedCount++;
      }
    }

    if (checkedCount === 0) {
      alert('Please select an option.');
      return false;
    } else {
      return true;
    }
}