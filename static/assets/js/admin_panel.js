let adminPanelsidebar = document.querySelector(".adminPanelsidebar");
let AdminPanelsidebarBtn = document.querySelector(".AdminPanelsidebarBtn");
AdminPanelsidebarBtn.onclick = function() {
  adminPanelsidebar.classList.toggle("active");
  if(adminPanelsidebar.classList.contains("active")){
    AdminPanelsidebarBtn.classList.replace("bx-menu" ,"bx-menu-alt-right");
}else
AdminPanelsidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
}
