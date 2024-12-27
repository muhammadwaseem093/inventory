/*!
 * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
 * Copyright 2013-2023 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
 */
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {
    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    const sidenavContent = document.body.querySelector('#layoutSidenav_content');
    const layoutSidenav = document.body.querySelector('#layoutSidenav');

    // Helper function: Adjusts the content area based on toggle state
    function adjustSideNavContent() {
        const isSidebarToggled = document.body.classList.contains('sb-sidenav-toggled');

        if (isSidebarToggled) {
            sidenavContent.style.marginLeft = '-100px';
            sidenavContent.style.width = '100%';
        } else {
            sidenavContent.style.marginLeft = '220px';
            sidenavContent.style.width = 'calc(100% - 220px)';
        }

        if (isSidebarToggled) {
            layoutSidenav.classList.add('sb-sidenav-collapsed');
        } else {
            layoutSidenav.classList.remove('sb-sidenav-collapsed');
        }
    }

    // Initialize the sidebar toggle state
    function initializeSidebarState() {
        const savedState = localStorage.getItem('sb|sidebar-toggle') === 'true';

        if (savedState) {
            document.body.classList.add('sb-sidenav-toggled');
        } else {
            document.body.classList.remove('sb-sidenav-toggled');
        }

        adjustSideNavContent();
    }

    // Initialize on page load
    initializeSidebarState();

    // Add event listener for the toggle button
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
            adjustSideNavContent();
        });
    }
});
