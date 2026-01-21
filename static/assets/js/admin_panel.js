let adminPanelsidebar = document.querySelector(".adminPanelsidebar");
let AdminPanelsidebarBtn = document.querySelector(".AdminPanelsidebarBtn");
AdminPanelsidebarBtn.onclick = function() {
  adminPanelsidebar.classList.toggle("active");
  if(adminPanelsidebar.classList.contains("active")){
    AdminPanelsidebarBtn.classList.replace("bx-menu" ,"bx-menu-alt-right");
}else
AdminPanelsidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
}



function goBack() {
  window.history.back();
}

// JavaScript function for cancel action (you can customize this)
function cancel() {
  alert("Cancelled!");
}



function toggleDetails() {
  var details = document.querySelector('.individual-product-details');
  if (details.style.display === 'none' || details.style.display === '') {
      details.style.display = 'block';
  } else {
      details.style.display = 'none';
  }
}
