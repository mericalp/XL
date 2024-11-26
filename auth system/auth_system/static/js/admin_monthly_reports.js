document.addEventListener("DOMContentLoaded", () => {
   const endpoint = "/api/admin/monthly-reports/";
   const tableElement = document.getElementById("reports-table");

   // Initialize DataTable
   const reportsTable = $(tableElement).DataTable({
       processing: true,
       serverSide: false,
       pageLength: 10,
       columns: [
           { data: "user_username", title: "Employee" },
           { data: "late_duration", title: "Late Minutes" },
           { data: "leave_days", title: "Remaining Leave Days" }
       ],
   });

   // Fetch data and populate the table
   async function loadReportsData() {
       try {
           const response = await fetch(endpoint, {
               method: "GET",
               headers: {
                   "Content-Type": "application/json",
               },
           });

           if (!response.ok) {
               throw new Error(`Error fetching reports: ${response.statusText}`);
           }

           const data = await response.json();
           reportsTable.clear();
           reportsTable.rows.add(data || []);
           reportsTable.draw();
       } catch (error) {
           console.error("Error loading data:", error);
       }
   }

   // Load data when the page is ready
   loadReportsData();
});
