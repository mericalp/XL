// static/js/admin_request_leave.js
class LeaveRequestManager {
   constructor() {
       this.initializeTable();
   }

   initializeTable() {
       this.table = $('#leave-requests-table').DataTable({
           processing: true,
           serverSide: false,
           ajax: {
               url: '/api/leave-requests/',
               dataSrc: ''
           },
           columns: [
               {data: 'user_username'},
               {data: 'start_date'},
               {data: 'end_date'},
               {
                   data: 'approved',
                   render: function(data) {
                       const badges = {
                           true: '<span class="badge bg-success">Approved</span>',
                           false: '<span class="badge bg-danger">Rejected</span>',
                           null: '<span class="badge bg-warning">Pending</span>'
                       };
                       return badges[String(data)];
                   }
               },
               {
                   data: null,
                   render: function(data) {
                       if (data.approved === false) {
                           return `
                               <button class="btn btn-success btn-sm approve-request" data-id="${data.id}">
                                   Reconsider
                               </button>`;
                       }
                       if (data.approved === null) {
                           return `
                               <button class="btn btn-success btn-sm approve-request" data-id="${data.id}">
                                   Approve
                               </button>
                               <button class="btn btn-danger btn-sm reject-request" data-id="${data.id}">
                                   Reject
                               </button>`;
                       }
                       return '';
                   }
               }
           ]
       });

       $('#leave-requests-table').on('click', '.approve-request, .reject-request', (e) => {
           const button = $(e.currentTarget);
           const id = button.data('id');
           const isApprove = button.hasClass('approve-request');
           this.handleRequest(id, isApprove);
       });
   }

   async handleRequest(id, isApprove) {
       try {
           const response = await fetch('/api/leave-requests/', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
                   'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
               },
               body: JSON.stringify({
                   leave_id: id,
                   approved: isApprove
               })
           });
           
           if (response.ok) {
               this.table.ajax.reload();
           }
       } catch (error) {
           console.error('Error:', error);
       }
   }
}

$(document).ready(() => new LeaveRequestManager());