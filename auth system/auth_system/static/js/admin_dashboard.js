class AdminDashboard {
    constructor() {
        this.commonConfig = {
            processing: true,
            serverSide: false,
            dom: 'Bfrtip',
            pageLength: 10
        };

        this.initializeTables();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    initializeTables() {
        this.createTable('#attendance-table', [
            { data: 'user_username', title: 'Employee' },
            { data: 'check_in', title: 'Check-in' },
            { data: 'check_out', title: 'Check-out' },
            { data: 'late_duration', title: 'Late Duration' },
            {
                data: null,
                title: 'Actions',
                render: data =>
                    `<button class="btn btn-warning btn-sm view-details" data-id="${data.id}">Details</button>`
            }
        ]);

        this.createTable('#leave-table', [
            { data: 'user_username', title: 'Employee' },
            { data: 'start_date', title: 'Start Date' },
            { data: 'end_date', title: 'End Date' },
            {
                data: null,
                title: 'Actions',
                render: data =>
                    `<button class="btn btn-success btn-sm approve-leave" data-id="${data.id}">Approve</button>
                     <button class="btn btn-danger btn-sm reject-leave" data-id="${data.id}">Reject</button>`
            }
        ]);

        this.createTable('#reports-table', [
            { data: 'user_username', title: 'Employee' },
            { data: 'total_hours', title: 'Total Hours' },
            { data: 'total_late_minutes', title: 'Late Minutes' }
        ]);

        this.loadData();
    }

    createTable(selector, columns) {
        if ($(selector).length) {
            $(selector).DataTable({
                ...this.commonConfig,
                data: [],
                columns
            });
        }
    }

    async loadData() {
        try {
            const endpoints = {
                '/leave-requests': '/api/leave-requests/',
                '/monthly-reports': '/api/admin/monthly-reports/',
                '/attendance': '/api/admin/dashboard/'
            };
            const currentPage = window.location.pathname;
            const endpoint = endpoints[Object.keys(endpoints).find(page => currentPage.includes(page))] || '/api/admin/dashboard/';
            const tableId = `${Object.keys(endpoints).find(page => currentPage.includes(page))?.replace('/', '') || 'attendance'}-table`;

            const response = await fetch(endpoint, {
                headers: { 'Authorization': 'Token YOUR_AUTH_TOKEN' }
            });
            const data = await response.json();

            if ($(`#${tableId}`).length) {
                const table = $(`#${tableId}`).DataTable();
                table.clear();
                table.rows.add(data || []);
                table.draw();
            }
        } catch (error) {
            console.error('Error loading data:', error);
            toastr.error('Failed to load data');
        }
    }

    setupEventListeners() {
        $(document).on('click', '.approve-leave, .reject-leave', e => {
            const button = $(e.currentTarget);
            const action = button.hasClass('approve-leave') ? 'approve' : 'reject';
            this.handleLeaveAction(button.data('id'), action);
        });
    }

    async handleLeaveAction(leaveId, action) {
        try {
            const response = await fetch('/api/leave-requests/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Authorization': 'Token YOUR_AUTH_TOKEN'
                },
                body: JSON.stringify({ leave_id: leaveId, action })
            });

            if (response.ok) {
                toastr.success(`Leave request ${action}ed successfully`);
                this.loadData();
            } else {
                toastr.error('Failed to process request');
                console.error(await response.text());
            }
        } catch (error) {
            console.error('Error:', error);
            toastr.error('Error processing request');
        }
    }

    startAutoRefresh() {
        setInterval(() => this.loadData(), 300000);
    }
}

$(document).ready(() => {
    if (typeof $.fn.DataTable === 'undefined') {
        console.error('DataTables not loaded!');
        return;
    }
    new AdminDashboard();
});
